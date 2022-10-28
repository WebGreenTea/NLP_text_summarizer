from flask import Flask,render_template,request,redirect
from transformers import pipeline
import torch
import pathlib
from datetime import datetime as date
import os
import PyPDF2
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# device = 0 if torch.cuda.is_available() else -1
# print('load model...')
# summarizer_bart_large_cnn = pipeline("summarization", model="facebook/bart-large-cnn",device=device)
# print('load model complete')
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn").to(device)


app = Flask(__name__)
def fileType(filename):
    filename = str(filename)
    temp = filename.split('.')
    return temp[len(temp)-1]
def pdfReader(path):
    text = []
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        text.append(pageObj.extractText())
    
    text = ' '.join(text)
    return text
def summaryProcess(articles):
    summarys = []
    for article in articles:
        print('tokenize....')
        tokens_input = tokenizer.encode("summarize: "+article, return_tensors='pt', max_length=512, truncation=True).to(device)
        print('ids....')
        ids = model.generate(tokens_input, min_length=80, max_length=120)
        print('summary....')
        summary = tokenizer.decode(ids[0], skip_special_tokens=True)
        summarys.append(summary)
    return summarys

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summary", methods=['POST'])
def summary():
    currentTime = str(date.now()).replace('.','_').replace(':','-')
    articles = request.form.getlist('articles')
    if(len(articles) != 0):#input with type
        filenames = ['']
        if(len(articles[0]) > 0):
            summarized = summaryProcess(articles)
            results = list(zip(filenames,summarized))
            return render_template("summary.html",results=results)
        return redirect("/")
    else:#input with files
        articles = []
        filenames = []
        if 'file[]' not in request.files:
            #flash('No file part')
            return render_template("index.html")
        files = request.files.getlist("file[]")
        for file in files:
            if file.filename == '':
                return redirect("/")
            if file:
                filename = file.filename
                filenames.append(filename)
                fileName_toSave = currentTime+'_'+filename
                path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/{fileName_toSave}"
                file.save(path)
                if(fileType(filename) == 'txt'):
                    print('txt')
                    f = open(path, 'r',encoding="utf-8")
                    txt = f.read()
                    articles.append(txt)
                elif(fileType(filename) == 'pdf'):
                    print('pdf')
                    txt = pdfReader(path)
                    articles.append(txt)

        summarized = summaryProcess(articles)
        results = list(zip(filenames,summarized))
        return render_template("summary.html",results=results)

@app.route("/myfiles")
def myfiles():
    
    return render_template('myfiles.html')

if __name__ == '__main__':
    app.run(debug=True)