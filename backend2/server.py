from flask import Flask, request
import model as ml
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app,supports_credentials=True)
y = "a"
z=""

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files
    # obj = files.getlist('pdf')
    # print(obj)
    # print(files)
    file = request.files['pdf']
    # print(file)
    file.save(os.path.join(os.getcwd(),file.filename))
    save_path= os.path.join(os.getcwd(),file.filename)
    # print(save_path)
    x = ml.read_pdf_file(save_path)
    global y
    global z
    y = x
    z= save_path
    chunks = ml.text_to_chunks(x)
    docsearch, chain = ml.processing_file(chunks,save_path)
    res = ml.question_answering2(docsearch,chain)
    print(res)
    dt="ans"
    obj={"s":"● Pdf Uploaded Successfully. Now You can ask question",dt:res}
    # return "● Pdf Uploaded Successfully. Now You can ask question" 
    return obj

@app.route('/senddata', methods=['POST'])
def get_data():
    print(request.json)
    a = request.json
    que = a["text"]
    print(que)
    global y
    global z
    chunks = ml.text_to_chunks(y)
    docsearch, chain = ml.processing_file(chunks,z)
    result = ml.question_answering(docsearch,chain,que)
    print(result)
    return result
    # return "Chapter+01+-+Inception.pdf"
if __name__ == '__main__':
    app.run(debug=True, port=5050)
