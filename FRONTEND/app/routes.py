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

# Rutas para cada método

# Solving Systems by Graphing
@app.route('/graphing')
def graphing():
    return render_template('graphing.html', url='/graphing')

# Solving Equations of One Variable
@app.route('/function_evaluator')
def function_evaluator():
    return render_template('function_evaluator.html', url='/function_evaluator')

@app.route('/incremental_search')
def incremental_search():
    return render_template('incremental_search.html', url='/incremental_search')

@app.route('/bisection')
def bisection():
    
    return render_template('bisection.html', url='/bisection')

@app.route('/false_position')
def false_position():
    return render_template('false_position.html', url='/false_position')

@app.route('/fixed_point')
def fixed_point():
    return render_template('fixed_point.html', url='/fixed_point')

@app.route('/newton_raphson')
def newton_raphson():
    return render_template('newton_raphson.html', url='/newton_raphson')

@app.route('/secant')
def secant():
    return render_template('secant.html', url='/secant')

@app.route('/multiple_roots')
def multiple_roots():
    return render_template('multiple_roots.html', url='/multiple_roots')

# Solution of Systems of Equations
@app.route('/gaussian_elimination_simple')
def gaussian_elimination_simple():
    return render_template('gaussian_elimination_simple.html', url='/gaussian_elimination_simple')

@app.route('/gaussian_elimination_partial')
def gaussian_elimination_partial():
    return render_template('gaussian_elimination_partial.html', url='/gaussian_elimination_partial')

@app.route('/gaussian_elimination_total')
def gaussian_elimination_total():
    return render_template('gaussian_elimination_total.html', url='/gaussian_elimination_total')

@app.route('/direct_factorization_lu_simple')
def direct_factorization_lu_simple():
    return render_template('direct_factorization_lu_simple.html', url='/direct_factorization_lu_simple')

@app.route('/direct_factorization_lu_partial_pivot')
def direct_factorization_lu_partial_pivot():
    return render_template('direct_factorization_lu_partial_pivot.html', url='/direct_factorization_lu_partial_pivot')

@app.route('/croult')
def croult():
    return render_template('croult.html', url='/croult')

@app.route('/doolittle')
def doolittle():
    return render_template('doolittle.html', url='/doolittle')

@app.route('/cholesky')
def cholesky():
    return render_template('cholesky.html', url='/cholesky')

@app.route('/jacobi')
def jacobi():
    return render_template('jacobi.html', url='/jacobi')

@app.route('/gauss_seidel')
def gauss_seidel():
    return render_template('gauss_seidel.html', url='/gauss_seidel')

@app.route('/sor')
def sor():
    return render_template('sor.html', url='/sor')

# Interpolation
@app.route('/vandermonde')
def vandermonde():
    return render_template('vandermonde.html', url='/vandermonde')

@app.route('/newton_divided')
def newton_divided():
    return render_template('newton_divided.html', url='/newton_divided')

@app.route('/lagrange')
def lagrange():
    return render_template('lagrange.html', url='/lagrange')

@app.route('/spline')
def spline():
    return render_template('spline.html', url='/spline')
