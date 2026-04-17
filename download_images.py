import urllib.request
import os

files = {
    'iqoo.jpg': 'https://placehold.co/400x400/png?text=Mobile',
    'HP_Laptop.jpg': 'https://placehold.co/400x400/png?text=Laptop',
    'HP_keyboard.png': 'https://placehold.co/400x400/png?text=Keyboard',
    'epson_E6L4gQG.jpg': 'https://placehold.co/400x400/png?text=Printer',
    'Smartwatch_Relógio.jpg': 'https://placehold.co/400x400/png?text=Watch'
}

for name, url in files.items():
    try:
        path = os.path.join('media', 'image', name)
        urllib.request.urlretrieve(url, path)
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed {name}: {e}")
