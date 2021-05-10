import json
import requests
from string import Template

DPCI_URL_TEMPLATE = Template('https://redsky.target.com/v2/plp/search/?channel=web&count=24&default_purchasability_filter=false&facet_recovery=false&isDLP=false\
&keyword=$DPCI&offset=0&pageId=%2Fs%2F$DPCI&pricing_store_id=1344&scheduled_delivery_store_id=1344&visitorId=1\
&include_sponsored_search_v2=true&ppatok=AOxT33a&platform=desktop&key=e')

TCIN_SEARCH_TEMPLATE = Template('https://redsky.target.com/v3/pdp/tcin/$TCIN?excludes=taxonomy%2Cbulk_ship%2Cawesome_shop%2Cquestion_answer_statistics%2Crating_and_review_reviews%2Crating_and_review_statistics%2Cdeep_red_labels%2Cin_store_location&key=e&pricing_store_id=1344&storeId=1344')

def pull_item_data(item):
	pulled_data = _get_data_from_dpci(item)
	if pulled_data is None:
		return None

	if pulled_data['upc'] is None:
		pulled_data = _get_data_from_tcin(item, pulled_data['tcin'])

	return pulled_data


def _get_data_from_dpci(item):
	url = DPCI_URL_TEMPLATE.safe_substitute(DPCI=item['dpci'])
	resp = requests.get(url)
	resp_json = resp.json()

	item_results = resp_json['search_response']['items']['Item']
	if not item_results:
		return None

	data = {}
	if item['name'] is None:
		data['name'] = item_results[0].get('title')
	data['upc'] = item_results[0].get('upc')
	data['tcin'] = item_results[0].get('tcin')
	data['image_url'] = item_results[0]['images'][0]['base_url'] + item_results[0]['images'][0]['primary']

	return data


def _get_data_from_tcin(item, tcin):
	url = TCIN_SEARCH_TEMPLATE.safe_substitute(TCIN=tcin)
	resp = requests.get(url)
	resp_json = resp.json()

	resp_items = resp_json['product']['item']['child_items']
	for resp_item in resp_items:
		if resp_item['dpci'] == item['dpci']:
			return _get_data_attributes(item, resp_item)
	return None

def _get_data_attributes(item, resp_item):
	data = {}
	if item['name'] is None:
		data['name'] = resp_item['product_description']['title']
	data['upc'] = resp_item['upc']

	image_data = resp_item['enrichment']['images'][0]
	data['image_url'] = image_data['base_url'] + image_data['primary']

	return data
