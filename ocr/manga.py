from manga_ocr import MangaOcr

class MangaAnalyzer:
    def __init__(self):
        self.mocr = MangaOcr()

    def predict(self, image_path):
        return self.mocr(image_path)