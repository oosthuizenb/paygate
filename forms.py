from django import forms

from ..utils import calculate_md5

class ProcessPaymentForm(forms.Form):

    paygate_id = forms.IntegerField()
    pay_request_id = forms.CharField()
    reference = forms.CharField()
    checksum = forms.CharField()

    def __init__(self, payment, paygate_id, **kwargs):
        super(ProcessPaymentForm, self).__init__(**kwargs)
        self.payment = payment
        self.paygate_id = paygate_id

    def clean(self):
        cleaned_data = super(ProcessPaymentForm, self).clean()
        hash_dict = cleaned_data
        hash_dict.pop('checksum')
        md5_hash = calculate_md5(hash_dict)

        if not self.errors:
            if cleaned_data['paygate_id'] != self.paygate_id:
                self._errors['paygate_id'] = self.error_class(['Bad paygate id'])
            if cleaned_data['reference'] != self.payment.transaction_id:
                self._errors['reference'] = self.error_class(['Bad reference'])
            if self.cleaned_data['checksum'] != md5_hash:
                self._errors['checksum'] = self.error_class(['Bad hash'])
        return cleaned_data
