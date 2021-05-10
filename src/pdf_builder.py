import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

results_dir = '../Results'
pdf_filename = 'Barcodes.pdf'

def build(items):
	pdf_path = os.path.join(results_dir, pdf_filename)
	pdf_path = _get_valid_path(pdf_path)

	pdf_canvas = canvas.Canvas(pdf_path)
	x, y = 10, 700

	for item in items:
		pdf_canvas.setFont("Helvetica", 7)
		pdf_canvas.drawString(x + 1, y + 98, f'Name: {item["name"]}')
		pdf_canvas.drawString(x + 1, y + 90, f'{item["dpci"]}')
		pdf_canvas.drawImage(item['image_path'], x, y, 3*cm, 3*cm)
		x += 80
		pdf_canvas.drawImage(item['barcode_path'], x, y, 4*cm, 3*cm)
		x += 120

		if x > 600:
			x = 10
			y -= 125
		if y < 30:
			x = 10
			y = 700
			# end current page; next loop will write to a new page
			pdf_canvas.showPage()

	pdf_canvas.save()


def _get_valid_path(file_path):
    filename, ext = os.path.splitext(file_path)

    n = 1
    while os.path.isfile(file_path):
        file_path = f'{filename} ({n}){ext}'
        n += 1

    return file_path
