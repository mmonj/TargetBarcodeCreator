import json
import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

ATTRIBUTES_RE = r'(.+?)_(.+?)_(\d{12})'
CATEGORIES = ['Ring', 'Earring', 'Bracelet', 'Necklace', 'Extenders']
ITEMATTRIBUTES_PATH = './ItemAttributes/'
ITEMS_JSON = 'items.json'

def main():
	with open(ITEMS_JSON, 'r', encoding='utf8') as f:
		items = json.load(f)

	barcodeFiles = [f for f in os.listdir(ITEMATTRIBUTES_PATH) if f.endswith('.png')]
	sortFiles(barcodeFiles)
	c = canvas.Canvas('AND Core Barcodes.pdf')

	x, y = 10, 700
	for barcodeFile in barcodeFiles:
		c.setFont("Helvetica", 7)
		
		itemType = re.search(ATTRIBUTES_RE, barcodeFile).group(1)
		dpci = re.search(ATTRIBUTES_RE, barcodeFile).group(2)
		setDate = items[dpci]['set_date']

		imageFile = ITEMATTRIBUTES_PATH + os.path.splitext(barcodeFile)[0] + '_image.jpg'
		barcodeFile = ITEMATTRIBUTES_PATH + barcodeFile

		c.drawString(x + 1, y + 98, f'Set date: {setDate}')
		c.drawString(x + 1, y + 90, f'{itemType}: {dpci}')
		c.drawImage(imageFile, x, y, 3*cm, 3*cm)
		x += 80
		c.drawImage(barcodeFile, x, y, 4*cm, 3*cm)
		x += 120
		if x > 600:
			x, y = 10, y - 125
		if y < 30:
			x, y = 10, 700
			c.showPage()

	c.save()


def sortFiles(files):
	temp = []

	for category in CATEGORIES:
		for file in files:
			if category in file:
				temp.append(file)

	for file in files:
		cat = re.search(ATTRIBUTES_RE, file).group(1)
		if cat not in CATEGORIES:
			temp.append(file)

	files[:] = temp


if __name__ == '__main__':
	main()


# from reportlab.pdfgen import canvas

# x, y = 10, 730
# c.drawString(x + 1, y + 90, "the dpci here")
# c.drawImage('1_215-03-8527_492150385272_image.jpg', x, y, 3*cm, 3*cm)
# c.save()