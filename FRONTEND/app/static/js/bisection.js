function calculateBisection() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let final = parseFloat(document.getElementById('final').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Crear el objeto de datos para enviar a la API
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

    // Token para la autenticación
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjk4NjkwNDcsImlhdCI6MTcyOTY5NjI0NywidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.fjAK610XqTtiDN13UhihK_Wtc06l7Ni3Ybg0pT9-7Uo";

    // Realizar la solicitud POST a la API
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/bisection/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
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
        // Limpiar la tabla de resultados
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = '';

        // Rellenar la tabla si hay resultados
        if (result.Iterations && result.Xn && result.Fx && result.Error) {
            result.Iterations.forEach((iteration, index) => {
                let row = resultsTable.insertRow();
                row.insertCell(0).textContent = iteration + 1;
                row.insertCell(1).textContent = result.Xn[index];
                row.insertCell(2).textContent = result.Fx[index];
                row.insertCell(3).textContent = result.Error[index];
            });

            // Graficar la función con la raíz
            let root = result.Xn[result.Xn.length - 1];
            plotFunction(expression, root);
        }

        // Mostrar mensaje de la raíz
        let rootMessage = document.getElementById('rootMessage');
        rootMessage.textContent = result.Message || "No se encontró un mensaje de raíz.";
    })
    .catch(error => {
        // Manejo de errores
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'block';
        errorMessageElement.textContent = error.detail || 'Ocurrió un error al procesar la solicitud.';
        errorMessageElement.style.textAlign = 'center';
    });
}

// Inicializar el applet de GeoGebra
function initializeGeoGebra() {
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
            ggbApplet.evalCommand("f(x) = log(sin(x)^2 + 1) - (1/2)");
        }
    }, true);
    ggbApp.inject('geogebra');
}

// Graficar la función y marcar la raíz
function plotFunction(expression, root) {
    ggbApplet.evalCommand("Delete[f]");
    ggbApplet.evalCommand(`f(x) = ${expression}`);

    if (root !== null && root !== undefined) {
        ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);
        ggbApplet.evalCommand("SetPointStyle(RootPoint, 3)");
        ggbApplet.evalCommand("SetPointSize(RootPoint, 5)");
    }
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeGeoGebra();
}
