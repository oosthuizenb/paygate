from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import get_language

from .forms import ProcessPaymentForm
from ..core import BasicProvider
from .utils import calculate_md5, post_payment, validate_checksum


class PaygateProvider(BasicProvider):

    _method = 'post'

    def __init__(self, paygate_id=10011072130, **kwargs):
        self.paygate_id =  paygate_id # Test ID
        self.endpoint = 'https://secure.paygate.co.za/payweb3/process.trans'
        super(PaygateProvider, self).__init__(**kwargs)

    def get_action(self, payment):
        return self.endpoint

    def get_hidden_fields(self, payment):
        # Step 1 send transaction data to Paygate
        data = {
            'paygate_id'        : self.paygate_id,
            'reference'         : payment.id,
            'amount'            : trunc(payment.total * 100),
            'currency'          : 'ZAR',
            'return_url'        : self.get_return_url(payment),
            'transaction_date'  : payment.created,
            'locale'            : get_language(),
            'country'           : 'ZAF',
            'email'             : payment.billing_email,
            'notify_url'        : payment.get_process_url(),
        }
        data['checksum'] = calculate_md5(data)
        data['url'] = 'https://secure.paygate.co.za/payweb3/initiate.trans'
        # Post data and validate response data
        hash_valid, response_data = post_payment(data)
        if not hash_valid 
            return HttpResponseForbidden('FAILED')
        
        return response_data

def process_data(self, payment, request):
    if request.method == "POST":
        token = kwargs.get('token')
        payment = Payment.objects.get(token=token)
        for k,v in request.POST.items():
            print(k,v)
        if request.POST.get('AUTH_CODE'):
            print("Notified")
            payment.status = "NOTIFIED"
            return HttpResponse("OK")

    # if request.POST['AUTH_CODE']: # Step 4
    #     hash_dict = request.POST
    #     hash_dict.pop('checksum')
    #     md5_hash = calculate_md5(hash_dict)
    #     if md5_hash != request.POST['CHECKSUM']
    #         return HttpResponseForbidden('FAILED')
    #     # change transaction status etc.
    #     return HttpResponse('OK')
