const maxSize = 6; // Tamaño máximo de 6x6 para la matriz
let apiToken;

// Llama a fetchApiToken y espera su finalización antes de cualquier llamada a la API
async function initializeApp() {
    await fetchApiToken();
}

// Obtener el token y tipo de la API al cargar la página
function fetchApiToken() {
    return fetch('/config')
        .then(response => response.json())
        .then(config => {
            apiToken = `${config.token_type} ${config.access_token}`;
        })
        .catch(error => console.error('Error al obtener el token:', error));
}

// Llama a fetchApiToken cuando se cargue la página
initializeApp();

// Inicializar el applet de GeoGebra
function initializeGeoGebra(expression, g_expression, root = null) {
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
            // Graficar la función f(x) y g(x)
            ggbApplet.evalCommand(`f(x) = ${expression}`);
            ggbApplet.evalCommand(`g(x) = ${g_expression}`);

            if (root !== null) {
                // Graficar el punto raíz si existe
                ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);
                ggbApplet.evalCommand(`SetPointStyle(RootPoint, 3)`);  // Cambia el estilo del punto
                ggbApplet.evalCommand(`SetPointSize(RootPoint, 5)`);   // Aumenta el tamaño del punto
            }
        }
    }, true);
    ggbApp.inject('geogebra'); // Inyecta el gráfico en el contenedor 'geogebra'
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    // Inicializa con funciones por defecto
    initializeGeoGebra('cos(x)-x', 'cos(x)');
};

function calculateFixedPoint() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let g_expression = document.getElementById('g_expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Crear el objeto de datos para enviar a la API
    let data = {
        "expression": expression,
        "g_expression": g_expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial
    };

    // Agregar "precision" solo si el usuario lo ha proporcionado y no es null
    if (precisionInput !== "" && precisionInput !== null) {
        data.precision = parseInt(precisionInput);
    }

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/fixed_point/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw err;  // Lanzar el error para capturarlo en el bloque catch
            });
        }
        return response.json();  // Parsear la respuesta a JSON
    })
    .then(result => {
        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = '';

        // Verificar que las propiedades existan antes de acceder a ellas
        if (result.Iterations && result.Xn && result.Fx && result.Error) {
            // Iterar a través de las iteraciones y llenar la tabla
            result.Iterations.forEach((iteration, index) => {
                let row = resultsTable.insertRow();
                let xn = result.Xn[index];
                let fx = result.Fx[index];
                let error = result.Error[index];

                // Crear las celdas de la tabla
                let iterationCell = row.insertCell(0);  // Número de iteración
                let xnCell = row.insertCell(1);          // Valor de Xn
                let fxCell = row.insertCell(2);          // Valor de f(Xn)
                let errorCell = row.insertCell(3);       // Valor del error

                // Rellenar las celdas con los valores
                iterationCell.textContent = iteration + 1;  // Mostrar iteración comenzando desde 1
                xnCell.textContent = xn;
                fxCell.textContent = fx;
                errorCell.textContent = error;
            });
        } else {
            console.error('Estructura de respuesta incorrecta. Algunas propiedades están indefinidas.');
            alert('Error: La estructura de la respuesta de la API no es la esperada.');
        }

        // Mostrar el mensaje de la raíz de la función en el contenedor
        let rootMessage = document.getElementById('rootMessage');
        if (result.Message) {
            rootMessage.textContent = result.Message;
        } else {
            rootMessage.textContent = "No se encontró un mensaje de raíz.";
        }

        // Obtener la raíz final
        let root = result.Xn[result.Xn.length - 1];

        // Actualizar el gráfico con la nueva función y la raíz
        initializeGeoGebra(expression, g_expression, root);

    })
    .catch(error => {
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'block';

        // Mostrar el mensaje de error exacto devuelto por la API
        if (error.detail) {
            errorMessageElement.textContent = error.detail;  // Mostrar el string de error devuelto por la API
        } else {
            errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';  // Mensaje genérico si no hay detalle
        }

        errorMessageElement.style.textAlign = 'center';  // Centrar el mensaje de error
    });
}
