import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newproject.settings")
django.setup()

from manager.models import Product, Category
from user.views import userhome
from django.test import RequestFactory

rf = RequestFactory()
from django.contrib.auth.models import AnonymousUser

request = rf.get('/userhome/?search=Mobile')
request.user = AnonymousUser()
response = userhome(request)
print("Mobile Count:", response.context_data['data'].count() if hasattr(response, 'context_data') else "unknown context")

request2 = rf.get('/userhome/?search=watch&category=')
request2.user = AnonymousUser()
response2 = userhome(request2)
print("Watch Count:", response2.context_data['data'].count() if hasattr(response2, 'context_data') else "unknown")

request3 = rf.get('/userhome/?search=&category=')
request3.user = AnonymousUser()
response3 = userhome(request3)
print("Empty Count:", response3.context_data['data'].count() if hasattr(response3, 'context_data') else "unknown")

print("All Products count:", Product.objects.count())
