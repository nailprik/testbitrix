from django.contrib import admin
from django.urls import path

from find.views import MainPage, Duplicates

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('duplicates/', Duplicates.as_view())
]
