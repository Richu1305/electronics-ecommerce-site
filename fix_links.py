import os

files = [
    r'c:\Users\user\Desktop\company\newproject\newproject\template\common\base.html',
    r'c:\Users\user\Desktop\company\newproject\newproject\template\user\pixel1.html'
]

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace href="index.html" with href="{% url 'home' %}"
        new_content = content.replace('href="index.html"', 'href="{% url \'home\' %}"')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
