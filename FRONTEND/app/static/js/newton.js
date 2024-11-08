let apiToken;

// Inicializa la aplicación al cargar la página
async function initializeApp() {
    try {
        await fetchApiToken();
        initializeGeoGebra();
    } catch (error) {
        console.error('Error en la inicialización de la aplicación:', error);
    }
}

// Obtiene el token y tipo de la API al cargar la página
function fetchApiToken() {
    return fetch('/config')
        .then(response => response.json())
        .then(config => {
            apiToken = `${config.token_type} ${config.access_token}`;
        })
        .catch(error => console.error('Error al obtener el token:', error));
}

// Llama a initializeApp al cargar la página
initializeApp();

// Agrega un nuevo punto (x, y) en el formulario
function addPoint() {
    const container = document.getElementById('points-container');
    if (container.children.length >= 6) {  // Limitar a 6 puntos
        alert("No se pueden agregar más de 6 puntos.");
        return;
    }

    const pointDiv = document.createElement('div');
    pointDiv.className = 'mb-2';
    pointDiv.innerHTML = `
        <input type="number" class="vector-cello" name="x[]" placeholder="x" required>
        <input type="number" class="vector-cello" name="y[]" placeholder="y" required>
    `;
    container.appendChild(pointDiv);
}

// Remueve el último punto (x, y) en el formulario, manteniendo siempre al menos dos puntos
function removePoint() {
    const container = document.getElementById('points-container');
    if (container.children.length > 2) {
        container.removeChild(container.lastChild);
    } else {
        alert("Debe haber al menos dos puntos (x, y).");
    }
}

// Función para calcular el método de Newton y graficar el polinomio y puntos
function calculateNewton() {
    const xInputs = document.querySelectorAll('input[name="x[]"]');
    const yInputs = document.querySelectorAll('input[name="y[]"]');
    const xValues = Array.from(xInputs).map(input => parseFloat(input.value));
    const yValues = Array.from(yInputs).map(input => parseFloat(input.value));

    if (xValues.length < 2 || yValues.length < 2 || xValues.includes(NaN) || yValues.includes(NaN)) {
        alert("Por favor, rellena todos los campos de los puntos (x, y).");
        return;
    }

    const precision = document.getElementById('precision').value ? parseInt(document.getElementById('precision').value) : 16;

    const data = {
        x: xValues,
        y: yValues,
        precision: precision
    };

    fetch("http://localhost:8000/api/v1.5.0/backend_numerical_methods/interpolation/newton/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err });
        }
        return response.json();
    })
    .then(result => {
        displayResults(result, xValues, yValues);
        plotPolynomialAndPointsInGeoGebra(result.polynomial, xValues, yValues);
    })
    .catch(error => handleError(error));
}

// Muestra los resultados en formato LaTeX, incluyendo la tabla de diferencias
function displayResults(result, xValues, yValues) {
    let polynomialLatex = result.polynomial
        .replace(/\*\*([0-9]+)/g, "^{$1}") // Convierte **n a ^{n} para LaTeX
        .replace(/\s?\*\s?/g, "");       // Elimina * y espacios antes de variables

    polynomialLatex = `\\( ${polynomialLatex} \\)`;

    const coefficientsLatex = `
        \\[
        \\begin{bmatrix}
        ${result.coefficients.join(' \\\\ ')}
        \\end{bmatrix}
        \\]
    `;

    // Construye la tabla de diferencias
    const tableHeader = `n & x_i & y = f[x_i] & ${[...Array(result.difference_table[0].length - 2).keys()].map(i => i + 1).join(' & ')} \\\\ \\hline`;
    const tableBody = result.difference_table.map((row, index) => {
        return `${index} & ${xValues[index]} & ${yValues[index]} & ${row.slice(2).join(' & ')}`;
    }).join(" \\\\ ");

    const differenceTableLatex = `
        \\[
        \\begin{array}{c|c|c|${'c|'.repeat(result.difference_table[0].length - 2)}}
        ${tableHeader}
        ${tableBody}
        \\end{array}
        \\]
    `;

    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = `
        <h3>Polinomio:</h3> ${polynomialLatex}<br><br>
        <h3>Coeficientes:</h3> ${coefficientsLatex}
        <h3>Tabla de diferencias:</h3> ${differenceTableLatex}
    `;

    MathJax.typesetPromise();
}

// Inicializa GeoGebra
function initializeGeoGebra() {
    const ggbApp = new GGBApplet({
       "appName": "graphing",
       "width": 800,
       "height": 450,
       "showToolBar": false,
       "showAlgebraInput": true,
       "showMenuBar": false,
       "enableRightClick": false,
       "enableShiftDragZoom": true,
       "showResetIcon": false,
       "language": "es",
       "showZoomButtons": true,
       "capturingThreshold": null,
       "enableFileFeatures": true,
       "appletOnLoad": function () {
          console.log("GeoGebra cargado");
          ggbApplet.setVisible('algebra', true);
       }
    }, true);
    ggbApp.inject('geogebra');
}

// Graficar el polinomio y los puntos en GeoGebra
function plotPolynomialAndPointsInGeoGebra(polynomial, xValues, yValues) {
    ggbApplet.reset();
    
    // Graficar el polinomio
    ggbApplet.evalCommand(`f(x) = ${polynomial}`);
    
    // Graficar los puntos
    xValues.forEach((x, index) => {
        const y = yValues[index];
        ggbApplet.evalCommand(`P${index + 1} = (${x}, ${y})`);
    });

    ggbApplet.setCoordSystem(-20, 20, -20, 20);

    document.getElementById('geogebra-container').style.display = 'block';
    document.getElementById('downloadButton').style.display = 'block';
}

// Descargar el gráfico como SVG
function downloadGeoGebraSVG() {
    if (typeof ggbApplet !== 'undefined' && typeof ggbApplet.exportSVG === 'function') {
        ggbApplet.exportSVG(function (svgContent) {
            if (!svgContent || !svgContent.startsWith('<svg')) {
                alert("El contenido exportado no es un SVG válido.");
                return;
            }

            const link = document.createElement('a');
            link.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent);
            link.download = 'geogebra_graph.svg';
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    } else {
        alert('No se pudo exportar el SVG. Asegúrate de que la API de GeoGebra esté disponible.');
    }
}

function handleError(error) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.style.display = 'block';
    errorMessageElement.style.fontSize = '1.5em'; 
    errorMessageElement.style.color = 'red'; 
    errorMessageElement.style.textAlign = 'center';

    if (error && error.detail) {
        if (typeof error.detail === 'string') {
            errorMessageElement.textContent = error.detail;
        } else if (Array.isArray(error.detail) && error.detail[0].msg) {
            errorMessageElement.textContent = error.detail[0].msg;
        } else {
            errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';
        }
    } else {
        errorMessageElement.textContent = 'Ocurrió un error desconocido.';
    }
}
