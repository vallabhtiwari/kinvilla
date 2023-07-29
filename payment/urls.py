from django.urls import path
from .views import request_payment, handle_payment

app_name = "payment"
urlpatterns = [
    path("request-payment/", request_payment, name="request-payment"),
    path("handle-payment/", handle_payment, name="handle-payment"),
]
