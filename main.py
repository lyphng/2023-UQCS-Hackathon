from PyPDF2 import PdfReader
import json

def check_prerequisites(target, courses):
    prerequisites = []
    for course in courses:
        if course == target :
            print("blahblah")
            #prerequisites = 
    return prerequisites

def read_pdf_page(file_name, page_number):

    pdf_file = open(file_name, 'rb')

    reader = PdfReader(pdf_file)
    
    page = reader.pages[page_number]
    
    text = page.extract_text()
    pdf_file.close()

    return text


json_file = open('course_data.json', "r")
data = json.load(json_file)
for line in data['courses']:
    if line['course'] == 'CSSE2310':
        print(line)
json_file.close()

#Reading line by line so attributes can be properly filtered
# pdf_file = open("example.pdf",'rb')
    
# reader = PdfReader(pdf_file)
    
# pages = len(reader.pages)

# for i in range(pages):

#         page = reader.pages[i]

#         print("Page No: ", i + 1)

#         text = page.extract_text().split("\n")
#         for i in range(len(text)):
#             print("Line Number : {i} - {text} \n\n".format(i = i, text = text[i].split("     ")))
#                 #print("Line Number : {i} - {text} \n\n".format(i = i, text = text[i]))
#         print()


#pdf_file.close()
