from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product, Lesson
from .serializers import ProductSerializer
from rest_framework.views import APIView


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class LessonAPIView(APIView):
    def get(self, request):
        student = request.data['user']
        user_instance = User.objects.get(username=student)
        user_products = user_instance.products.all()
        print(user_products[0])
        lessons = []
        for i in user_products:
           lessons.append(Lesson.objects.filter(product=i).values('name', 'video', 'product__name'))
        print(lessons)

        return Response({'product_info': lessons})
class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

