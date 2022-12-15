import eml_parser
import email
import html2text as h2t
from urlextract import URLExtract
import re

from os import walk

path = './SpamFolder/'
out_path = './OutputMsgs/'

def Get_Parsed_EML_Messages(eml_files: bytes):
    """ Функция для парсинга EML файлов (email писем)

    Args: 
        eml_files[]: Список .eml файлов ( open(email_path, 'rb').read() )

    Returns:
        dict[]: Массив словарей отпарсенных частей сообщений
            dict[['body'], ['headers']]:\n
                dict['body']:  - тело\n
                    dict['body']['text'] - текстовая часть из html письма\n
                    dict['body']['urls'] - ссылки из текстовой составляющей html письма\n
                dict['header']: - заголовки письма\n
                    dict['header']['from'] - От кого (пример - no-reply.dns@email.dns-shop.ru)\n
                    dict['header']['received_domain'][] - Домен(ы) отправителя ['ip1.email.dns-shop.ru']\n
                    dict['header']['received_ip'][] - IP адрес(а) отправителя (цепочки) ['185.31.80.190']\n
                    dict['header']['date'] - Дата отправки\n
                    dict['header']['subject'] - Тема письма\n

                    dict['header']:
                        dict['header']['header']['message-id'] - Id письма, можно достать Uid ['40227=d46c7fba-9b87-4029-acf8-6e2e9329226d=-2=10338015@links.email.dns-shop.ru']\n

    """
    parsed_messages = []
    URLParser = URLExtract()
    ep = eml_parser.EmlParser()

    for file in eml_files:
        # Парсим файлы, создаем словари, заполняем массив
        (msg, parsed_msg) = ep.decode_email_bytes(file)
        body = "" # НАДО ДОБАВИТЬ ПРОВЕРКУ ENCODING
        if msg.is_multipart():
            #body = h2t.html2text(msg.get_payload()[-1].get_payload()[-1])
            body = msg.get_payload()[-1].get_payload()[-1]
            while not isinstance(body, str):
                body = body.get_payload()[-1]
            body = h2t.html2text(body)
        else:
            try:
                body = h2t.html2text(msg.get_payload(decode=True).decode(encoding='cp1252'))
            except:
                body = "None"

        parsed_msg['header']['urls'] = set(URLParser.find_urls(body))
        parsed_msg['header']['text'] = body
        
        parsed_messages.append(parsed_msg)
    return parsed_messages
    

