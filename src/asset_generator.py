import barcode
import os
import requests

from barcode.writer import ImageWriter

OUTPUT_FOLDER = '../_generated'


def generate_barcode(item):
    save_path = os.path.join(OUTPUT_FOLDER, item['upc'] + '-barcode')
    upc_barcode = barcode.get('upc', item['upc'], writer=ImageWriter())
    output_path = upc_barcode.save(save_path)

    item['barcode_path'] = output_path


def download_image(item):
    save_path = os.path.join(OUTPUT_FOLDER, item['upc'] + '-item_image' + '.png')

    resp = requests.get(item['image_url'], stream=True)
    with open(save_path, "wb") as fd:
        fd.write(resp.content)

    item['image_path'] = save_path
