from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework import authentication,permissions

from api.serializers import UserSerializer,CakeSerializer,CartSerializer,OrderSerializer,ReviewSerializer
from api.models import Cake,Cart,Review,Order


class UsersView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()


class CakesView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class=CakeSerializer
    queryset=Cake.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


   #http://127.0.0.1:8000/api/cakes/:id/add_to_cart/
    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        serializer=CartSerializer(data=request.data)
        cake_obj=Cake.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

    #http://127.0.0.1:8000/api/cakes/:id/place_order/
    @action(methods=['POST'],detail=True)
    def place_order(self,request,*args,**kwargs):
        serializer=OrderSerializer(data=request.data)
        cake_obj=Cake.objects.get(id=kwargs.get("pk"))
        user=request.user
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
    #http://127.0.0.1:8000/api/cakes/:id/add_review/
    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        serializer=ReviewSerializer(data=request.data)
        cake_obj=Cake.objects.get(id=kwargs.get("pk"))
        user=request.user
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


class CartsView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=CartSerializer
    queryset=Cart.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class OrdersView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)