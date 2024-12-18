const maxSize = 6;
let apiToken;

// Llama a fetchApiToken y espera su finalización antes de cualquier llamada a la API
async function initializeApp() {
   await fetchApiToken();
   // Ahora puedes iniciar cualquier otra funcionalidad que dependa del token
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
fetchApiToken();

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

    // Realizar la solicitud POST a la API con el token cargado desde el archivo .env
    fetch("http://localhost:8000/api/v1.5.0/backend_numerical_methods/methods/bisection/",
         {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken // Aquí se usa el token completo
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
                row.insertCell(0).textContent = iteration;
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


// Función para descargar el gráfico como SVG
function downloadGeoGebraSVG() {
    if (typeof ggbApplet !== 'undefined' && typeof ggbApplet.exportSVG === 'function') {
        ggbApplet.exportSVG(svgContent => {
            if (svgContent.startsWith('<svg')) {
                const link = document.createElement('a');
                link.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent);
                link.download = 'geogebra_graph.svg';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else {
                alert("Error: El contenido exportado no es un SVG válido.");
            }
        });
    } else {
        alert('No se pudo exportar el SVG. Verifica la disponibilidad de la API de GeoGebra.');
    }
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeGeoGebra();
}
