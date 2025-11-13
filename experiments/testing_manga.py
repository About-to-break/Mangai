from ocr.manga import MangaAnalyzer

ocr_unit = MangaAnalyzer()

print(ocr_unit.predict("test.png"))