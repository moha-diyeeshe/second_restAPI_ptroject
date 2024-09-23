from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import MenuItem
from rest_framework import generics
from .serialiazers import MenuItemSerialiazers
from django.core.paginator import Paginator,EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,throttle_classes
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

# Create your views here.
@api_view(['GET'])
def index(request):
    return Response('list of books', status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def menu_item(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        per_page = request.query_params.get('per_page',default=4)
        page = request.query_params.get('page',default=1)

        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_field = ordering.split(",")
            items = items.order_by(*ordering_field)
        paginator = Paginator(items,per_page=per_page)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items=[]
        serializer_item = MenuItemSerialiazers(items, many = True)
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



@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"some secret message"})



@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='manager').exists():
     return Response({"message":"only manager can see it"})
    else:
        return Response({"message":"is not allowed this "},403)
    

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"throtelling"})



@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"for logged user only"})