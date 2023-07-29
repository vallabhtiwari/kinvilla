from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Payment
from user.models import Resident
from room.models import Room
import razorpay

# Create your views here.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)
razorpay_client.set_app_details({"title": "KinVilla", "version": "0.0"})


def request_payment(request):
    resident = Resident.objects.get(resident_id=request.session.get("resident_id"))
    room = Room.objects.get(room_number=request.session.get("room_number"))

    amount = float(room.rent)
    old_payments = Payment.objects.filter(payer=resident)
    if not old_payments:
        amount *= 2

    payment_obj = Payment.objects.create(
        payer=resident,
        room=room,
        date_of_payment=timezone.localtime(timezone.now()),
        amount=amount,
    )
    # amount for razorpay should be in paise
    amount = int(amount * 100)
    order = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"{payment_obj.payment_id}",
        "partial_payment": False,
        "payment_capture": "0",
    }
    payment = razorpay_client.order.create(order)
    razorpay_order_id = payment["id"]
    callback_url = (
        "http://" + str(get_current_site(request)) + "/payment/handle-payment/"
    )

    context = {}
    context["razorpay_order_id"] = razorpay_order_id
    context["razorpay_key_id"] = settings.RAZORPAY_KEY_ID
    context["razorpay_amount"] = amount
    context["currency"] = "INR"
    context["callback_url"] = callback_url
    context["description"] = "Booking payment"
    payment_obj.razorpay_order_id = razorpay_order_id
    payment_obj.save()

    try:
        del request.session["resident_id"]
        del request.session["room_number"]
    except:
        pass

    return render(request, "payment/request_payment.html", context=context)


@csrf_exempt
def handle_payment(request):
    context = {}
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            razorpay_signature = request.POST.get("razorpay_signature", "")
            # make parameters dictionary to verify
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
            # updating the Payment info in the database
            payment_obj = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment_obj.razorpay_payment_id = razorpay_payment_id
            payment_obj.razorpay_signature = razorpay_signature
            payment_obj.save()
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                try:
                    # capture the payment
                    razorpay_client.payment.capture(
                        razorpay_payment_id, int(payment_obj.amount) * 100
                    )
                    # render success page on successful caputre of payment
                    payment_obj.status = "1"
                    payment_obj.save()

                    payer = payment_obj.payer
                    room = payment_obj.room
                    old_payments = (
                        Payment.objects.filter(payer=payer)
                        .filter(room=room)
                        .exclude(payment_id=payment_obj.payment_id)
                    )

                    if not old_payments:
                        context["room_number"] = room.room_number
                        # payment successful page with redirect to make booking
                        context["redirect_url"] = reverse(
                            "room:room-detail",
                            args=[room.floor, room.room_number],
                        )
                    else:
                        # payment successful page with redirect to homepage/profile
                        context["redirect_url"] = reverse(
                            "user:user-detail", args=[payer.resident_id]
                        )

                    return render(request, "payment/payment_successful.html", context)
                except:
                    # if there is an error while capturing payment.
                    print("PPPPPPPPPPPPPPPPPPPPPP")
                    payment_obj.status = "2"
                    payment_obj.save()
                    # payment failed page
                    return render(request, "payment/payment_failed.html", context)
            else:
                # if signature verification fails.
                print("QQQQQQQQQQQQQQQQQQQQQQ")
                payment_obj.status = "0"
                payment_obj.save()
                # payment failed page
                return render(request, "payment/payment_failed.html", context)
        except:
            # if we don't find the required parameters in POST data
            print("RRRRRRRRRRRRRRRRRRRRRRRRR")
            return render(request, "payment/payment_failed.html", context)
    else:
        # if other than POST request is made.
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        return HttpResponseBadRequest()
