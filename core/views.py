# Импортируем необходимые библиотеки
from django.shortcuts import render
import numpy as np
import plotly.graph_objects as go
from scipy.misc import derivative
from sympy import symbols, lambdify, sympify
from core.forms import DateForm
from .models import *


# Функция для поиска экстремумов
def find_extrema(func, x_values):
    # Рассчитываем значения функции в заданных точках
    y_values = func(x_values)

    # Вычисляем первую производную
    first_derivatives = derivative(func, x_values, dx=1e-6)

    # Вычисляем вторую производную
    second_derivatives = derivative(func, x_values, dx=1e-6, n=2)

    # Список найденных экстремумов
    extrema = []

    # Минимальное расстояние между экстремумами
    min_distance = 1

    # Координата X последнего найденного экстремума
    last_extremum_x = None

    # Перебираем все точки x, кроме первой и последней
    for i in range(1, len(x_values) - 1):
        # Проверяем, меняет ли знак первая производная
        if first_derivatives[i - 1] * first_derivatives[i + 1] < 0:
            # Если это не первый экстремум и он достаточно далеко от предыдущего
            if last_extremum_x is None or abs(x_values[i] - last_extremum_x) >= min_distance:
                # Определяем тип экстремума по знаку второй производной
                extrema_type = 'min' if second_derivatives[i] > 0 else 'max'
                # Добавляем экстремум в список
                extrema.append((x_values[i], y_values[i], extrema_type))
                # Запоминаем координату X текущего экстремума
                last_extremum_x = x_values[i]

    return extrema


# Функция для построения графика и анализа
def chart(request):

    func_error = None

    # Обработка POST-запроса
    if request.method == 'POST':
        form = DateForm(request.POST)

        # Проверка валидности формы
        if form.is_valid():
            func = (form.cleaned_data['func']).lower()  # Извлекаем введенную функцию
            x_start = form.cleaned_data['x_start']  # Извлекаем начальное значение X
            x_end = form.cleaned_data['x_end']  # Извлекаем конечное значение X

            # Преобразуем функцию в символьную форму
            x = symbols('x')
            
            try:
                user_defined_function = lambdify(x, sympify(func))
            except Exception as e:
                func_error = e
                context = {'form': form, 'func_error': func_error}
                return render(request, 'core/chart.html', context)

            # Создаем массив значений X
            x_values = np.linspace(x_start, x_end, 100000)

            # Находим экстремумы функции
            try:
                extrema = find_extrema(user_defined_function, x_values)
            except Exception as e:
                func_error = e
                context = {'form': form, 'func_error': func_error, }
                return render(request, 'core/chart.html', context)


            # Рассчитываем значения функции для всех значений X
            y = user_defined_function(x_values)

            # Создаем объект Figure для построения графика
            fig = go.Figure()

            # Добавляем линию графика функции
            fig.add_trace(go.Scatter(x=x_values, y=y, mode='lines', name='Function'))

            # Инициализируем переменные для поиска максимального и минимального значения
            max_value = float('-inf')
            min_value = float('inf')
            max_point = None
            min_point = None

            # Списки для хранения точек экстремумов
            all_max_extremum_dots = []
            all_min_extremum_dots = []

			# Ищем максимальное и минимальное значения среди экстремумов
            for extremum in extrema:
                if extremum[2] == "max":
                    all_max_extremum_dots.append(extremum)
                    if extremum[1] > max_value:
                        max_value = extremum[1]
                        max_point = extremum
                elif extremum[2] == "min":
                    all_min_extremum_dots.append(extremum)
                    if extremum[1] < min_value:
                        min_value = extremum[1]
                        min_point = extremum

            # Добавляем точки экстремумов на график
            for dot in extrema:
                fig.add_trace(go.Scatter(x=[dot[0]], y=[dot[1]], mode='markers', name=f"{dot[2]}"))

            # Формируем заголовок графика
            title_text = f'График функции {func} от {x_start} до {x_end}'
            if max_point and min_point:
                title_text += f'<br>Имеет экстремумы в точках {max_point[2]} — ({round(max_point[0], 2)}, {round(max_point[1], 2)}) | {min_point[2]} — ({round(min_point[0], 2)}, {round(min_point[1], 3)})'
            elif max_point:
                title_text += f'<br>Имеет максимум в точке {max_point[2]} — ({round(max_point[0], 2)}, {round(max_point[1], 2)})'
            elif min_point:
                title_text += f'<br>Имеет минимум в точке {min_point[2]} — ({round(min_point[0], 2)}, {round(min_point[1], 2)})'
            else:
                title_text += f'<br>Не имеет экстремумов'

            # Настраиваем параметры графика
            fig.update_layout(
                title=title_text,
                xaxis_title='X',
                yaxis_title='Y',
                title_font_size=24,
                title_x=0.5
            )

            # Преобразование графика в HTML-код для вставки на веб-страницу
            chart = fig.to_html()

            # Создание объекта данных с функцией и диапазоном X
            data = Data(func=func, x_start=x_start, x_end=x_end)
            
            # Сохранение объекта данных в базу данных
            data.save()
            # Формирование контекста для передачи в шаблон: график и форма
            context = {'chart': chart, 'form': form, 'func_error': func_error}
    else:
        # Создание пустой формы, если метод запроса не POST
        form = DateForm()
        # Формирование контекста только с формой
        context = {'form': form, 'func_error': func_error}

    # Рендеринг HTML-шаблона 'core/chart.html' с передачей контекста
    return render(request, 'core/chart.html', context)

