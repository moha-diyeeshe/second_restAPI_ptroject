from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import MenuItem
from rest_framework import generics
from .serialiazers import MenuItemSerialiazers

# Create your views here.
@api_view(['GET'])
def index(request):
    return Response('list of books', status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def menu_item(request):
    if request.method == 'GET':
        item = MenuItem.objects.select_related('category').all()
        serializer_item = MenuItemSerialiazers(item, many = True)
        return Response(serializer_item.data)
    if request.method == 'POST':
        serializer_item = MenuItemSerialiazers(data = request.data)
        serializer_item.is_valid(raise_exception=True)
        serializer_item.save()
        return Response(serializer_item.data,status=status.HTTP_201_CREATED)
@api_view(['GET','POST'])
def Single_item(request,pk):
    item = get_object_or_404(MenuItem,pk = pk)    
    serializer_class = MenuItemSerialiazers(item)
    return Response(serializer_class.data)






