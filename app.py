from flask import Flask
import pandas as pd
from VirtualThingFileGenarator import manage_files
app = Flask(__name__)
@app.route('/')
def hello_world():
    return """Hello, IT\'s an API what to do querys to ThingWeb\n
              \n************************************************\n
              \n***********************API**********************\n"""

@app.route('/limpar_arquivos')
def limpa_arquivos():
    #reset files contents
    rf = manage_files()
    return rf.reset_all_folders()

if __name__ == "__main__":
    app.run(debug=True)