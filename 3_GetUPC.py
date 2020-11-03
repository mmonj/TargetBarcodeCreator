#!python3

import json
import re
import requests
import pickle

ITEMS_JSON = 'items.json'
DPCI_RE = r'(\d\d\d-\d\d-\d\d\d\d)\s+(.+)'

JSON_DPCI_RE = r'\"dpci\":\"(\d\d\d-\d\d-\d\d\d\d)\",'
JSON_UPC_RE = r'\"upc\":\"(\d+)\",'
JSON_BASEURL_RE = r'\"base_url\":\"(http.+?)\",'
JSON_PRIMARY_RE = r'\"primary\":\"(GUEST.+?)\",'

# search with dpci
REQUESTS_URL1 = 'https://redsky.target.com/v2/plp/search/?channel=web&count=24&default_purchasability_filter=false&facet_recovery=false&isDLP=false&keyword='
REQUESTS_URL2 = '&offset=0&pageId=%2Fs%2F'
REQUESTS_URL3 = '&pricing_store_id=2380&scheduled_delivery_store_id=1344&visitorId=016F58ED8EC8020194F7BF5A4099DDF1&include_sponsored_search_v2=true&ppatok=AOxT33a&platform=desktop&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F79.0.3945.88+Safari%2F537.36&key=eb2551e4accc14f38cc42d32fbc2b2ea'

# search tcin
UPC_URL1 = 'https://redsky.target.com/v3/pdp/tcin/'
UPC_URL2 = '?excludes=taxonomy%2Cbulk_ship%2Cawesome_shop%2Cquestion_answer_statistics%2Crating_and_review_reviews%2Crating_and_review_statistics%2Cdeep_red_labels%2Cin_store_location&key=eb2551e4accc14f38cc42d32fbc2b2ea&pricing_store_id=2380&storeId=2380'

def main():
	items = getItems()

	for dpci in items:
		url = f'{REQUESTS_URL1}{dpci}{REQUESTS_URL2}{dpci}{REQUESTS_URL3}'

		source = requests.get(url).text
		itemData = json.loads(source)

		try:
			tcin = itemData['search_response']['items']['Item'][0]['tcin']
		except Exception as e:
			continue
		# url = 'https://target.com' + itemData['search_response']['items']['Item'][0]['url']

		items[dpci] = {**items[dpci], **{'tcin': tcin}}

	

	# with open(ITEMS_JSON, 'w', encoding='utf8') as f:
	# 	json.dump(items, f, indent=4)

	# with open(ITEMS_JSON, 'r', encoding='utf8') as f:
	# 	items = json.load(f)

	for dpci in items:
		if not 'tcin' in items[dpci]:
			continue

		tcin = items[dpci]['tcin']
		url = f'{UPC_URL1}{tcin}{UPC_URL2}'
		source = requests.get(url).text
		# itemData = json.loads(source)

		try:
			m_dpci = re.finditer(JSON_DPCI_RE, source)
			m_upc = re.finditer(JSON_UPC_RE, source)
			base_url  = re.search(JSON_BASEURL_RE, source).group(1)
			primary = re.search(JSON_PRIMARY_RE, source).group(1)
		except Exception as e:
			continue

		dpciList = []
		upcList = []
		for m in m_dpci:
			dpciList.append(m.group(1))

		for m in m_upc:
			upcList.append(m.group(1))

		if not len(dpciList) == len(upcList):
			continue

		imageURL = base_url + primary

		for i, _ in enumerate(dpciList):
			dpci = dpciList[i]
			upc = upcList[i]
			if dpci in items:
				items[dpci]  = {**items[dpci], **{'upc': upc, 'imageURL': imageURL}}

		# imageURL = itemData['product']['item']['enrichment']['images'][0]['base_url'] + itemData['product']['item']['enrichment']['images'][0]['primary']

		# try:
		# 	for item in itemData['product']['item']['child_items']:
		# 		upc = item['upc']
		# 		dpci = item['dpci']
		# 		items[dpci]  = {'type': items[dpci]['type'], 'upc': upc, 'imageURL': imageURL}
		# except Exception as e:
		# 	print('Error:', str(e))
		# 	print(url)
		# 	print()

	with open(ITEMS_JSON, 'w', encoding='utf8') as f:
		json.dump(items, f, indent=4)


def getItems():
	with open(ITEMS_JSON, 'r', encoding='utf8') as f:
		items = json.load(f)

	return items


if __name__ == '__main__':
	main()