
from flask import Flask, render_template, request, redirect, url_for, jsonify
from tinydb import TinyDB
from flask_cors import CORS
from datetime import datetime
import joblib as jl
from tensorflow.keras.models import load_model
from datetime import datetime
import os
from pipeline import *

app = Flask(__name__)

db = TinyDB('banco.json')

model_path = os.path.join(os.path.dirname(__file__), 'lstm_btc_usd_model.h5')
lstm_model = load_model(model_path)

CORS(app)

@app.route('/ola')
def ola():
	return 'ola'


@app.route('/')
def root():
	db.insert({
		'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'route': '/',
		'message': 'Página de previsão acessada'
	})
	return render_template('index.html')


@app.route('/retreinar_modelo')
def retreinar_modelo():
	db.insert({
		'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'route': '/retreinar_modelo',
		'message': 'Página de retreinar modelo acessada'
	})
	return render_template('retreinar_modelo.html')


@app.route('/retrain', methods=['POST'])
def retrain():
	db.insert({
		'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'route': '/retrain',
		'message': 'Modelo retreinado'
	})
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	#retrain_model(start_date, end_date)
	return f"<p>Modelo retreinado com sucesso de {start_date} a {end_date}.</p>"

@app.route('/logs')
def logs():
	return render_template('logs.html')


@app.route('/get_logs')
def get_logs():
	a = ''
	for log in db.all():
		a += f'{log["date"]} - {log["message"]} <br>'
	return a

if __name__ == '__main__':
    	app.run(host='localhost', port=8000)
