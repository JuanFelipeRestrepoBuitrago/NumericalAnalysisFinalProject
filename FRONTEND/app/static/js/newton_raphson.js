// Función para inicializar el applet de GeoGebra
function initializeGeoGebra(expression, derivative_expression, root = null) {
    const ggbApp = new GGBApplet({
        "appName": "graphing",
        "width": 800,
        "height": 400,
        "showToolBar": false,
        "showAlgebraInput": false,
        "showMenuBar": false,
        "enableRightClick": false,
        "enableShiftDragZoom": true,
        "showResetIcon": true,
        "language": "es",
        "showZoomButtons": true,
        "capturingThreshold": null,
        "enableFileFeatures": true,
        "appletOnLoad": function () {
            ggbApplet.evalCommand(`f(x) = ${expression}`);
            ggbApplet.evalCommand(`g(x) = ${derivative_expression}`);

            if (root !== null) {
                ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);
                ggbApplet.evalCommand(`SetPointStyle(RootPoint, 3)`);
                ggbApplet.evalCommand(`SetPointSize(RootPoint, 5)`);
            }
        }
    }, true);
    ggbApp.inject('geogebra');
}

// Función para calcular la derivada automáticamente si no se proporciona
function calculateDerivative(expression) {
    try {
        let node = math.parse(expression);
        let derivative = math.derivative(node, 'x');
        return derivative.toString();
    } catch (error) {
        console.error("Error al derivar la función:", error);
        return null;
    }
}

// Inicializar GeoGebra al cargar la página con una función y su derivada
window.onload = function () {
    initializeGeoGebra('x^3 - x - 2', '3x^2 - 1');
};

// Función que se llama al enviar el formulario para calcular Newton-Raphson
function calculateNewtonRaphson() {
    let expression = document.getElementById('expression').value;
    let derivative_expression = document.getElementById('derivative_expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Calcular la derivada automáticamente si no se proporciona
    if (!derivative_expression) {
        derivative_expression = calculateDerivative(expression);
        if (!derivative_expression) {
            alert("No se pudo calcular la derivada de la función proporcionada.");
            return;
        }
    }

    let data = {
        "expression": expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "derivative_expression": derivative_expression
    };

    if (precisionInput) {
        data.precision = parseInt(precisionInput);
    }

    // Token de autenticación desde el archivo de configuración
    let token;
    fetch('/config')
        .then(response => response.json())
        .then(config => {
            token = `${config.token_type} ${config.access_token}`;

            return fetch("http://localhost:8000/api/v1.5.0/backend_numerical_methods/methods/newton_raphson/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": token
                },
                body: JSON.stringify(data)
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }
            return response.json();
        })
        .then(result => {
            console.log(result);

            let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
            resultsTable.innerHTML = ''; 

            if (result.Iterations && result.Xn && result.Fx && result.Error) {
                result.Iterations.forEach((iteration, index) => {
                    let row = resultsTable.insertRow();
                    let xi = result.Xn[index];
                    let fx = result.Fx[index];
                    let error = result.Error[index];

                    let iterationCell = row.insertCell(0);
                    let xiCell = row.insertCell(1);
                    let fxCell = row.insertCell(2);
                    let errorCell = row.insertCell(3);

                    iterationCell.textContent = iteration + 1;
                    xiCell.textContent = xi;
                    fxCell.textContent = fx;
                    errorCell.textContent = error;
                });

                let root = result.Xn[result.Xn.length - 1];
                initializeGeoGebra(expression, derivative_expression, root);

            } else {
                console.error('Estructura de respuesta incorrecta. Algunas propiedades están indefinidas.');
                alert('Error: La estructura de la respuesta de la API no es la esperada.');
            }

            let rootMessage = document.getElementById('rootMessage');
            rootMessage.textContent = result.Message || "No se encontró un mensaje de raíz.";
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            const errorMessageElement = document.getElementById('error-message');
            errorMessageElement.style.display = 'block';
            errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';
            errorMessageElement.style.textAlign = 'center';
        });
}
