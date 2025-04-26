from flask import Flask, render_template, request, redirect, url_for
import os
from imgapi import get_image_url
from keywords import keyword_extraction

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    keywords = []
    if 'file' in request.files:
        subject = request.form.get('subject')
        level = request.form.get('level')
        uploaded_file = request.files['file']
        knum = int(request.form.get('images'))
        if uploaded_file.filename.endswith('.txt'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                notes_content = f.read()
            
            keywords = keyword_extraction(notes_content, knum)
            keywords = keywords[0:min(len(keywords), knum)]
    img_urls = []
    for kw in keywords:
        img_urls.append(get_image_url(kw + subject + level))
    
    return render_template('results.html', img_urls=img_urls, keywords=keywords)

if __name__ == '__main__':
    app.run()