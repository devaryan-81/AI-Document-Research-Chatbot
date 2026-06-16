## DOCUMENT PROCESSING

import fitz
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(filepath):
    """Returns list of dicts: {page, paragraph, text}"""
    doc = fitz.open(filepath)
    chunks = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if not text.strip():
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)
            
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para_num, para in enumerate(paragraphs, start=1):
            sentences = [s.strip() for s in para.split(". ") if s.strip()]
            for sent_num, sent in enumerate(sentences, start=1):
                chunks.append({
                    "page": page_num,
                    "paragraph": para_num,
                    "sentence": sent_num,
                    "text": sent
                })
    doc.close()
    return chunks

def extract_text_from_image(filepath):
    img = Image.open(filepath)
    text = pytesseract.image_to_string(img)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for para_num, para in enumerate(paragraphs, start=1):
        chunks.append({"page": 1, "paragraph": para_num, "sentence": 1, "text": para})
    return chunks