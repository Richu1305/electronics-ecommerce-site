import urllib.request
def get_product_count(url):
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    return html.count('class="product-title"')

try:
    print("Mobiles:", get_product_count("http://127.0.0.1:8000/userhome?search=Mobiles"))
except urllib.error.HTTPError as e:
    print(e.read().decode())
print("moBiles:", get_product_count("http://127.0.0.1:8000/userhome?search=moBiles"))
