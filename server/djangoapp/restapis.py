import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # url = url+"?dealerId="+str(dealer_id)
    json_result = get_request(
        "https://eu-gb.functions.appdomain.cloud/api/v1/web/570d9ccc-0e4d-400b-a827-6c9e117b30cf/default/Get%20all%20reviews%20for%20a%20dealership?dealerId=15")
    if json_result:
        print("json_result: " + json_result)
        docs = json_result["docs"]
        for doc in docs:
            review = DealerReview(dealership=doc["dealership"], name=doc["name"], purchase=doc["purchase"],
                                  review=doc["review"], purchase_date=doc["purchase_date"], car_make=doc["car_make"],
                                  car_model=doc["car_model"], car_year=doc["car_year"], id=doc["id"])
            results.append(review)


def analyze_review_sentiments(dealerreview):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    apikey = "x7Hd1XwXvqoDndE0RF7q-hAAMisqciZUAmcNLNC-oTtC"
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/cb74a6f3-5636-4269-a0c6-b9f77e4168b2"

    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    text = dealerreview

    try:
        response = natural_language_understanding.analyze(text=text,
                                                          features=Features(sentiment=SentimentOptions())).get_result()
        a = response["sentiment"]
        a = a["document"]
        a = a["label"]
    except:
        a = "neutral"

    return a
