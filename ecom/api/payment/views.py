from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree

# Create your views here.

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='pjggx4y7zqfb6scz',
    public_key='frhj4cd4y93gjgcf',
    private_key='13b81c0da2168661a24d0d01c6e5b43b'
  )
)

def validate_user_session(id, token):
    userModel = get_user_model()

    try:
        user = userModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False    
    except userModel.DoesNotExist:
        return False

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session, please login again !'})
    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success':True})   

@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session, please login again !'})

    nonce_from_the_client = request.POST["paymentMethodNonce"]  
    amount_from_the_client = request.POST["amount"]

    result = gateway.transaction.sale({
    "amount": amount_from_the_client,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True}
    })  

    if result.is_success:
        return JsonResponse({'success':result.is_success,'transaction':{'id':result.transaction.id,'amount':result.transaction.amount}})
    else:
        return JsonResponse({'error':True, 'success':False})    

