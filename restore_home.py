import re

html_file = r'c:\Users\user\Desktop\company\newproject\static\MiniStore-1.0.0\index.html'
out_file = r'c:\Users\user\Desktop\company\newproject\newproject\template\common\home.html'

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = next(i for i, line in enumerate(lines) if '<section id="billboard"' in line)
end_idx = next(i for i, line in enumerate(lines) if '<footer id="footer"' in line)

content = "".join(lines[start_idx:end_idx])
content = re.sub(r'src="images/([^"]+)"', r'src="{% static \'MiniStore-1.0.0/images/\1\' %}"', content)
content = re.sub(r"url\('images/([^']+)'\)", r"url('{% static \'MiniStore-1.0.0/images/\1\' %}')", content)
content = content.replace(r"\'", "'")
content = content.replace("shop.html", "{% url 'userhome' %}")
content = content.replace("blog.html", "#")
content = content.replace("single-post.html", "#")
content = content.replace("contact.html", "#")
content = content.replace("cart.html", "{% url 'cartitems' %}")
content = content.replace("checkout.html", "{% url 'checkout' %}")

with open(out_file, 'w', encoding='utf-8') as f:
    f.write("{% extends 'common/base.html' %}\n")
    f.write("{% load static %}\n")
    f.write("{% block content %}\n")
    f.write(content)
    f.write("{% endblock %}\n")
