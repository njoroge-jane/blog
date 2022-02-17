from .models import Quotes
import urllib.request, json

#getting the quotes base url
base_url = None

def configure_request(app):
    global base_url

    base_url = app.config['QUOTE_BASE_URL']

def random():
    get_random_quote = base_url

    with urllib.request.urlopen(get_random_quote) as url:
        get_random_data = url.read()
        get_random_response = json.loads(get_random_data)

        random_results = None

        if get_random_response:
            random_results_list = get_random_response
            random_results = process_results(random_results_list)

        return random_results   

def process_results(result_list):
    author = result_list.get('author')
    quote = result_list.get('quote')

    random_quote_object = Quotes(author, quote)

    return random_quote_object