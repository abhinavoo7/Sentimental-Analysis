from flask import Flask, render_template, request
import os
import re
import string
from textblob import TextBlob


Uploads = os.path.join('static', 'Uploads')
app = Flask(__name__)
app.config['uploads'] = Uploads    

def cleaning(content):    
    content = re.sub('\n', ' ', content)
    content = "".join([char for char in content if char not in string.punctuation])
    content = re.sub('[0-9]*', '', content)
    content = content.lower()
    return content

def sentimentf (text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0 :
      return 'Positive'
    elif pol < 0 :
      return 'Negative'
    else:
        return 'Neutral'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    file = ""
    if request.method=='POST':
        file = request.files["file"]
        app.config["file"] = "E:/Sentiment Analyzer/static/Uploads"
        file.save(os.path.join(app.config["file"], file.filename))
        fh = open(os.path.join(app.config["file"], file.filename), encoding="utf8")
        text = fh.read()
        content = text.split('\n')
        text = cleaning(text)          
        Sentiment = sentimentf(text)
        
        sent = []
        for line in content:
            line = cleaning(line)
            sent.append(sentimentf(line))
                
        count = {}
        for val in sent:
            count[val] = count.get(val,0) + 1 
                  
        Sentiment = Sentiment 
        fh.close() 
        os.remove('E:/Sentiment Analyzer/static/Uploads/' + file.filename)           
        
    return render_template('index.html', Sentiment = Sentiment, count = count)  

app.run(debug=True)
