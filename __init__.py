from decimal import Decimal
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import get_language

from .forms import ProcessPaymentForm
from ..core import BasicProvider
from ..utils import calculate_md5

CENTS = Decimal('0.01')

class PaygateProvider(BasicProvider):

    def __init__(self, *args, **kwargs):
        self.paygate_id = kwargs.pop('id') # Provided by paygate
        self.project_id = kwargs.pop('project_id')
        self.endpoint = kwargs.pop(
             'endpoint', 'https://secure.paygate.co.za/payweb3/initiate.trans') # Get test endpoint for paygate
        super(PaygateProvider, self).__init__(*args, **kwargs)

    def get_hidden_fields(self, payment):
        # Step 1 send transaction data to Paygate
        data = {
            'paygate_id'        : self.paygate_id,
            'reference'         : payment.transaction_id,
            'amount'            : Decimal(str(payment.total)).quantize(CENTS) * 100,
            'currency'          : payment.currency,
            'return_url'        : self.get_return_url(payment),
            'transaction_date'  : payment.created,
            'locale'            : get_language(),
            'control'           : str(payment.id),
            'description'       : payment.description,
            'country'           : '',
            'email'             : payment.billing_email,
            'notify_url'        : payment.get_process_url(),
            }
        data['checksum'] = calculate_md5(data)

        return data

    def process_data(self, payment, request):
        if request.POST['AUTH_CODE']: # Step 4
            hash_dict = request.POST
            hash_dict.pop('checksum')
            md5_hash = calculate_md5(hash_dict)
            if md5_hash != request.POST['CHECKSUM']
                return HttpResponseForbidden('FAILED')
            # change transaction status etc.    
            return HttpResponse('OK')

        # Step 2 validate the response from Paygate
        form = ProcessPaymentForm(payment=payment,
                                  paygate_id=self.paygate_id,
                                  data=request.POST or None
                                  )
        if not form.is_valid():
            return HttpResponseForbidden('FAILED')

        # Step 3 redirect user to Paygate

        form.save()
        return render(request, 'form.html', {
        'form': form}) # FIX
