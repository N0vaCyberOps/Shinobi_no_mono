"""
Moduł wykrywania anomalii z wykorzystaniem Isolation Forest.
Integracja z asynchronicznym pipeline'em danych.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from core.utils.logger import CyberLogger
from typing import List, Dict

class AnomalyDetector:
    def __init__(self):
        self._model: IsolationForest = None
        self._logger = CyberLogger(__name__)
        self._features: List[Dict] = []
        self._trained: bool = False

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
        self._logger.info("Model ML wytrenowany na %d próbek", len(X))

    async def detect(self, packet_features: Dict) -> float:
        """Asynchroniczna detekcja anomalii."""
        if not self._trained:
            raise RuntimeError("Model nie został wytrenowany")
        
        X = self._preprocess_data([packet_features])
        anomaly_score = self._model.decision_function(X)[0]
        return float(anomaly_score)

    def _preprocess_data(self, raw_data: List[Dict]) -> np.ndarray:
        """Przygotowanie danych dla modelu ML."""
        # Ekstrakcja kluczowych cech pakietów
        features = []
        for entry in raw_data:
            features.append([
                entry.get("packet_size", 0),
                entry.get("protocol_type", 0),
                entry.get("entropy", 0),
                entry.get("response_time", 0)
            ])
        return np.array(features)
