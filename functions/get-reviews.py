from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

def main(dict):
    response = "{}"
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict['COUCH_URL'])
        statusCode = 200

        if ('__ow_method' in dict) and (dict['__ow_method']=="post"):
            post = dict #Ignore, not needed .loads(dict['__ow_body'])
            is_post = True
        else:
            is_post = False

        if is_post:
            review = {
                "name": post["name"],
                "review": post["review"],
                "car_make": post["car_make"],
                "car_model": post["car_model"],
                "purchase": post["purchase"],
                "name": post["name"],
                "dealership": post["dealership"]
            }
            if "purchase_date" in post:
                review["review"]["purchase_date"] = post["purchase_date"]
            """
            Sample input for insert:
            {
                "review": 
                    {
                        "id": 1114,
                        "name": "Upkar Lidder",
                        "dealership": 15,
                        "review": "Great service!",
                        "purchase": false,
                        "another": "field",
                        "purchase_date": "02/16/2021",
                        "car_make": "Audi",
                        "car_model": "Car",
                        "car_year": 2021
                    }
                }
            """
            service.post_document('reviews',review)
            response="Inserted/Updated Review: "+str(review)
        else:
            if 'dealerId' in dict:
                response = service.post_find(
                  db='reviews',
                  selector={'dealership': {'$eq': int(dict['dealerId'])}},
                ).get_result()
                if len(response["docs"])==0:
                    statusCode = 404
            else:
                response = service.post_find(
                  db='reviews',
                  selector={'id': {'$gt':0}},
                ).get_result()
    except Exception as e:
        response = {'error': str(e), 'request': dict}
        statusCode = 500

    return {"body": {"result":response, "statusCode": statusCode}}
