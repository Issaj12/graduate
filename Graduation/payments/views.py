from django.shortcuts import render
from django.conf import settings
from .forms import PaymentForm
from .models import Transaction
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse
import json

# Initialize MpesaClient globally
mpesa_client = MpesaClient()


def initiate_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            if request.user.is_authenticated:
                transaction.user = request.user
            transaction.status = "Pending"
            transaction.save()

            phone_number = transaction.phone_number
            amount = transaction.amount

            print(f"Initiating STK Push: {phone_number} - {amount}")

            try:
                response = mpesa_client.stk_push(
                    phone_number=phone_number,
                    amount=amount,
                    account_reference="TestPayment",
                    transaction_desc="Payment for service",
                    callback_url=settings.MPESA_CALLBACK_URL
                )

                # Access MpesaResponse attributes directly
                print("STK Push response:", response)

                if getattr(response, "ResponseCode", None) == "0":
                    transaction.transaction_id = getattr(response, "CheckoutRequestID", "")
                    transaction.save()
                    return render(request, "payments/pending.html", {"transaction": transaction})
                else:
                    transaction.status = "Failed"
                    transaction.save()
                    error_message = getattr(response, "errorMessage", "Unknown error")
                    return render(request, "payments/failed.html", {"error": error_message})

            except Exception as e:
                print("Error initiating STK Push:", str(e))
                transaction.status = "Failed"
                transaction.save()
                return render(request, "payments/failed.html", {"error": str(e)})

    else:
        form = PaymentForm(user=request.user)

    return render(request, "payments/payment_form.html", {"form": form})


def daraja_callback(request):
    try:
        data = json.loads(request.body)
        callback_data = data.get("Body", {}).get("stkCallback", {})
        checkout_request_id = callback_data.get("CheckoutRequestID")
        result_code = callback_data.get("ResultCode")

        transaction = Transaction.objects.filter(transaction_id=checkout_request_id).first()

        if transaction:
            if result_code == 0:
                transaction.status = "Success"
            else:
                transaction.status = "Failed"
            transaction.save()

        return JsonResponse({"status": "ok"})
    except Exception as e:
        print("Error processing Daraja callback:", str(e))
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
