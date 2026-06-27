import os
import sys

def check_dependencies():
    try:
        import fitz
    except ImportError:
        print("[!] PyMuPDF (fitz) is not installed. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf"])
        import fitz
    
    try:
        from PIL import Image
    except ImportError:
        print("[!] Pillow is not installed. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image

def extract_all():
    import fitz
    from PIL import Image

    pdf_path = "original.pdf"
    if not os.path.exists(pdf_path):
        print(f"[!] Error: '{pdf_path}' not found in the current directory.")
        print("Please copy the original PDF file of the study guide into this folder and rename it to 'original.pdf'.")
        return

    os.makedirs("images", exist_ok=True)
    print("[+] Opening original.pdf...")
    doc = fitz.open(pdf_path)
    
    # Configuration of figures: (Abbildung name, page_number (0-indexed), crop_top_%, crop_bottom_%)
    # Pages correspond to the page numbering in the document (which might be 0-indexed here)
    figures = [
        ("abbildung_1", 7, 23, 77),   # Page 8: Woher Fahrräder kommen
        ("abbildung_2", 11, 20, 75),  # Page 12: Simple economic cycle
        ("abbildung_3", 16, 12, 45),  # Page 17: Supply curve
        ("abbildung_4", 17, 12, 45),  # Page 18: Demand curve
        ("abbildung_5", 18, 10, 45),  # Page 19: Equilibrium price
        ("abbildung_6", 20, 35, 90),  # Page 21: Market forms
        ("abbildung_7", 21, 40, 95),  # Page 22: Functions of money
        ("abbildung_8", 22, 50, 95),  # Page 23: Cash and deposit money
        ("abbildung_9", 25, 10, 42),  # Page 26: Why interest exists
        ("abbildung_10", 26, 10, 32), # Page 27: Fixed vs variable interest (top)
        ("abbildung_11", 26, 45, 90), # Page 27: Nominal vs effective interest (bottom)
        ("abbildung_12", 28, 30, 75), # Page 29: Causes of inflation
        ("abbildung_13", 31, 40, 80), # Page 32: Embedded economy
        ("abbildung_14", 37, 15, 75), # Page 38: Decoupling map
        ("abbildung_15", 38, 10, 60), # Page 39: Net-zero year map
        ("abbildung_16", 41, 15, 80), # Page 42: Planetary boundaries diagram
        ("abbildung_17", 44, 40, 90), # Page 45: Doughnut model deficits
        ("abbildung_18", 52, 45, 75), # Page 53: Legal forms
        ("abbildung_19", 61, 10, 35), # Page 62: External financing
        ("abbildung_20", 70, 50, 95), # Page 71: Marketing questions
        ("abbildung_21", 73, 20, 60), # Page 74: Marketing concept
        ("abbildung_22", 74, 55, 95), # Page 75: Market metrics
        ("abbildung_23", 75, 25, 50), # Page 76: Target groups (top)
        ("abbildung_24", 75, 55, 85), # Page 76: Phases of market (bottom)
        ("abbildung_25", 76, 60, 92), # Page 77: Product life cycle
        ("abbildung_26", 78, 10, 40), # Page 79: Product policy measures
        ("abbildung_27", 79, 5, 35),  # Page 80: Price setting factors
        ("abbildung_28", 83, 30, 75), # Page 84: Three dimensions of digitalisation
        ("abbildung_29", 86, 60, 95), # Page 87: IT use and value creation
        ("abbildung_30", 89, 10, 45), # Page 90: Ad forms
        ("abbildung_31", 90, 10, 30), # Page 91: Cookie choice
        ("abbildung_32", 90, 30, 90), # Page 91: Adobe pricing
        ("abbildung_33", 93, 50, 85), # Page 94: WWW platforms
        ("abbildung_34", 95, 65, 95), # Page 96: Business informatics interdisciplinarity
        ("abbildung_35", 96, 30, 85), # Page 97: Perspectives
        ("abbildung_36", 99, 10, 35), # Page 100: Information and application systems
        ("abbildung_37", 100, 25, 65) # Page 101: Components of information systems
    ]

    print("[+] Rendering and cropping illustrations...")
    for fig_name, page_num, top_pct, bottom_pct in figures:
        try:
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            
            # Save temp page image
            temp_path = f"images/temp_{fig_name}.png"
            pix.save(temp_path)
            
            # Crop image using Pillow
            with Image.open(temp_path) as img:
                width, height = img.size
                
                # Calculate pixel crop boundaries
                top = int(height * (top_pct / 100.0))
                bottom = int(height * (bottom_pct / 100.0))
                
                cropped_img = img.crop((0, top, width, bottom))
                cropped_img.save(f"images/{fig_name}.png")
            
            os.remove(temp_path)
            print(f"    [OK] Saved images/{fig_name}.png (Page {page_num + 1})")
        except Exception as e:
            print(f"    [FAIL] Failed to extract {fig_name}: {e}")
            
    print("[+] Extraction complete! Images are stored in 'images/' folder.")

if __name__ == "__main__":
    check_dependencies()
    extract_all()
