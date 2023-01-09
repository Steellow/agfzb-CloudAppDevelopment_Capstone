from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}

    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)

    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/570d9ccc-0e4d-400b-a827-6c9e117b30cf/default/Get%20all%20dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = dealerships
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html')


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    return HttpResponse(get_dealer_reviews_from_cf(request, dealer_id))

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):


def add_review(request, dealer_id):
    user = request.user
    context = {}
    if user.is_authenticated:
        if request.method == "POST":
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year)

            new_payload = {}
            new_payload["review"] = payload

            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/zerodiversex_zerodiversex/dealerships/post-review.json"

            # Get dealers from the URL
            post_request(url, new_payload)
            return redirect('djangoapp:dealer_details', **{"dealername": dealername, "id": id})

            # url = "https://3dbc2a14.us-south.apigw.appdomain.cloud/postreview/api/review"
            # result = post_request(url, json_payload)
            # return HttpResponse(json_payload)

        elif request.method == "GET":
            models = list(
                CarModel.car_manager.all().filter(dealerid=dealer_id))
            context["cars"] = models
            context["dealer_id"] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)
