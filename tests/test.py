#!python3

import PyPDF2

with open('jan_list.pdf', 'rb') as fd:
    reader = PyPDF2.PdfFileReader(fd)
    print(reader.getPage(0).extractText())