# -*- coding: utf-8 -*-
# Задание на ЛР3: 
# 1. Черновую архитектуру проекта и **задачи** проекта — что будем обрабатывать и что хотим из этого всего получить
# 2. Отчитаться за блок документом с целью, задачами, архитектурой, функциональными требованиями, входными и выходными воздействиями
# 3. Продолжить изучение ООП в Питоне — взять свои коллекции из первых 2-х лаб. работ и переработать их в иерархию классов
# 4. Изучить и быть готовыми объяснить на примерах разницу между `__str__` и `__repr__` для пользовательского класса, можно прямо написать вывод иерархии классов через эти методы
# 5. Проработать имитацию функции `__call__`
#-----------------------------------------------------------------------------------------------------------

# 1: Черновой вариант проекта:
#Цель - создать демо-программу для распознавания авто и людей на фото/видео 
#для последующей ее модификации

#Задачи:
#  1. Создать модуль ввода обрабатываемых данных
#  2. Создать модуль приведения входных данных в необходимые форматы
#    3.1 Создать модуль обработки фото
#    3.2 Создать модуль обработки видео
#  4. Создать пользовательский веб-интерфейс
#  5. Провести тестирование/при необходимости обучение моделей
#  
#Технологии:
#  Интерфейс: веб фреймворк Flask
#  База Данных: PostgreSQL
#  Основной функционал (Распознавание на видео): OpenCV / TensorFlow+Keras
#
#Входные воздействия:
#  Загрузка изображения (png, jpg, jpeg и пр.) и/или вилео (mp4, flv, webm, avi) в виде файла или ссылки
#  
#Выходные данные:
#  Вывод кол-ва распознанных объектов
#  ?Real-time демонстрация и выделение распознанных объектов

class Sensor:
    # Класс сенсора прибора
    def __init__(self, id: int, type_name: str):
        self.id = id
        self.type = type_name
        pass
    
    def __repr__(self) -> str:
        return 'Repr: Id:{0}:{1}'.format(self.id, self.type)
    
    def __str__(self) -> str:
        return 'Str: Id:{0}:{1}'.format(self.id, self.type)

class Device:
    # Класс приборов
    def __init__(self, id: int, manuf_number: str, device_type: str):
        self.id = id
        self.manuf_number = manuf_number
        self.device_type = device_type
        pass

class DGS(Device):
    # Класс Датчиков-Газоанализаторов Стационарных
    def __init__(self, id: int, manuf_number: str, smart_sensor: Sensor):
        self.sensor = smart_sensor
        super().__init__(id, manuf_number, 'DGS')
        pass
    
    def __call__(self):
         print(self.smart_sensor)

    def __str__(self):
        return f'STR DGS: {self.manuf_number} ({self.sensors[0].type})'   

class PG(Device):
    # Класс Персональных Газоанализаторов
    def __init__(self, id: int, manuf_number: str, sensors: Sensor):
        self.sensors = sensors
        super().__init__(id, manuf_number, 'PG')
        pass

    def __call__(self):
         print(self.sensors)

    def __str__(self):
        return f'STR PG: {self.manuf_number} ({self.sensors[0].type})'     

if __name__ == '__main__':

    pg1 = PG(1,'ПГ-123456789', [Sensor(id+1, 'BS12-5') for id in range(4)])
    pg1()
    print(pg1.sensors)
    print(pg1)
    for sensor in pg1.sensors:
        print(sensor)
    devices = []
    for i in range(10):
        devices.append(DGS(i+1, f'DGS-210000{i}', Sensor(i,'smart')))
        devices.append(PG(i+1, f'ПГ-100000{i}', [Sensor(id+i+1, 'BS12-5') for id in range(4)]))

    for device in devices:
        print(device.manuf_number)

    print(f'Родительский класс класса {type(pg1).__name__}: {type(pg1).__base__.__name__}')
        





