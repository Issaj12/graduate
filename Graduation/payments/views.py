from django.shortcuts import render
from django.conf import settings
from .forms import PaymentForm
from .models import Transaction
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

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
                    account_reference="Graduate sasa",
                    transaction_desc="Payment for service",
                    callback_url=settings.MPESA_CALLBACK_URL
                )

                # DEBUG (keep this)
                print("STK Push response:", response.__dict__)

                # ✅ CORRECT ATTRIBUTE NAME
                if response.response_code == "0":
                    transaction.transaction_id = response.checkout_request_id
                    transaction.merchant_request_id = response.merchant_request_id
                    transaction.status = "Pending"
                    transaction.save()

                    return render(
                        request,
                        "payments/pending.html",
                        {"transaction": transaction}
                    )

                else:
                    transaction.status = "Failed"
                    transaction.save()

                    return render(
                        request,
                        "payments/failed.html",
                        {
                            "error": response.response_description
                        }
                    )

            except Exception as e:
                print("Error initiating STK Push:", str(e))

                transaction.status = "Failed"
                transaction.save()

                return render(
                    request,
                    "payments/failed.html",
                    {"error": str(e)}
                )

    else:
        form = PaymentForm(user=request.user)
        
    context = {"form": form}
    return render(request, "payments/payment_form.html", context)




@csrf_exempt
def daraja_callback(request):
    try:
        data = json.loads(request.body)

        stk_callback = data.get("Body", {}).get("stkCallback", {})
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode")

        transaction = Transaction.objects.filter(
            transaction_id=checkout_request_id
        ).first()

        if transaction:
            if result_code == 0:
                transaction.status = "Success"
            else:
                transaction.status = "Failed"

            transaction.save()

        return JsonResponse({"status": "ok"})

    except Exception as e:
        print("Error processing Daraja callback:", str(e))
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=400
        )
