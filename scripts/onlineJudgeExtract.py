# online judge links bring user to pdf so will need OCR.
import pytesseract
from pdf2image import convert_from_path
import requests
import PyPDF2
from pathlib import Path

def onlineJudgeExtract(url: str) -> list:
    # format of the list: [Number, Title, Description, Input, Output]
    response = requests.get(url)
    # download the pdf
    p = Path(__file__).with_name('temp.pdf')
    with p.open('wb') as file:
        file.write(response.content)
    
    # Read the PDF and extract the text
    images = convert_from_path("temp.pdf", poppler_path=r'C:\Program Files\poppler-23.05.0\Library\bin')
    text = ""
    for image in images:
        text = pytesseract.image_to_string(image, config='--psm 6')
        extracted_text += text
    
    with open('temp.pdf', 'rb') as file:
        file.close()
    return [text]

if __name__ == "__main__":
    test_url = "https://onlinejudge.org/external/100/10071.pdf"
    # 10071, Should be Back to High School Physics
    res = onlineJudgeExtract(test_url)
    print("TEXT", res[0])
    p = Path(__file__).with_name('temp.txt')
    with p.open('w+') as file:
        file.write(res[0])
    print("SUCCESS")