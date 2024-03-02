from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils import timezone


from .models import *
from django.conf import settings
from django.contrib.auth.models import User

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def group_manager(sender, instance, created, **kwargs):
    user_products = instance.products.values_list('id', flat=True) # список всех курсов, которые доступны пользователю

    for i in list(user_products):
        prod = Product.objects.get(pk=i)
        if prod.time_start > timezone.now(): # проверка времени начала курса
            prod_groups = Group.objects.filter(product__pk=i, product=i) # список всех групп конкретного курса
            if len(prod_groups) > 0: # проверка на наличие групп в продукте
                without_group = True # добавляем проверку того, относится ли уже данный пользователь к группе данного курса

                for j in prod_groups:
                    if j in instance.group_members.all():
                        without_group = False # проверка не пройдена, пользователь есть уже в какой-то группе по данному курсу

                if without_group: # если True, то проверка пройдена, пользователя нет ни в одной группе, надо добавить его
                    is_not_added = True # добавляем проверку на то, отправили ли пользователя в группу, где не хватает учеников

                    for j in prod_groups: # проход по всем группам
                        if len(j.users.all()) < prod.min_students: # поиск группы, где не хватает учеников
                            instance.group_members.add(j) # добавление ученика к группе
                            is_not_added = False # переводим флажок в False, чтобы код остановился
                            break

                    if is_not_added: # если True, значит не нашлось группы, где нет минимального кол-ва учеников
                        arr_group_not_full = [] # список будет содержать группы, в которых есть свободные места
                        for j in prod_groups:
                            if len(j.users.all()) < prod.max_students: # проверка заполненности группы
                                arr_group_not_full.append(j) #добавление в список не запоненную группу
                        min_prod_group = len(arr_group_not_full[0].users.all()) # количество учеников в первой группе для вычисление минимума

                        for j in arr_group_not_full:
                            len_j = len(j.users.all())
                            if len_j < min_prod_group:
                                min_prod_group = len_j # нахождение минимума

                        for j in arr_group_not_full:
                            if len(j.users.all()) == min_prod_group: # поиск минимальной незаполненной группы
                                instance.group_members.add(j) # добавление пользователя в минимальную группу
                                break
            else:
                print('Не существует групп для этого продукта')
            '''Таким образом, автоматическое заполнение групп будет происходить равномерно, как и было сказано в задании!'''
