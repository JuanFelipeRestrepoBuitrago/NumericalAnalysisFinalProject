from flask import render_template, redirect, url_for, request, jsonify, send_file
import requests
from app import app
import matplotlib
matplotlib.use('Agg')  # Configurar matplotlib para usar el backend 'Agg'
import matplotlib.pyplot as plt
import numpy as np

import io

API_URL = "http://localhost:8000/api/v1.3.0/backend_numerical_methods"

@app.route('/')
def home():
    return redirect(url_for('index_page'))

@app.route('/home')
def index_page():
    return render_template('home.html', url='/home')

@app.route('/metodos')
def metodos_page():
    return render_template('metodos.html', url='/metodos')

@app.route('/bisection', methods=['GET', 'POST'])
def calculate_bisection():
    if request.method == 'POST':
        try:
            data = {
                "expression": request.form['expression'],
                "error_type": request.form.get('error_type', 'absolute'),
                "tolerance": float(request.form['tolerance']),
                "max_iterations": int(request.form['max_iterations']),
                "precision": int(request.form.get('precision', 16)),
                "initial": float(request.form['initial']),
                "final": float(request.form['final'])
            }
            # Enviar los datos a la API y procesar
            response = requests.post(f"{API_URL}/methods/bisection/", json=data)
            response.raise_for_status()
            result = response.json()  # Obtener los resultados de la API

            return render_template('bisection.html', result=result, message=result.get('Message', ''))
        except (ValueError, KeyError) as e:
            return f"Error en los datos del formulario: {e}", 400
        except requests.exceptions.RequestException as e:
            return f"Error al conectarse a la API: {e}", 500
        except Exception as e:
            return f"Error desconocido: {e}", 500
    else:
        return render_template('bisection.html', url='/bisection')


@app.route('/graphing')
def graphing():
    return render_template('graphing.html')

@app.route('/false_rule', methods=['GET'])
def false_rule_page():
    return render_template('false_rule.html')

@app.route('/fixed_point', methods=['GET'])
def fixed_point_page():
    return render_template('fixed_point.html')

@app.route('/secant')
def secant_page():
    return render_template('secant.html')

# Ruta para la página del método Newton-Raphson
@app.route('/newton_raphson')
def newton_raphson_page():
    return render_template('newton_raphson.html')

@app.route('/first_modified_newton')
def first_modified_newton_page():
    return render_template('first_modified_newton.html')


@app.route('/second_modified_newton', methods=['GET'])
def second_modified_newton_page():
    return render_template('second_modified_newton.html')


# Nueva ruta para la guía de expresiones
@app.route('/guia')
def guia_page():
    return render_template('guia.html')