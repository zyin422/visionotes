from flask import Flask, render_template, request
import os
import serpapi
import requests
from imgapi import get_image_url
from keywords import keyword_extraction

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # folder to store uploaded files

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    img_urls = []
    notes_content = ''
    keywords = []
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename.endswith('.txt'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    notes_content = f.read()
                    keywords = keyword_extraction(notes_content)
            
            for i in range(min(len(keywords), 3)):
                img_urls.append(get_image_url(keywords[i]))
            
            
            


    return render_template('index.html', img_urls=img_urls, notes_content=notes_content, keywords=keywords)
if __name__ == '__main__':
    app.run()
