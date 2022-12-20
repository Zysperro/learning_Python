import eml_parser
import email
import quopri
import html2text as h2t
from urlextract import URLExtract
import imaplib
import base64

from os import walk

path = './SpamFolder/'
out_path = './OutputMsgs/'

def Get_Messages_From_Mail(mail_address: str, mail_pass:str, server_domain:str):
    """ Функция получения писем из email

    Args: 
        mail_address: Адрес почты
        mail_pass: Пароль от почты
        server_domain: адрес imap сервера (yandex.ru / google.com / mail.ru...)

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
    host = f'imap.{server_domain}'
    print(host)
    imap = imaplib.IMAP4_SSL(host)
    imap.login(mail_address, mail_pass)
    imap.select("INBOX")
    (inbox, data) = imap.search(None, 'ALL')
    for num in data[0].split():
        (typ, data) = imap.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                #f = email.message_from_bytes(response_part[1])
                #file = f.as_bytes()
                #print(file)
                (msg, parsed_msg) = ep.decode_email_bytes(response_part[1])
                body = "" # НАДО ДОБАВИТЬ ПРОВЕРКУ ENCODING
                html_body = ""
                if msg.is_multipart():
                    body = msg
                    #while isinstance(body, email.message.Message):
                    #while body.is_multipart():
                    for part in body.walk():
                        if part.get_content_type() == 'text/html':
                            html_body = part.get_payload()
                            print(part['Content-Transfer-Encoding'])
                            if 'base64' in part['Content-Transfer-Encoding']:
                                html_body = base64.b64decode(html_body).decode()
                            if 'quoted-printable' in part['Content-Transfer-Encoding']:
                                try:
                                    html_body = quopri.decodestring(html_body).decode('utf-8')
                                except Exception as e:
                                    print(f'Cant decode in UTF8 Q-P: {e}')
                                try:
                                    html_body = quopri.decodestring(html_body).decode('windows-1251')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')
                                try:
                                    html_body = quopri.decodestring(html_body).decode('koi8-r')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')    
                            parsed_msg['header']['html'] = html_body
                        if part.get_content_type() == 'text/plain':
                            text_body = part.get_payload()
                            print(type(text_body))
                            print(part['Content-Transfer-Encoding'])
                            if 'base64' in part['Content-Transfer-Encoding']:
                                text_body = base64.b64decode(text_body).decode()
                            if 'quoted-printable' in part['Content-Transfer-Encoding']:
                                print(part['Content-Type'])
                                try:
                                    text_body = quopri.decodestring(text_body).decode('utf-8')
                                except Exception as e:
                                    print(f'Cant decode in UTF8 Q-P: {e}')
                                try:
                                    text_body = quopri.decodestring(text_body).decode('windows-1251')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')
                                try:
                                    text_body = quopri.decodestring(text_body).decode('koi8-r')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')
                                print(type(text_body))
                            parsed_msg['header']['text'] = text_body
                            parsed_msg['header']['urls'] = set(URLParser.find_urls(text_body))
                    #html_body = body
                    #body = h2t.html2text(body)
                else:
                        html_body = msg.get_payload()
                        if msg.get_content_type() == 'text/html' or 'text/plain':
                            if 'base64' in msg['Content-Transfer-Encoding']:
                                html_body = base64.b64decode(html_body).decode()
                            if 'quoted-printable' in part['Content-Transfer-Encoding']:
                                try:
                                    html_body = quopri.decodestring(html_body).decode('utf-8')
                                except Exception as e:
                                    print(f'Cant decode in UTF8 Q-P: {e}')
                                try:
                                    html_body = quopri.decodestring(html_body).decode('windows-1251')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')
                                try:
                                    html_body = quopri.decodestring(html_body).decode('koi8-r')
                                except Exception as e:
                                    print(f'Cant decode in win-1251 Q-P: {e}')
                        else:
                            html_body = "Неподдерживаемый формат"
                        parsed_msg['header']['html'] = html_body
                        parsed_msg['header']['text'] = html_body
                        parsed_msg['header']['urls'] = set(URLParser.find_urls(html_body))
                print('Adding msg')
                parsed_messages.append(parsed_msg)
    return parsed_messages


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
        if file is None:
            continue
        # Парсим файлы, создаем словари, заполняем массив
        # (msg, parsed_msg) = ep.decode_email_bytes(file)
        # body = ""
        # html_body = ""
        # try:
        #     #if not msg is None:
        #     #    body = msg.get_payload(decode=True).decode()
        #     #else:
        #     msg = email.message_from_bytes(file)
        #     for part in msg.walk():
        #         if part.get_content_type() == 'text/html':
        #             body = part.get_payload()
        #     #print(body)
        #     #parsed_msg['body'] = body
        #     print("Got msg from file.")
        # except Exception as e:
        #     print(f"Couldn't get msg from file: {e} : {email.message_from_bytes(file)['subject']}")
        # parsed_msg['header']['urls'] = set(URLParser.find_urls(body))
        # parsed_msg['body'] = body

        #===========================
        (msg, parsed_msg) = ep.decode_email_bytes(file)
        body = "" # email.message.Message
        text_body = ""
        html_body = ""
        msg = email.message_from_bytes(file)

        if msg.is_multipart():
            body = msg
            #while isinstance(body, email.message.Message):
            #while body.is_multipart():
            for part in body.walk():
                if part.get_content_type() == 'text/html':
                    html_body = part.get_payload()
                    print(part['Content-Transfer-Encoding'])
                    if 'base64' in part['Content-Transfer-Encoding']:
                        html_body = base64.b64decode(html_body).decode()
                    if 'quoted-printable' in part['Content-Transfer-Encoding']:
                        try:
                            html_body = quopri.decodestring(html_body).decode('utf-8')
                        except Exception as e:
                            print(f'Cant decode in UTF8 Q-P: {e}')
                        try:
                            html_body = quopri.decodestring(html_body).decode('windows-1251')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')
                        try:
                            html_body = quopri.decodestring(html_body).decode('koi8-r')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')    
                    parsed_msg['header']['html'] = html_body
                if part.get_content_type() == 'text/plain':
                    text_body = part.get_payload()
                    print(type(text_body))
                    print(part['Content-Transfer-Encoding'])
                    if 'base64' in part['Content-Transfer-Encoding']:
                        text_body = base64.b64decode(text_body).decode()
                    if 'quoted-printable' in part['Content-Transfer-Encoding']:
                        print(part['Content-Type'])
                        try:
                            text_body = quopri.decodestring(text_body).decode('utf-8')
                        except Exception as e:
                            print(f'Cant decode in UTF8 Q-P: {e}')
                        try:
                            text_body = quopri.decodestring(text_body).decode('windows-1251')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')
                        try:
                            text_body = quopri.decodestring(text_body).decode('koi8-r')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')
                        print(type(text_body))
                    parsed_msg['header']['text'] = text_body
                    parsed_msg['header']['urls'] = set(URLParser.find_urls(text_body))
            #html_body = body
            #body = h2t.html2text(body)
        else:
                html_body = msg.get_payload()
                if msg.get_content_type() == 'text/html' or 'text/plain':
                    if 'base64' in msg['Content-Transfer-Encoding']:
                        html_body = base64.b64decode(html_body).decode()
                    if 'quoted-printable' in part['Content-Transfer-Encoding']:
                        try:
                            html_body = quopri.decodestring(html_body).decode('utf-8')
                        except Exception as e:
                            print(f'Cant decode in UTF8 Q-P: {e}')
                        try:
                            html_body = quopri.decodestring(html_body).decode('windows-1251')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')
                        try:
                            html_body = quopri.decodestring(html_body).decode('koi8-r')
                        except Exception as e:
                            print(f'Cant decode in win-1251 Q-P: {e}')
                else:
                    html_body = "Неподдерживаемый формат"
                parsed_msg['header']['html'] = html_body
                parsed_msg['header']['text'] = html_body
                parsed_msg['header']['urls'] = set(URLParser.find_urls(html_body))

        last_msg = body
        # for i in range(1):
        #     part = last_msg
        #     #print(part['Content-Type'])
        #     if 'text/html' in part['Content-Type']:
        #         html_body = part.get_payload()
        #         print(part['Content-Transfer-Encoding'])
        #         if 'base64' in part['Content-Transfer-Encoding']:
        #             html_body = base64.b64decode(html_body).decode()
        #         if 'quoted-printable' in part['Content-Transfer-Encoding']:
        #             html_body = quopri.decodestring(html_body)
        #         parsed_msg['header']['html'] = html_body
        #     if 'text/plain' in part['Content-Type']:
        #         text_body = part.get_payload()
        #         print(part['Content-Transfer-Encoding'])
        #         if 'base64' in part['Content-Transfer-Encoding']:
        #             text_body = base64.b64decode(text_body).decode()
        #         if 'quoted-printable' in part['Content-Transfer-Encoding']:
        #             text_body = quopri.decodestring(text_body)   

        # parsed_msg['header']['urls'] = set(URLParser.find_urls(text_body))
        # parsed_msg['header']['text'] = text_body
        # parsed_msg['header']['html'] = html_body

        parsed_messages.append(parsed_msg)

        #===========================

        #parsed_messages.append(parsed_msg)
    return parsed_messages
    

