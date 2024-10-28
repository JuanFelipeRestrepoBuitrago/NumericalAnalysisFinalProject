// Función para formatear la expresión para GeoGebra
function formatExpressionForGeoGebra(expression) {
    return expression
        .replace(/\*\*/g, "^")  // Reemplaza ** por ^ para exponentes en GeoGebra
        .replace(/Math\.sqrt/g, "sqrt")  // Asegura que sqrt se usa correctamente
        .replace(/Math\.sin/g, "sin")   // Reemplaza funciones trigonométricas
        .replace(/Math\.cos/g, "cos")
        .replace(/Math\.tan/g, "tan")
        .replace(/Math\.log/g, "log");  // Logaritmo natural en GeoGebra
}

// Inicializar el applet de GeoGebra
function initializeGeoGebra(expression = "x^2-4", root = null) {
    const formattedExpression = formatExpressionForGeoGebra(expression);

    console.log("Expresión enviada a GeoGebra: ", formattedExpression);

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
            ggbApplet.evalCommand(`f(x) = ${formattedExpression}`);
            
            if (root !== null) {
                ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);
                ggbApplet.evalCommand(`SetPointStyle(RootPoint, 3)`);
                ggbApplet.evalCommand(`SetPointSize(RootPoint, 5)`);
            }
        }
    }, true);
    
    ggbApp.inject('geogebra');
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeApp();  // Inicializar aplicación con token y configuración
};

let apiToken;

// Inicializar la aplicación y cargar el token
async function initializeApp() {
    await fetchApiToken();
    initializeGeoGebra();
}

// Obtener el token de la API al cargar la página
function fetchApiToken() {
    return fetch('/config')
        .then(response => response.json())
        .then(config => {
            apiToken = `${config.token_type} ${config.access_token}`;
        })
        .catch(error => console.error('Error al obtener el token:', error));
}

// Función que se llama al enviar el formulario
function calculateSecant() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let second_initial = parseFloat(document.getElementById('second_initial').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Crear el objeto de datos para enviar a la API
    let data = {
        "expression": expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "second_initial": second_initial
    };

    if (precisionInput !== "" && precisionInput !== null) {
        data.precision = parseInt(precisionInput);
    }

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/secant/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(result => {
        console.log(result);

        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = '';  

        // Verificar la estructura y existencia de las propiedades antes de llenar la tabla
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
        } else {
            console.error('Estructura de respuesta incorrecta. Algunas propiedades están indefinidas.');
            alert('Error: La estructura de la respuesta de la API no es la esperada.');
        }

        // Mostrar el mensaje de la raíz de la función en el contenedor
        let rootMessage = document.getElementById('rootMessage');
        let root = null;
        if (result.Message) {
            rootMessage.textContent = result.Message;
            root = result.Xn[result.Xn.length - 1];
        } else {
            rootMessage.textContent = "No se encontró un mensaje de raíz.";
        }

        // Actualizar el gráfico con la nueva función y la raíz aproximada
        initializeGeoGebra(expression, root);
    })
    .catch(error => {
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'block';
        if (typeof error.detail === 'string') {
            errorMessageElement.textContent = error.detail;
        } else if (Array.isArray(error.detail) && error.detail[0].msg) {
            errorMessageElement.textContent = error.detail[0].msg;
        } else {
            errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';
        }
        errorMessageElement.style.textAlign = 'center';
    });
}
