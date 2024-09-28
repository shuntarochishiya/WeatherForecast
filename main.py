# Подключение необходимых библиотек
from tkinter import *
from pyowm import OWM
from pyowm.utils.config import get_default_config
from datetime import datetime
from tzwhere import tzwhere
from geopy.geocoders import Nominatim
import pytz
from tkinter import messagebox
import io
from pyowm.utils import timestamps
from PIL import ImageTk, Image

# Функция, получающая на вход город, введенный пользователем и выводящая время в нем
def time():
    # Создание области для вывода времени заданного города
    time_frame = Frame(frame, bg='#FFC0CB')
    time_frame.place(rely=0.876, height=55, width=284)

    time_Label = Label(time_frame, bg='#FFC0CB')
    time_Label.configure(font=('Arial', 14), fg='white')
    time_Label.pack()

    # Получение города и его координат
    address = search_input.get()
    w = tzwhere.tzwhere()
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(address)

    # Определение часового пояса города и вывод времени
    timezone = w.tzNameAt(location.latitude, location.longitude)
    source_date = datetime.now()
    currentTimeZone = pytz.timezone(str(timezone))
    currentDateTime = currentTimeZone.localize(source_date)
    newDateTime = currentDateTime.astimezone(currentTimeZone)

    # Вывод времени
    time_Label.config(text=f'Текущее время в вашем городе:\n{newDateTime.strftime("%H:%M (%Z (GTM))")}')

# Функция, получающая погоду в городе на завтра
def tomorrow():
    # Создание области для вывода прогноза погоды
    city = search_input.get()
    result_frame = Frame(frame, bg='#E6E6FA')
    result_frame.place(rely=0.3, height=230, relwidth=1)

    info = Label(result_frame, bg='#DDA0DD', font=40)
    info.pack()

    # Получение данных о погоде на следующий день
    owm = OWM('31cc3df8fce4e76440685a9a5829e83c')
    mgr = owm.weather_manager()
    three_h_forecast = mgr.forecast_at_place(str(city), '3h')
    tomorrow_at_midday = timestamps.tomorrow(12, 0)
    link = three_h_forecast.get_weather_at(tomorrow_at_midday)

    status = link.detailed_status
    temp = link.temperature('celsius')['temp']

    # Вывод информации о погоде
    weather = f"В городе {city} завтра\n{status}\n\nТемпература {round(temp)}° по Цельсию"
    info['text'] = weather

    # Кнопка для возвращения к текущему прогнозу
    tomorrow_button = Button(result_frame, bg='#E6E6FA', text="Вернуться назад?", font=1, command=result_frame.destroy)
    tomorrow_button.pack(side=BOTTOM)

# Функция, получающая информацию о погоде в данный момент
def forecast():
    city = search_input.get()

    result_frame = Frame(frame, bg='#E6E6FA')
    result_frame.place(rely=0.3, height=230, relwidth=1)

    info = Label(result_frame, bg='#DDA0DD', font=20)
    info.pack()

    # Получение данных о погоде
    owm = OWM('31cc3df8fce4e76440685a9a5829e83c')
    manager = owm.weather_manager()
    observation = manager.weather_at_place(city)
    link = observation.weather

    status = link.detailed_status
    humidity = link.humidity
    temp = link.temperature('celsius')['temp']
    wind_speed = link.wind()['speed']
    pressure = round(link.barometric_pressure()['press'] * 0.750062)

    # Формирование строки с информацией о погоде
    weather = (f"В городе {city} сейчас\n{status}\n\nТемпература {round(temp)}° по Цельсию"
               f"\n\nВлажность воздуха {humidity}%\n\nСкорость ветра {wind_speed} м/с"
               f"\n\nДавление {pressure} мм.рт.ст.")
    info['text'] = weather

    # Кнопка для отображения прогноза на завтра
    tomorrow_button = Button(frame, bg='#E6E6FA', text="Прогноз погоды на завтра?", font=1, command=tomorrow)
    tomorrow_button.place(rely=0.858, relx=0.566, width=220)

# Проверка наличия города в списке городов мира
def check(city):
    with io.open('D:/PythonProjects/WeatherForecast/list.txt', encoding='utf-8') as file:
        for line in file:
            if city in line:
                return True
        return False

# Обработка нажатия кнопки поиска
def click():
    city = search_input.get()
    if check(city):
        forecast()
        time()
    else:
        messagebox.showwarning("Предупреждение", "Город не найден. Пожалуйста, уточните название.")

# Обработка нажатия клавиши Enter
def callback(event):
    click()

# Очистка строки ввода
def delete_input():
    search_input.delete(0, 'end')

# Установка языка программы
config_dict = get_default_config()
config_dict['language'] = 'ru'

# Создание главного окна
app = Tk()
app.title("Прогноз погоды")
app.resizable(width=False, height=False)
app['bg'] = 'yellow'
app.iconbitmap('D:/PythonProjects/WeatherForecast/pic.ico')

# Центрирование окна
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f'540x480+{w//2-200}+{h//2-250}')

# Холст для размещения элементов
canvas = Canvas(app, width=540, height=480, bg='#00CED1')
canvas.pack()

# Рамка для всех элементов
frame = Frame(app, bg='#1E90FF', bd=5)
frame.place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.94)

# Фоновое изображение
img = ImageTk.PhotoImage(Image.open("sky.png"))
canvas.create_image(20, 20, anchor=NW, image=img)

# Основная надпись
title = Label(frame, text='Погода в вашем городе', bg='#B0E0E6')
title.configure(font=("Comic Sans MS", 20, "italic"), relief='groove', height=1, width=20)
title.place(relx=0.17, rely=0.03)

# Рамка для строки ввода и кнопок
string_frame = Frame(frame, bg='#E6E6FA')
string_frame.place(relx=0.03, rely=0.15, height=55, relwidth=0.94)

# Кнопка поиска
button = Button(string_frame, text='Перейти', bg='#40E0D0', command=click)
button.configure(font=("Verdana", 14), fg='white')
button.place(relx=0.78, rely=0.15)

# Строка ввода
search_input = Entry(string_frame, bg='#E0FFFF')
search_input.configure(font=('Candara', 15))
search_input.place(relx=0.01, rely=0.15, width=360, height=40)
search_input.bind('<Return>', callback)

# Кнопка удаления текста
cross = Button(search_input, text='X', bg='#E0FFFF', command=delete_input)
cross.place(relx=0.95, width=20, relheight=1)

# Запуск приложения
app.mainloop()
