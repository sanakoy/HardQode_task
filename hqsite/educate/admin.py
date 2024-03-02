from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)

class ProductInline(admin.TabularInline):  # Или admin.StackedInline
    model = Product.users.through
    extra = 1

class GroupInline(admin.TabularInline):
    model = Group.users.through
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [ProductInline, GroupInline]
# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)