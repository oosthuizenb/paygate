from datetime import date
from hashlib import md5

from django.utils.translation import ugettext_lazy as _



def get_month_choices():
    month_choices = [(str(x), '%02d' % (x,)) for x in range(1, 13)]
    return [('', _('Month'))] + month_choices


def get_year_choices():
    year_choices = [(str(x), str(x)) for x in range(
        date.today().year, date.today().year + 15)]
    return [('', _('Year'))] + year_choices

def calculate_md5(data):
    checksum = ''
    key = 'secret' # This is last value added to encryption key before md5 is called.
    for key,value in data:
        checksum = f'{checksum}{value}'
    checksum = f'{checksum}{key}' # add key to checksum value
    md5_hash = md5(checksum.encode('utf-8')).hexdigest()
    print(md5_hash) # debugging
    return md5_hash
