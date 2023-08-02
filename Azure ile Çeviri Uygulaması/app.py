import requests, os, uuid, json

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

@app.route('/', methods=['GET'])

def index():
    
    return render_template('index.html')

@app.route('/', methods=['POST'])

def index_post():

    # Formdaki değerleri okuma

    original_text = request.form['text']

    target_language = request.form['language']

    # .env'den değerleri yükleme

    key = os.environ['KEY']

    endpoint = os.environ['ENDPOINT']

    location = os.environ['LOCATION']

    # Çevirmek istenileni ve API sürümünü (3.0) ve hedef dili belirtme

    path = '/translate?api-version=3.0'

    # Hedef dil parametresini ekleme

    target_language_parameter = '&to=' + target_language

    # Tam URL'yi oluşturma

    constructed_url = endpoint + path + target_language_parameter

    # Abonelik anahtarını içeren başlık bilgilerini ayarlama

    headers = {

        'Ocp-Apim-Subscription-Key': key,

        'Ocp-Apim-Subscription-Region': location,

        'Content-type': 'application/json',

        'X-ClientTraceId': str(uuid.uuid4())

    }

    # Çevrilecek metinle request'in gövdesini oluşturma

    body = [{ 'text': original_text }]

    # Post'u kullanarak arama yapın

    translator_request = requests.post(constructed_url, headers=headers, json=body)

    # JSON yanıtını alma

    translator_response = translator_request.json()

    # Çeviriyi alma

    translated_text = translator_response[0]['translations'][0]['text']

    # Oluşturma şablonunu arama; çevrilmiş metni, orijinal metni ve hedef dili şablona iletme

    return render_template(

        'results.html',

        translated_text=translated_text,

        original_text=original_text,

        target_language=target_language
        
    )