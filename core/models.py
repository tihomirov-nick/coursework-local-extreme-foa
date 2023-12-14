# Импортируем необходимые библиотеки
from django.db import models
from django.utils.timezone import now

# Определяем класс модели
class Data(models.Model):

    # Поле для хранения функции

    # Тип поля: models.CharField
    # Максимальная длина: 255 символов

    func = models.CharField('Функция', max_length=255)

    # Поле для хранения начального значения X

    # Тип поля: models.FloatField
    # Значение по умолчанию: 0

    x_start = models.FloatField('Начало интервала', default=0)

    # Поле для хранения конечного значения X

    # Тип поля: models.FloatField
    # Значение по умолчанию: 0

    x_end = models.FloatField('Конец интервала', default=0)

    # Поле для хранения даты создания графика

    # Тип поля: models.DateTimeField
    # Значение по умолчанию: текущая дата и время
    # Поле может быть изменено пользователем

    date_create = models.DateTimeField('Дата создания графика', default=now, editable=True)

    # Переопределяем метод `__str__()`

    # Возвращает строковое представление модели

    def __str__(self):
        return self.func

