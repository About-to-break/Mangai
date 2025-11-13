from paddleocr import PaddleOCRVL

class PaddleVLAnalyzer:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self._init_model()

    def _init_model(self):
        self.ocr_vl = PaddleOCRVL(**self.config)

    def update_config(self, **kwargs):
        self.config.update(kwargs)
        self._init_model()

    def predict(self, image_path):
        return self.ocr_vl.predict(image_path)



