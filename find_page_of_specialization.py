import fitz

doc = fitz.open("original.pdf")
for page_num in range(len(doc)):
    text = doc[page_num].get_text()
    if "Japan" in text or "Malaysi" in text or "Sättel" in text or "Sattel" in text or "Singapore" in text:
        print(f"Page {page_num + 1} has matches")
        # print first 500 chars
        print(text[:500])
        print("="*40)
