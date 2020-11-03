#!python3

from io import StringIO
import barcode
from barcode.writer import ImageWriter
import json
import requests
import shutil
import threading

ITEMS_JSON = 'items.json'
FOLDER_PATH = './ItemAttributes'

def main():
	with open(ITEMS_JSON, 'r', encoding='utf8') as f:
		items = json.load(f)

	for dpci in items:
		if not 'upc' in items[dpci]:
			continue
		upc = items[dpci]['upc']
		itemType = items[dpci]['type']
		if itemType == ' ':
			itemType = 'None'
		imageURL = items[dpci]['imageURL']
		filename = f'{itemType}_{dpci}_{upc}_image'
		SAVE_PATH = f'{FOLDER_PATH}/{filename}.jpg'

		t1 = threading.Thread(target=downloadImage, args=[imageURL, SAVE_PATH])
		t1.start()

		filename = f'{itemType}_{dpci}_{upc}'
		SAVE_PATH = f'{FOLDER_PATH}/{filename}'

		UPC = barcode.get_barcode_class('upc')
		upcObj = UPC(upc, writer=ImageWriter())
		fullname = upcObj.save(SAVE_PATH)
		fp = StringIO()


def downloadImage(imageURL, SAVE_PATH):
	response = requests.get(imageURL, stream=True)
	with open(SAVE_PATH, 'wb') as out_file:
	    shutil.copyfileobj(response.raw, out_file)
	del response

if __name__ == '__main__':
	main()
