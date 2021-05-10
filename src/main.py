#!python3

import os
import subprocess

import data_parser
import site_parser
import asset_generator
import pdf_builder

def main():
	print('Parsing item dump')
	items = data_parser.parse_item_dump()
	pulled_items = []

	print('Parsing site for item data')
	for i, item in enumerate(items):
		print(f'  > Pulling item data for {item["dpci"]}  ({i + 1}/{len(items)})')
		pulled_data = site_parser.pull_item_data(item)
		if pulled_data:
			item.update(**pulled_data)
			pulled_items.append(item)

	# _make_item_names_printable(pulled_items)

	print('Getting barcodes and images')
	for item in pulled_items:
		asset_generator.generate_barcode(item)
		asset_generator.download_image(item)

	print('Building pdf')
	pdf_builder.build(pulled_items)


# def _make_item_names_printable(items):
# 	pass



if __name__ == '__main__':
	main()
