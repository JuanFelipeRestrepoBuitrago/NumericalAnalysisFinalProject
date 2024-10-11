// Inicializar el applet de GeoGebra
function initializeGeoGebra(expression = null, root = null) {
    const ggbApp = new GGBApplet({
        appName: "graphing",
        width: 800,
        height: 400,
        showToolBar: false,
        showAlgebraInput: false,
        showMenuBar: false,
        enableRightClick: false,
        enableShiftDragZoom: true,
        showResetIcon: true,
        language: "es",
        showZoomButtons: true,
        capturingThreshold: null,
        enableFileFeatures: true,
        appletOnLoad: function () {
            if (expression) {
                // Graficar la función ingresada
                ggbApplet.evalCommand(`f(x) = ${expression}`);
            }
            if (root !== null) {
                // Graficar el punto raíz si existe
                ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);
                ggbApplet.evalCommand(`SetPointStyle(RootPoint, 3)`);  // Cambia el estilo del punto
                ggbApplet.evalCommand(`SetPointSize(RootPoint, 5)`);   // Aumenta el tamaño del punto
            }
        }
    }, true);
    ggbApp.inject('geogebra');  // Inyecta el gráfico en el contenedor 'geogebra'
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeGeoGebra();
};

function calculateFalseRule() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let final = parseFloat(document.getElementById('final').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value; // Tipo de error
    let precisionInput = document.getElementById('precision').value; // Obtener precisión

    // Crear objeto de datos para la API
    let data = {
        expression: expression,
        error_type: error_type,
        tolerance: tolerance,
        max_iterations: max_iterations,
        initial: initial,
        final: final
    };

    if (precisionInput !== "" && precisionInput !== null) {
        data.precision = parseInt(precisionInput);
    }

    // Define el token de autenticación
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg0OTYyNjQsImlhdCI6MTcyODMyMzQ2NCwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.VbzqMestAYMgOSIW-Bg5lF179l-aVu3ZqSujniYXUx4";

    // Realizar solicitud POST a la API
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/false_rule/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Si la respuesta no es OK, intenta obtener el mensaje de error en JSON
        if (!response.ok) {
            return response.json().then(err => {
                throw err;  // Lanza el error para ser capturado en el catch
            });
        }
        return response.json();  // Parsear la respuesta a JSON si es exitosa
    })
    .then(result => {
        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = ''; // Limpiar resultados anteriores

        // Verificar la estructura y existencia de las propiedades antes de llenar la tabla
        if (result.Iterations && result.Xn && result.Fx && result.Error) {
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

        // Mostrar mensaje de la raíz
        let rootMessage = document.getElementById('rootMessage');
        if (result.Message) {
            rootMessage.textContent = result.Message;
        } else {
            rootMessage.textContent = "No se encontró un mensaje de raíz.";
        }

        // Obtener la raíz final
        let root = result.Xn[result.Xn.length - 1];

        // Actualizar el gráfico con la nueva función y la raíz
        initializeGeoGebra(expression, root);

    })
    .catch(error => {
        // Manejo de errores
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
