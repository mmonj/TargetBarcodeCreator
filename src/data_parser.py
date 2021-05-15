import re

ITEM_DUMP = '_item_dump.txt'

# items which to extract from item_dumps.txt and add to json
WANTED_ITEMS_RE = r'^(AND.*?)( *Program Set by.*)?$'
ITEM_ATTRIBUTES_RE = r'(.*?) (\d+/\d+/\d+) (\d{3}-\d{2}-\d{4}) ?(.*)?'
DPCI_RE = r'\b\d{3}-\d{2}-\d{4}\b'


# parse txt file that is consistently formatted
def parse_item_paste():
	with open(ITEM_DUMP, 'r', encoding='utf8') as fd:
		contents = fd.read()

	info_list = _get_and_items(contents)
	items = _build_dict(info_list)

	return items


# parse txt file with DPCIs scattered around
def parse_item_dump():
	with open(ITEM_DUMP, 'r', encoding='utf8') as fd:
		contents = fd.read()

	matches = re.finditer(DPCI_RE, contents, re.MULTILINE)
	dpcis = []

	for match in matches:
		if match.group() not in dpcis:
			dpcis.append(match.group())

	items = []
	for dpci in dpcis:
		temp = {'name': None, 'dpci': dpci}
		items.append(temp)

	return items


def _get_and_items(contents):
	info_list = []
	matches = re.finditer(WANTED_ITEMS_RE, contents, re.IGNORECASE | re.MULTILINE)

	for match in matches:
		info_list.append(match.group(1))

	return info_list


def _build_dict(info_list):
	items = []
	for item in info_list:
		match = re.search(ITEM_ATTRIBUTES_RE, item)
		if not match:
			continue

		data = {
			'name': match.group(1), 
			'type': match.group(4), 
			'set_date': match.group(2), 
			'dpci': match.group(3)
		}

		items.append(data)

	return items
