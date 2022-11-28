# -*- coding: utf-8 -*-
import string
from traceback import print_tb
from xml.etree.ElementTree import tostring

connectionTypes = ('wired', 'wireless', 'none')
for ctype in connectionTypes:
   print(ctype)
DGS_models = {'DGS-210', 'DGS-230','GK-01','GK-04'}
DGS_models.add('DGS-200')
print('Список моделей ДГС:')
print(DGS_models)
device_list = {1:'ER2100124213'}
for i in range(2,10):
    device_list[i] = 'ER21000000{0}'.format(i)
print("Список приборов:")
for device in device_list.items():
    print(device[1])
stringVariable = 'ya, boii, tis\' a string!'
intVariable = 1
floatVariable = 1.0
print("Типы переменных:")
print(type(connectionTypes))
print(type(DGS_models))
print(type(device_list))
print(type(stringVariable))
print(type(intVariable))
print(type(floatVariable))
