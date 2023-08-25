from PyPDF2 import PdfReader

def check_prerequisites(target, courses):
    prerequisites = []
    for course in courses:
        if course == target :
            print("blahblah")
            #prerequisites = 
    return prerequisites

pdf_file = open('example.pdf', 'rb')

reader = PdfReader(pdf_file)
  
page = reader.pages[0]
  
text = page.extract_text()

print(text)

pdf_file.close()