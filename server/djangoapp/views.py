# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import os
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...


from .restapis import get_request, post_review

@csrf_exempt
def get_dealers(request, state=None):
    endpoint = "fetchDealers" + ("/" + state if state else "")
    dealers = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealers or []})

@csrf_exempt
def get_cars(request):
    data_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "database", "data", "car_records.json"
    )
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            records = json.load(f).get("cars", [])

        unique_cars = {}
        for car in records:
            key = (car.get("make"), car.get("model"))
            if all(key) and key not in unique_cars:
                unique_cars[key] = {
                    "CarMake": key[0],
                    "CarModel": key[1]
                }

        return JsonResponse({
            "status": 200,
            "CarModels": list(unique_cars.values())
        })
    except (OSError, json.JSONDecodeError) as error:
        logger.exception("Unable to load car records: %s", error)
        return JsonResponse({"status": 500, "CarModels": []}, status=500)


@csrf_exempt
def getallcarmakes(request):
    result = get_cars(request)
    data = json.loads(result.content)
    return JsonResponse({
        "status": data["status"],
        "CarMakes": data["CarModels"]
    })


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        required = [
            "name", "dealership", "review", "purchase_date",
            "car_make", "car_model", "car_year"
        ]
        if any(data.get(field) in (None, "") for field in required):
            return JsonResponse(
                {"status": 400, "error": "All details are mandatory"},
                status=400
            )

        data["purchase"] = True
        saved = post_review(data)
        if saved is None:
            return JsonResponse(
                {"status": 500, "error": "Could not save review"},
                status=500
            )

        return JsonResponse({"status": 200, "review": saved})
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        return JsonResponse({"status": 400, "error": str(error)}, status=400)

@csrf_exempt
def get_dealer_details(request, dealer_id):
    dealer = get_request("fetchDealer/" + str(dealer_id))
    if isinstance(dealer, dict):
        dealer = [dealer]
    return JsonResponse({"status": 200, "dealer": dealer or []})

@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    reviews = get_request("fetchReviews/dealer/" + str(dealer_id))
    return JsonResponse({"status": 200, "reviews": reviews or []})
