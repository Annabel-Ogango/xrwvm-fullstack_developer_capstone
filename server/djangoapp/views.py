import logging
import json
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
#from .restapis import get_request, analyze_review_sentiments, post_review
from .restapis import post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exists = False
    try:
        User.objects.get(username=username)
        username_exists = True
    except Exception as e:
        logger.debug("{} is new user".format(username))
        print(e)

    if not username_exists:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        from .populate import initiate
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


def get_dealer_reviews(request, dealer_id):
    mock_reviews = [
        {
            "name": "Annabel",
            "dealership": dealer_id,
            "review": "I highly recommend this dealership! Their customer service is also top notch!",
            "purchase": True,
            "purchase_date": "30-Mar-2026",
            "car_make": "Kia",
            "car_model": "Cerato",
            "car_year": 2020,
            "sentiment": "positive"
        }
    ]
    return JsonResponse({"status": 200, "reviews": mock_reviews})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            print(e)
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 400, "message": "Bad Request"})
