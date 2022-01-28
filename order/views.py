
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

# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def checkout(request):
    print(request.data)
    serializer = OrderSerializer(data=request.data)
    print(serializer, serializer.is_valid())
    if serializer.is_valid():
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        print(serializer.validated_data['items'])
        items_ordered = ""
        for item in serializer.validated_data['items']:
            items_ordered += f"Product {item.get('product')} Preis (EZ) {item.get('product').price} Preis (Summme) {item.get('quantity') * item.get('product').price}"
        print(items_ordered)
        # paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        try:
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