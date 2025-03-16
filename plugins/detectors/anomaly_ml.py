"""
Moduł wykrywania anomalii z wykorzystaniem Isolation Forest i cache’owaniem.
"""

from functools import lru_cache
import numpy as np
from sklearn.ensemble import IsolationForest
from core.utils.logger import CyberLogger
from typing import List, Dict

class AnomalyDetector:
    def __init__(self):
        self._model: Optional[IsolationForest] = None
        self._logger = CyberLogger(__name__)
        self._trained: bool = False

    @staticmethod
    @lru_cache(maxsize=1024)
    def _hashable_features(features: tuple) -> np.ndarray:
        """Konwersja cech do formy hashable dla cache."""
        return np.array(features)

    async def train_model(self, training_data: List[Dict]) -> None:
        """Trenowanie modelu na historycznych danych."""
        X = self._preprocess_data(training_data)
        self._model = IsolationForest(
            n_estimators=100,
            contamination=0.01,
            random_state=42
        )
        self._model.fit(X)
        self._trained = True
        self._logger.info(f"Model ML wytrenowany na {len(X)} próbek")

    async def detect(self, packet_features: Dict) -> float:
        """Asynchroniczna detekcja anomalii."""
        if not self._trained:
            raise RuntimeError("Model nie został wytrenowany")
        
        X = self._preprocess_data([packet_features])
        anomaly_score = self._model.decision_function(X)[0]
        return float(anomaly_score)

    def _preprocess_data(self, raw_data: List[Dict]) -> np.ndarray:
        """Przygotowanie danych dla modelu ML."""
        features = [self._extract_features(packet) for packet in raw_data]
        return self._hashable_features(tuple(map(tuple, features)))