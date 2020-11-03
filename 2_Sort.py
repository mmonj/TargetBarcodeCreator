#!python3

import json
import re

ATTRIBUTES_RE = r'(.+?) (\d\d?/\d\d?/\d\d\d\d) (.+\d) (.+)'
WANTED_ITEM_RE = r'^AND Core'

UNSORTED_FILENAME = 'dump.txt'
ITEMS_JSON = 'items.json'
TYPE_LIST = ['Ring', 'Earring', 'Bracelet', 'Necklace', 'Extenders', 'Backs']

def main():
	with open(UNSORTED_FILENAME, 'r', encoding='utf8') as f:
		items = f.read()
	items = items.split('\n')

	getANDitems(items)
	itemsDict = {}

	for item in items:
		m = re.search(ATTRIBUTES_RE, item)
		setDate = m.group(2)
		dpci = m.group(3)
		itemType = m.group(4)
		if itemType == 'Earring':
			itemType = 'Earrings'

		itemsDict[dpci] = {'set_date': setDate, 'type': itemType}


	with open(ITEMS_JSON, 'w', encoding='utf8') as f:
		json.dump(itemsDict, f, indent=4)





	# for itemType in TYPE_LIST:
	# 	for item in contents:
	# 		if itemType in item:
	# 			items.append(item)

	# for item in contents:
	# 	if otherItem(item):
	# 		items.append(item)

	# for i, item in enumerate(items):
	# 	attributes = []
	# 	matches = re.finditer(ATTRIBUTES_RE, item)
	# 	for match in matches:
	# 		attributes.append(match.group(1))

	# 	while len(attributes[0]) < 29:
	# 		attributes[0] = attributes[0] + ' '

	# 	while len(attributes[1]) < 19:
	# 		attributes[1] = attributes[1] + ' '

	# 	while len(attributes[2]) < 21:
	# 		attributes[2] = attributes[2] + ' '

	# 	items[i] = ''.join(attributes)


	# items = '\n'.join(items)

	# with open(SORTED_FILENAME, 'w', encoding='utf8') as f:
	# 	f.write(items)

def getANDitems(contents):
	temp = []
	for item in contents:
		if 'Program Set By Date Item # Section #' in item:
			item = item.replace('Program Set By Date Item # Section #', '')
		if re.match(WANTED_ITEM_RE, item):
			temp.append(item)
	contents[:] = temp


def otherItem(item):
	for itemType in TYPE_LIST:
		if itemType in item:
			return False
	return True


if __name__ == '__main__':
	main()