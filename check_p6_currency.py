import fitz

doc = fitz.open("original.pdf")
for page_num in range(len(doc)):
    text = doc[page_num].get_text()
    if "Sättel" in text:
        print(f"Page {page_num + 1}:")
        for line in text.split('\n'):
            if "Sättel" in line or "China" in line or "Export" in line:
                print(f"  {line.strip()}")
