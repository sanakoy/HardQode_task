from rest_framework import serializers
from django.contrib.auth.models import *
from .models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'video']

class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'lessons_count')

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()
