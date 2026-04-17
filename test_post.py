import urllib.request
import urllib.parse
from django.core.management.utils import get_random_secret_key

try:
    data = urllib.parse.urlencode({'Name': 'Test', 'Description': 'Test Desc'}).encode()
    req = urllib.request.Request('http://127.0.0.1:8000/category', data=data, method='POST')
    # Because of CSRF, we can't easily post from urllib without a token. 
    # But wait, we can just GET the page instead to see if GET is crashing?
    print(urllib.request.urlopen('http://127.0.0.1:8000/category').getcode())
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()
