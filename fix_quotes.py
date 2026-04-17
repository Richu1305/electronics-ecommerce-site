import sys
fpath = r'c:\Users\user\Desktop\company\newproject\newproject\template\common\home.html'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace(r"\'", "'")
with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)
