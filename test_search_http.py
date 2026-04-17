import urllib.request
import urllib.parse
from urllib.error import HTTPError

def get_product_count(url):
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    # search for <h5 class="product-title"
    return html.count('class="product-title"')

print("Mobile:", get_product_count("http://127.0.0.1:8000/userhome?search=Mobile"))
print("Watch:", get_product_count("http://127.0.0.1:8000/userhome?search=Watch"))
print("Empty:", get_product_count("http://127.0.0.1:8000/userhome?search="))
print("All:", get_product_count("http://127.0.0.1:8000/userhome"))
print("For You:", get_product_count("http://127.0.0.1:8000/userhome?search=For+You"))
