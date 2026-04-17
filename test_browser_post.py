import urllib.request
import urllib.parse
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. GET request to get CSRF token
resp = opener.open('http://127.0.0.1:8000/category')
html = resp.read().decode()
csrf_token = None
for line in html.split('\n'):
    if 'name="csrfmiddlewaretoken"' in line:
        csrf_token = line.split('value="')[1].split('"')[0]
        break

if not csrf_token:
    print("Could not find CSRF token")
    import sys; sys.exit(1)

# 2. POST request
data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': csrf_token,
    'Name': 'My New Category',
    'Description': 'This is a description'
}).encode()

try:
    resp2 = opener.open('http://127.0.0.1:8000/category', data=data)
    print("Success! HTTP", resp2.getcode())
except Exception as e:
    import traceback
    traceback.print_exc()
