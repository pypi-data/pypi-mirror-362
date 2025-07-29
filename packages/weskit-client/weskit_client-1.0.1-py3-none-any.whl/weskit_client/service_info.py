import pprint
from weskit_client.com import requests_to_json

pp = pprint.PrettyPrinter(indent=4)


def get_service_info(weskit_api_url):
    json = requests_to_json(url="{}/ga4gh/wes/v1/service-info".format(weskit_api_url), method="GET")
    pp.pprint(json)
