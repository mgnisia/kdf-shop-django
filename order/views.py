
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer
import requests
import os

class MissingEnvironmentVariable(Exception):
    pass


def get_my_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")

token = get_my_env_var('MAILGUN_TOKEN')
domain = get_my_env_var('MAILGUN_DOMAIN')
reply_mail = get_my_env_var('REPLY_TO_MAIL')

@api_view(['POST'])
def checkout(request):
    print(request.data)
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        print(serializer.validated_data['items'])
        items_ordered = ""
        for item in serializer.validated_data['items']:
            items_ordered += f"Produkt {item.get('product')} Preis (EZ) {item.get('product').price} Preis (Summme) {item.get('quantity') * item.get('product').price}"
            items_ordered += "\n"
        print(items_ordered)

           
        try:
            r = requests.post(
                f"{domain}/messages",
                auth=("api", token),
                data={"from": "Bestellung KDF Shop <mailgun@mail.kdf-shop.de>",
                    "to": [reply_mail],
                    "h:Reply-To": reply_mail,
                    "subject": "Deine Bestsellung bei dem kdf-shop.de",
                    "text": f"Deine Bestellung \n {items_ordered} \n Viele Grüße\n Moritz"})      
            serializer.save(items_ordered=items_ordered)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)