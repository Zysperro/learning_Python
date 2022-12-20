import MailParser as mp
import flask
import os
import shutil
from os import walk
import werkzeug

app = flask.Flask('MailApp', template_folder='./venv/templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.secret_key = os.urandom(24)

eml_files = []
eml_files_path = './venv/UploadFiles/' #"C:/Users/user/source/repos/SpamFilterProject/SpamFolder/"
ALLOWED_EXTENSIONS = {'eml'}
mail_address = "Rashat03@yandex.ru"
mail_pass = ""
mail_domain = "yandex.ru"
selectedMessage = []
selectedMessageText = ""
selectedMessageSubject = "Тема выбранного письма"
messages = list()

@app.route('/', methods=['POST', 'GET'])
def show_index_page():
    global selectedMessageText
    global selectedMessageSubject
    global messages
    messages.clear()

    #if flask.request.method == 'POST':
    #    selectmsg()
    #eml_files = get_eml_files(eml_files_path)
    #messages = get_email()
    #messages = mp.Get_Parsed_EML_Messages(eml_files)
    #try:
    #    selectedMessageText = messages[1]['body']
    #except Exception as e:
    #    print(e)
    return flask.render_template('index.html', selectedMessageF = selectedMessage, inbox = messages, selectedMessageHTML = selectedMessageText, selectedMessageSubjectF = selectedMessageSubject)

# Выбор письма и открытие его
@app.route('/selectmsg', methods=['POST'])
def selectmsg():
    global selectedMessage
    global selectedMessageText
    global selectedMessageSubject
    global messages
    selectedMessageSubject = flask.request.form['messsageListItem']
    try:
        for msg in messages:
            if(msg['header']['subject'] == selectedMessageSubject):
                selectedMessage.clear()
                selectedMessage.append(msg)
                selectedMessageText = msg['header']['html']
    except Exception as e:
        print(f'Couldn\'t load HTML msg: {e}')
    return flask.render_template('index.html', inbox = messages, selectedMessageF = selectedMessage, selectedMessageHTML = selectedMessageText, selectedMessageSubjectF = selectedMessageSubject)

def get_email():
    return mp.Get_Messages_From_Mail(mail_address, mail_pass, mail_domain)

def clean_folder():
    for filename in os.listdir(eml_files_path):
        file_path = os.path.join(eml_files_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_files', methods=['POST', 'GET'])
def get_files():
    clean_folder()
    global eml_files
    global messages
    if flask.request.method == 'GET':
        return flask.render_template('index.html', inbox = messages, selectedMessageHTML = selectedMessageText, selectedMessageSubjectF = selectedMessageSubject)

    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            print('No file part')
            flask.flash('No file part')
            return flask.redirect(flask.request.url)
        upload_files = flask.request.files.getlist("file")
        for file in upload_files:
            if file.filename == '':
                print('No selected file')
                flask.flash('No selected file')
                return flask.redirect(flask.request.url)
            if file and allowed_file(file.filename):
                filename = werkzeug.utils.secure_filename(file.filename)
                file.save(os.path.join(eml_files_path, filename))
                print(file.filename)
        eml_files = get_eml_files(eml_files_path)
        messages = mp.Get_Parsed_EML_Messages(eml_files)
    return flask.render_template('index.html', inbox = messages, selectedMessageHTML = selectedMessageText, selectedMessageSubjectF = selectedMessageSubject)

@app.route('/get_mail', methods=['POST'])
def get_mail():
    # Загрузка писем из почты
    global messages
    global mail_domain
    global mail_address
    global mail_pass
    print(flask.request.form['userpw'])
    print(flask.request.form['username'])
    print(flask.request.form['providerList'])
    mail_domain = flask.request.form['providerList']
    mail_address = flask.request.form['username']
    mail_pass = flask.request.form['userpw']
    messages = get_email()
    return flask.render_template('index.html', inbox = messages, selectedMessageHTML = selectedMessageText, selectedMessageSubjectF = selectedMessageSubject)


def get_eml_files(folder_path):
    eml_files_list = []
    eml_paths_list = []

    for (dirpath, dirnames, filenames) in walk(folder_path):
        eml_paths_list.extend(filenames)
        break
    for file in eml_paths_list:
        if(file.endswith('meta')):
            continue
        #print(file)
        with open(folder_path+file, 'rb') as f:
            eml_files_list.append(f.read())

    return eml_files_list

if __name__ == '__main__':  
    app.run('0.0.0.0', port=9979, debug=True)
