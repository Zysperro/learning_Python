# -*- coding: utf-8 -*-
# Задание на ЛР2:
# 1. Организовать существующую кодовую базу в соответствии с требованиями PEP8 и/или обосновать отступления от него в комментариях к этим отступлениям
# 2. Привести скрипты к виду скриптов — особенно касается `__main__`
# 3. Закрепить принципы работы с областями видимости
# 4. Отметить принципы именования переменных и классов в соответствии с PEP8 (можно делать вместе с п. 1)
#-----------------------------------------------------------------------------------------------------------

import string
from traceback import print_tb
from xml.etree.ElementTree import tostring

# Заменил все наименования переменных c camelCase на соотв. PEP lower_case 
# Например connectionTypes заменил на connection_types

# Добавил указатель 
if __name__ == '__main__':

    # Список типов подключения к газоанализаторов (ДГС)
    connection_types = (
        'wired', 
        'wireless', 
        'none'
        )  # Оформил по PEP 8 в столбик
    print(connection_types)
    # Список моделей газоанализаторов. Оформил по PEP 8
    dgs_models = {
        'dgs-210', 'dgs-230',
        'GK-01','GK-04'
        } 
    dgs_models.add('dgs-200')
    print('Список моделей ДГС:')
    print(dgs_models)
    device_list = {1: 'ER2100124213'}
    for i in range(2,10):
        device_list[i] = 'ER21000000{0}'.format(i)
    print("Список приборов:")
    for device in device_list.items():
        print(device[1])
    # Переменные для демонстрации типов
    string_variable = 'ya, boii, tis\' a string!'
    int_variable = 1
    float_variable = 1.0
    outside_variable = "I'm an outside variable! Unchanged!"  # Переменная для демонстрации областей видимости
    print(outside_variable)

    # Просто функция для вывода типов наших переменных и демонстрации области видимости
    def print_data_types():    
        print("Типы переменных:")
        print(type(connection_types))
        print(type(dgs_models))
        print(type(device_list))
        print(type(string_variable))
        print(type(int_variable))
        print(type(float_variable))
        outside_variable = "Wow, now I'm inside! Totally different!"
        print(outside_variable)  # Выводим измененную строку внутри функции
        
        
    print_data_types()
    print(outside_variable) # Выводим "измененную" строку вне функции после ее вызова
    pass
    
