import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def requests_to_json(url, method, verify=False, headers=None, data=None):
    try:
        with open(".weskit_access_key", 'r') as file:
            access_token = file.read()
            headers = dict(Authorization="Bearer " + access_token)
    except FileNotFoundError:
        headers = None
    try:
        if method.upper() == 'GET':
            response = requests.get(url, verify=verify, headers=headers, data=data)
        elif method.upper() == 'POST':
            response = requests.post(url, verify=verify, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            print(f"Unauthorized (401) error when calling '{url}'. Please check your access token.", file=sys.stderr)
        else:
            print(f"Request to '{url}' returns status code {response.status_code}.", file=sys.stderr)
            print(response.text, file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Network error occurred while calling '{url}'", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"Timeout error occurred while calling '{url}'", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}", file=sys.stderr)
        sys.exit(1)
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}", file=sys.stderr)
        sys.exit(1)
