import onnxruntime as ort
import numpy as np

class AnomalyDetector:
    def __init__(self, model_path='model.onnx'):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features):
        input_data = np.array(features, dtype=np.float32).reshape(1, -1)
        return self.session.run(None, {self.input_name: input_data})[0][0]