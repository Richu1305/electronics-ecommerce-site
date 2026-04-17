import urllib.request
def get_product_count(url):
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    return html.count('class="product-title"')

print("Mobile with empty category:", get_product_count("http://127.0.0.1:8000/userhome?search=Mobile&category="))
