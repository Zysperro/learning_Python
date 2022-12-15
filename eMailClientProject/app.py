import MailParser as mp
import flask
from os import walk

app = flask.Flask('MailApp', template_folder='./venv/templates')
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

eml_files = []
eml_files_path = "C:/Users/user/source/repos/SpamFilterProject/SpamFolder/"

@app.route('/')
def show_index_page():
    eml_files = get_eml_files(eml_files_path)
    messages = mp.Get_Parsed_EML_Messages(eml_files)
    return flask.render_template('index.html', inbox = messages)

def get_eml_files(folder_path):
    eml_files_list = []
    eml_paths_list = []

    for (dirpath, dirnames, filenames) in walk(folder_path):
        eml_paths_list.extend(filenames)
        break
    for file in eml_paths_list:
        if(file.endswith('meta')):
            continue
        print(file)
        with open(folder_path+file, 'rb') as f:
            eml_files_list.append(f.read())

    return eml_files_list

if __name__ == '__main__':
    app.run('0.0.0.0', port=9979, debug=True)