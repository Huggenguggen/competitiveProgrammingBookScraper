# online judge links bring user to pdf so will need OCR.

import requests
import PyPDF2

byte_to_char = {
    "\x00": "-",
    "\x14": "<=",
}

def onlineJudgeExtract(url: str) -> list:
    # format of the list: [Number, Title, Description, Input, Output]
    response = requests.get(url)
    # download the pdf
    with open('temp.pdf', 'wb') as file:
        file.write(response.content)
    
    # Read the PDF and extract the text
    pdf_file = open('temp.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    Num = Title = Desc = Input = Output =""
    red_text_color = (1, 0, 0)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        content = page.extract_text()
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                subtype = annotation.get('/Subtype')

                if subtype and subtype == '/Highlight':
                    color = annotation.get('/C')
                    if color == red_text_color:
                        text += '\n'  # Add newline before red header
                        break

        text += content
        
        pdf_file.close()
        
        with open('temp.pdf', 'rb') as file:
            file.close()
        return [text]

if __name__ == "__main__":
    test_url = "https://onlinejudge.org/external/100/10071.pdf"
    # 10071, Should be Back to High School Physics
    res = onlineJudgeExtract(test_url)
    for key in byte_to_char:
        res[0].replace(key, byte_to_char[key])
    print("TEXT", res[0])
    with open('temp.txt', 'w+') as file:
        file.write(res[0])
    print("SUCCESS")