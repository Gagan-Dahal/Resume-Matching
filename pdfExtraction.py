import fitz
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []

    for page in doc:
        text = page.get_text().strip()

        if text:
            full_text.append(text)
        else:
            print(f"Page {page.number + 1} is image-based, running OCR...")
            pix = page.get_pixmap(dpi=700)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            full_text.append(ocr_text)

    return "\n".join(full_text)


text = extract_text_from_pdf("11.pdf")

with open("test.txt", "w") as fp:
    fp.write(text)
    print("Text written successfully")
