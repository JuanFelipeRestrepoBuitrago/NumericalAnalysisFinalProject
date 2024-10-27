// Función para inicializar el applet de GeoGebra
function initializeGeoGebra(expression, derivative_expression = null, root = null) {
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
            if (derivative_expression !== null) {
                ggbApplet.evalCommand(`g(x) = ${derivative_expression}`);
            }
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

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeGeoGebra('x^3 - x - 2');
};

// Función para obtener el token de autenticación desde '/config'
async function getTokenFromConfig() {
    const response = await fetch('/config');
    const config = await response.json();
    return `${config.token_type} ${config.access_token}`;
}

async function calculateModifiedNewton() {
    const expression = document.getElementById('expression').value;
    let derivative_expression = document.getElementById('derivative_expression').value;
    const initial = parseFloat(document.getElementById('initial').value);
    const tolerance = parseFloat(document.getElementById('tolerance').value);
    const max_iterations = parseInt(document.getElementById('max_iterations').value);
    const error_type = document.getElementById('error_type').value;
    const multiplicity = parseInt(document.getElementById('multiplicity').value);

    if (derivative_expression === "" || derivative_expression === null) {
        derivative_expression = calculateDerivative(expression);
        if (!derivative_expression) {
            alert("No se pudo calcular la derivada de la función proporcionada.");
            return;
        }
    }

    const data = {
        "expression": expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "multiplicity": multiplicity,
        "derivative_expression": derivative_expression
    };

    try {
        const token = await getTokenFromConfig();

        const response = await fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/first_modified_newton_method/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": token
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error(`Error en la solicitud: ${response.statusText}`);

        const result = await response.json();

        const resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = '';

        if (result.Iterations && result.Xn && result.Fx && result.Error) {
            result.Iterations.forEach((iteration, index) => {
                let row = resultsTable.insertRow();
                row.insertCell(0).textContent = iteration + 1;
                row.insertCell(1).textContent = result.Xn[index];
                row.insertCell(2).textContent = result.Fx[index];
                row.insertCell(3).textContent = result.Error[index];
            });

            let root = result.Xn[result.Xn.length - 1];
            initializeGeoGebra(expression, derivative_expression, root);

        } else {
            console.error('Estructura de respuesta incorrecta. Algunas propiedades están indefinidas.');
            alert('Error: La estructura de la respuesta de la API no es la esperada.');
        }

        document.getElementById('rootMessage').textContent = result.Message || "No se encontró un mensaje de raíz";

    } catch (error) {
        console.error('Error en la solicitud:', error);
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'block';
        errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';
        errorMessageElement.style.textAlign = 'center';
    }
}
