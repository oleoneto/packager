# packager:core:routes

"""
Import routes into each view module and append the path to the list:
# packager/core/views.my_view.py
from django.urls import path
from packager.core.views.routes import routes

def my_view(request):
    ...

routes.append(
    path('', my_view, name='my-view')
)


Append the whole list to your urlpatterns:
# packager/core/urls.py
from packager.core.views.routes import routes

urlpatterns = [
    ...
] + routes
"""

routes = []
