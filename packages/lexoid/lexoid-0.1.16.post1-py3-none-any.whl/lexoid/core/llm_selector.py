import base64
import io
import os
from glob import glob
from typing import Dict, List, Tuple

import cv2
import joblib
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from skimage.feature import hog
from skimage.transform import resize
from tqdm import tqdm

from lexoid.core.conversion_utils import convert_doc_to_base64_images


# ====================== Image Feature Extraction ======================


def base64_to_cv2_image(b64_string: str) -> np.ndarray:
    image_data = base64.b64decode(b64_string.split(",")[1])
    image = Image.open(io.BytesIO(image_data)).convert("L")  # grayscale
    return np.array(image)


def extract_edge_stats(edges: np.ndarray) -> Tuple[float, float, float, float]:
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    lengths = []
    angles = []

    for contour in contours:
        for i in range(1, len(contour)):
            p1 = contour[i - 1][0]
            p2 = contour[i][0]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = np.hypot(dx, dy)
            if length == 0:
                continue
            angle = np.degrees(np.arctan2(dy, dx))
            lengths.append(length)
            angles.append(angle)

    if not lengths:
        return 0.0, 0.0, 0.0, 0.0

    return (np.mean(lengths), np.var(lengths), np.mean(angles), np.var(angles))


def extract_hog_features(
    image: np.ndarray, resize_shape=(128, 128)
) -> Tuple[float, float]:
    """
    Extracts summary HOG features from an image.

    Returns:
        Tuple of (mean, variance) of the HOG feature vector.
    """
    resized = resize(image, resize_shape, anti_aliasing=True)
    features = hog(
        resized,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        feature_vector=True,
    )
    return np.mean(features), np.var(features)


def extract_page_features(img: np.ndarray) -> List[float]:
    h, w = img.shape
    aspect_ratio = w / h

    # Binarization
    _, bin_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text_pixels = np.sum(bin_img < 128)
    text_density = text_pixels / (h * w)

    # Line estimation
    horizontal_projection = np.sum(bin_img < 128, axis=1)
    lines = np.sum(horizontal_projection > 0.5 * np.max(horizontal_projection))

    # Noise (Canny)
    edges = cv2.Canny(img, 100, 200)
    noise_level = np.sum(edges) / 255 / (h * w)

    # Skew angle
    coords = np.column_stack(np.where(bin_img < 128))
    angle = 0.0
    if len(coords) > 0:
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        if angle < -45:
            angle += 90

    # Edge stats
    mean_len, var_len, mean_ang, var_ang = extract_edge_stats(edges)

    # HOG features
    hog_mean, hog_var = extract_hog_features(img)

    return [
        text_density,
        lines,
        noise_level,
        aspect_ratio,
        angle,
        mean_len,
        var_len,
        mean_ang,
        var_ang,
        hog_mean,
        hog_var,
    ]


def extract_doc_features(doc_path: str) -> List[float]:
    page_data = convert_doc_to_base64_images(doc_path)
    features = [extract_page_features(base64_to_cv2_image(b64)) for _, b64 in page_data]
    features = np.array(features)
    return features.mean(axis=0).tolist()


# ====================== Model Training and Inference ======================


class LLMScoreRegressor:
    def __init__(
        self,
        results_csv="tests/outputs/document_results.csv",
        doc_dir="examples/inputs/",
        model_dir="model_data",
    ):
        self.results_csv = results_csv
        self.doc_dir = doc_dir
        self.model = MultiOutputRegressor(
            RandomForestRegressor(n_estimators=100, random_state=42)
        )
        self.scaler = StandardScaler()
        self.models = []
        self.fitted = False
        self.model_dir = model_dir
        self.feature_path = os.path.join(model_dir, "features.npy")
        self.target_path = os.path.join(model_dir, "targets.npy")
        self.model_path = os.path.join(model_dir, "model.pkl")
        self.scaler_path = os.path.join(model_dir, "scaler.pkl")
        self.model_list_path = os.path.join(model_dir, "models.txt")
        os.makedirs(model_dir, exist_ok=True)

    def _prepare_data(self):
        print(self.results_csv)
        df = pd.read_csv(self.results_csv)

        self.models = sorted(df["model"].unique().tolist())
        with open(self.model_list_path, "w") as f:
            f.write("\n".join(self.models))

        grouped = df.groupby("Input File")

        X, Y = [], []
        for base_name, group in tqdm(grouped):
            path = glob(os.path.join(self.doc_dir, base_name + "*"))[0]
            features = extract_doc_features(path)
            scores = (
                group.set_index("model")["sequence_matcher"]
                .reindex(self.models)
                .fillna(0.0)
                .values
            )
            scores = (scores - scores.mean()) / scores.std()
            X.append(features)
            Y.append(scores)
        X, Y = np.array(X), np.array(Y)
        return X, Y

    def train(self):
        X, Y = self._prepare_data()
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, Y)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        np.save(self.feature_path, X)
        np.save(self.target_path, Y)
        self.fitted = True
        print("Model trained and saved.")

    def load(self):
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        with open(self.model_list_path) as f:
            self.models = [line.strip() for line in f.readlines()]
        self.fitted = True

    def predict_scores(self, doc_path: str) -> Dict[str, float]:
        if not self.fitted:
            self.load()
        features = extract_doc_features(doc_path)
        X_scaled = self.scaler.transform([features])
        scores = self.model.predict(X_scaled)[0]
        return dict(zip(self.models, scores))

    def rank_models(self, doc_path: str) -> List[Tuple[str, float]]:
        scores = self.predict_scores(doc_path)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def evaluate_leave_one_out(self) -> pd.DataFrame:
        print("Running Leave-One-Out Cross-Validation...")
        X, Y = self._prepare_data()
        n_docs = X.shape[0]
        all_predictions = []
        all_targets = []

        for i in range(n_docs):
            # Split into train/test
            X_train = np.delete(X, i, axis=0)
            Y_train = np.delete(Y, i, axis=0)
            X_test = X[i].reshape(1, -1)
            Y_test = Y[i]

            # Fit model on train split
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            model = MultiOutputRegressor(
                RandomForestRegressor(n_estimators=100, random_state=42)
            )
            model.fit(X_train_scaled, Y_train)

            # Predict on left-out doc
            Y_pred = model.predict(X_test_scaled)[0]
            all_predictions.append(Y_pred)
            all_targets.append(Y_test)

        predictions = np.array(all_predictions)
        targets = np.array(all_targets)

        # Compute mean absolute error per model
        errors = np.abs(predictions - targets)
        mae_per_model = errors.mean(axis=0)
        mean_mae = errors.mean()

        result_df = pd.DataFrame(
            {"model": self.models, "MAE": mae_per_model}
        ).sort_values(by="MAE")

        print("Leave-One-Out MAE per model:")
        print(result_df.to_string(index=False))
        print(f"Overall Mean MAE: {mean_mae:.4f}")
        return result_df


# ====================== Example Usage ======================

if __name__ == "__main__":
    model_dir = "model_data"
    selector = LLMScoreRegressor(model_dir=model_dir)
    selector.train()
    selector.evaluate_leave_one_out()

    test_doc = "examples/inputs/test_2.pdf"
    ranking = selector.rank_models(test_doc)
    print("Model Ranking:")
    for model, score in ranking:
        print(f"{model}: {score:.4f}")
