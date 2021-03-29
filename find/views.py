import json
import math

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from duplicates import settings
from find.tools import find_duplicates, make_batch, get_all_companies_titles


class Duplicates(APIView):

    def get(self, request):
        domain = request.GET['domain']
        access_token = request.GET['access_token']
        titles = get_all_companies_titles(access_token, domain)
        duplicates = find_duplicates(titles)
        return Response(duplicates)


class MainPage(APIView):

    @csrf_exempt
    def post(self, request):
        access_token = request.data['AUTH_ID']
        domain = request.GET["DOMAIN"]
        data = {
            'access_token': access_token,
            'domain': domain,
            'HOST': settings.ALLOWED_HOSTS[0]
        }
        return render(request, 'index.html', context=data)
