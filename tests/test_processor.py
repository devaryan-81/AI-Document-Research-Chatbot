import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processor import extract_text_from_pdf, extract_text_from_image

print("========= Testing PDF extraction =========")
chunks = extract_text_from_pdf("Document Research Chatbot/tests/sample files/final_resume.pdf")
print(f"Total chunks : {len(chunks)}")
for c in chunks[:5]:
    print(c)
    
print("\n=== Testing Image OCR extraction ===")
chunks_img = extract_text_from_image("Document Research Chatbot/tests/sample files/Screenshot 2025-06-05 153022.png")
print(f"Total chunks: {len(chunks_img)}")
for c in chunks_img[:5]:
    print(c)