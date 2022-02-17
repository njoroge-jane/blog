from .models import Quotes
import urllib.request, json

#getting the quotes base url
base_url = None

def configure_request(app):
    global base_url

    base_url = app.config['QUOTE_BASE_URL']

def quote():
    get_quote = base_url

    with urllib.request.urlopen(get_quote) as url:
        get_data = url.read()
        get_response = json.loads(get_data)

        quote_results = None

        if get_response:
            results_list = get_response
            qoute_results = process_results(results_list)

        return quote_results   

def process_results(result_list):
    author = result_list.get('author')
    quote = result_list.get('quote')

    quote_object = Quotes(author, quote)

    return quote_object