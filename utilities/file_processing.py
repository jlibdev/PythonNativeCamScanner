import os, mimetypes
import sys
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from datetime import date
import uuid

SAVE_PATH = os.path.join(os.path.expanduser("~"), "Documents", "CamScanner")

def resource_path(relative_path):
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS 
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def open_file(file_path):
    if os.path.exists(file_path):
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["xdg-open", file_path], check=True)
    else:
        print("File not found:", file_path)


def retrieve_img_files():
    # Construct paths
    image_camscanner_path = os.path.join(SAVE_PATH, "images")

    # Create folder if it doesn’t exist
    os.makedirs(image_camscanner_path, exist_ok=True)

    # Function to check if a file is a JPEG or PNG
    def is_image(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type in ["image/jpeg", "image/png"]

    # Retrieve all JPEG and PNG files
    img_files = [
        os.path.join(image_camscanner_path, f)
        for f in os.listdir(image_camscanner_path)
        if is_image(os.path.join(image_camscanner_path, f))
    ]

    return img_files 


def retrieve_pdf_files():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Construct paths
    pdf_camscanner_path = os.path.join(SAVE_PATH, "pdf")
    
    # Create folder if it doesn’t exist
    os.makedirs(pdf_camscanner_path, exist_ok=True)

    def is_pdf(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type == "application/pdf"

    pdf_files = [
        os.path.join(pdf_camscanner_path, f)
        for f in os.listdir(pdf_camscanner_path)
        if is_pdf(os.path.join(pdf_camscanner_path, f))
    ]

    return pdf_files


def export_to_pdf(image_list, output_pdf=os.path.join(SAVE_PATH, "pdf" , f"CamScam-{date.today()}-{str(uuid.uuid4())}.pdf")):
    if image_list:
        c = canvas.Canvas(output_pdf, pagesize=letter)
        pdf_width, pdf_height = letter

        for idx, img in enumerate(image_list):
            img = img.cv_image
            pil_img = Image.fromarray(img)

            temp_filename = f"temp_{idx}.jpg"
            pil_img.save(temp_filename)

    
            orig_width, orig_height = pil_img.size

            new_width = pdf_width
            new_height = (orig_height / orig_width) * new_width 

            if new_height > pdf_height:
                new_height = pdf_height
                new_width = (orig_width / orig_height) * new_height 

            y_position = (pdf_height - new_height) / 2  
            x_position = (pdf_width - new_width) / 2

            c.drawImage(temp_filename, x_position, y_position, width=new_width, height=new_height)
            c.showPage()

            os.remove(temp_filename)

        c.save()
        print(f"PDF saved as {output_pdf}")

    else:
       print("Error")


def export_to_img(image_list, img_type="png"):
    for i in range(len(image_list)):
            img = cv2.cvtColor(image_list[i].cv_img_orig,cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(SAVE_PATH, "images" , f"CamScam-{date.today()}-{str(uuid.uuid4())}.{img_type}") , img)

