# Импортируем необходимые библиотеки
from django import forms
from .models import *

# Определяем класс формы
class DateForm(forms.Form):

    # Поле для ввода функции

    # Тип поля: forms.CharField
    # Максимальная длина: 255 символов

    func = forms.CharField(max_length=255,
                         help_text="<br>Введите функцию в таком виде. Например: 'x^2 + 2*x'")

    # Поле для ввода начального значения X

    # Тип поля: forms.FloatField
    # Принимает только числа с плавающей точкой

    x_start = forms.FloatField(
        help_text="<br>Введите начальное значение X. Например: 0")

    # Поле для ввода конечного значения X

    # Тип поля: forms.FloatField
    # Принимает только числа с плавающей точкой

    x_end = forms.FloatField(
        help_text="<br>Введите конечное значение X. Например: 10")
