from flask import render_template, redirect, url_for
from app import app

@app.route('/')
def home():
    return redirect(url_for('index_page'))

@app.route('/home')
def index_page():
    return render_template('home.html', url='/home')

@app.route('/metodos')
def metodos_page():
    return render_template('metodos.html', url='/metodos')
