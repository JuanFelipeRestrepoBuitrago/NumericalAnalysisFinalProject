const maxSize = 6; // Tamaño máximo de 6x6 para la matriz
let apiToken; // Variable global para el token de autenticación

// Inicializar la aplicación obteniendo el token de la API
async function initializeApp() {
    await fetchApiToken();
    initializeGeoGebra(); // Inicializar GeoGebra después de obtener el token
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

// Función para generar la matriz, el vector b y el vector de inicialización x0 basados en el tamaño ingresado
function generateMatrix() {
    const size = parseInt(document.getElementById('matrixSize').value);
    if (isNaN(size) || size < 2 || size > maxSize) {
        alert('Por favor ingresa un tamaño válido entre 2 y 6.');
        return;
    }
    document.getElementById('matrixInput').innerHTML = '';
    document.getElementById('vectorInput').innerHTML = '';
    document.getElementById('xInitialInput').innerHTML = '';
    generateMatrixInput(size);
    generateVectorInput('vectorInput', size);
    generateVectorInput('xInitialInput', size);
    applyInputRestrictions();
    hideGraphAndDownloadButton();
}

// Función para generar la matriz de coeficientes
function generateMatrixInput(size) {
    for (let i = 0; i < size; i++) {
        const matrixRow = document.createElement('tr');
        for (let j = 0; j < size; j++) {
            const matrixCell = document.createElement('td');
            matrixCell.innerHTML = '<input type="text" class="matrix-cell form-control" />';
            matrixRow.appendChild(matrixCell);
        }
        document.getElementById('matrixInput').appendChild(matrixRow);
    }
}

// Función para generar el vector b o el vector x0
function generateVectorInput(id, size) {
    for (let i = 0; i < size; i++) {
        const vectorRow = document.createElement('tr');
        const vectorCell = document.createElement('td');
        vectorCell.innerHTML = '<input type="text" class="vector-cell form-control" />';
        vectorRow.appendChild(vectorCell);
        document.getElementById(id).appendChild(vectorRow);
    }
}

// Función para aplicar restricciones a los inputs (solo permitir números)
function applyInputRestrictions() {
    document.querySelectorAll('input.matrix-cell, input.vector-cell').forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9.\-]/g, ''); // Solo permitir números y signos negativos
        });
    });
}

// Función para ocultar el gráfico y el botón de descarga
function hideGraphAndDownloadButton() {
    document.getElementById('geogebra-container').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'none';
}

// Función para obtener la matriz desde la tabla
function getMatrixFromTable() {
    const matrix = [];
    const rows = document.querySelectorAll('#matrixInput tr');
    rows.forEach(row => {
        const rowData = [];
        const cells = row.querySelectorAll('input.matrix-cell');
        cells.forEach(cell => rowData.push(parseFloat(cell.value)));
        matrix.push(rowData);
    });
    return matrix;
}

// Función para obtener un vector desde la tabla
function getVectorFromTable(id) {
    const vector = [];
    const cells = document.querySelectorAll(`#${id} input.vector-cell`);
    cells.forEach(cell => vector.push([parseFloat(cell.value)]));
    return vector;
}

// Función principal del método de Jacobi
function calculateJacobiMethod() {
    const matrix = getMatrixFromTable();
    const vectorB = getVectorFromTable('vectorInput');
    const xInitial = getVectorFromTable('xInitialInput');
    if (matrix.some(row => row.includes(NaN)) || vectorB.includes(NaN) || xInitial.includes(NaN)) {
        alert("Por favor, rellena todos los campos de la matriz, el vector y el vector inicial.");
        return;
    }
    const precision = document.getElementById('precision').value || 16;
    const maxIter = document.getElementById('max_iter').value || 100;
    const tol = document.getElementById('tolerance').value || 1e-7;
    const methodType = document.getElementById('method_type').value;
    const errorType = document.getElementById('error_type').value;

    const data = {
        A: matrix,
        b: vectorB,
        x_initial: xInitial,
        precision: parseInt(precision),
        max_iter: parseInt(maxIter),
        tol: parseFloat(tol),
        error_type: errorType,
        method_type: methodType
    };

    sendDataToAPI(data);
    if (matrix.length === 2 && matrix[0].length === 2) {
        plotSystemInGeoGebra(matrix, vectorB);
    } else {
        hideGraphAndDownloadButton();
    }
}

// Función para enviar los datos a la API
function sendDataToAPI(data) {
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/linear_equations_system/jacobi/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) throw response.json();
            return response.json();
        })
        .then(result => {
            displayResults(result);
            return fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/linear_equations_system/jacobi/spectral_radius_and_convergence/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": apiToken
                },
                body: JSON.stringify(data)
            });
        })
        .then(response => response.json())
        .then(convergenceResult => displayConvergenceAndSpectral(convergenceResult))
        .catch(error => handleError(error));
}

// Función para mostrar los resultados en la tabla
function displayResults(result) {
    const resultsTable = document.querySelector("#resultsTable tbody");
    const resultsTableHead = document.querySelector("#resultsTable thead");
    resultsTable.innerHTML = '';
    resultsTableHead.innerHTML = '';

    const iterations = result.iterations;
    const solutions = result.x;
    const errors = result.error;
    const numSolutions = solutions.length;

    const headerRow = document.createElement('tr');
    const headerIteration = document.createElement('th');
    headerIteration.textContent = 'Iteración';
    headerRow.appendChild(headerIteration);

    for (let i = 0; i < numSolutions; i++) {
        const headerX = document.createElement('th');
        headerX.textContent = `X${i + 1}`;
        headerRow.appendChild(headerX);
    }

    const headerError = document.createElement('th');
    headerError.textContent = 'Error';
    headerRow.appendChild(headerError);
    resultsTableHead.appendChild(headerRow);

    iterations.forEach((iteration, index) => {
        const newRow = document.createElement('tr');
        const cellIteration = document.createElement('td');
        cellIteration.textContent = iteration;
        newRow.appendChild(cellIteration);

        for (let i = 0; i < numSolutions; i++) {
            const cellXn = document.createElement('td');
            cellXn.textContent = solutions[i][index];
            newRow.appendChild(cellXn);
        }

        const cellError = document.createElement('td');
        cellError.textContent = errors[index];
        newRow.appendChild(cellError);
        resultsTable.appendChild(newRow);
    });
}

// Función para mostrar convergencia y espectro radial
function displayConvergenceAndSpectral(convergenceResult) {
    const convergenceMessage = document.getElementById('convergence-message');
    const spectralRadiusMessage = document.getElementById('spectral-radius-message');
    convergenceMessage.textContent = `Convergencia: ${convergenceResult.convergence || 'No disponible'}`;
    spectralRadiusMessage.textContent = `Espectro Radial: ${convergenceResult.spectral_radius || 'No disponible'}`;
}

// Función para manejar errores
function handleError(error) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = 'Ocurrió un error al calcular los resultados: ' + error;
}

// Función para graficar el sistema de ecuaciones en GeoGebra
function plotSystemInGeoGebra(matrix, vector) {
    const a1 = matrix[0][0], b1 = matrix[0][1], c1 = vector[0][0];
    const a2 = matrix[1][0], b2 = matrix[1][1], c2 = vector[1][0];
    const eq1 = `(${a1}) * x + (${b1}) * y = ${c1}`;
    const eq2 = `(${a2}) * x + (${b2}) * y = ${c2}`;

    ggbApplet.reset();
    ggbApplet.setVisible('algebra', true);
    ggbApplet.evalCommand(`ec1: ${eq1}`);
    ggbApplet.evalCommand(`ec2: ${eq2}`);
    ggbApplet.setCoordSystem(-10, 10, -10, 10);

    document.getElementById('geogebra-container').style.display = 'block';
    document.getElementById('downloadButton').style.display = 'block';
}

// Función para inicializar GeoGebra al cargar la página
function initializeGeoGebra() {
    const ggbApp = new GGBApplet({
        "appName": "graphing",
        "width": 850,
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
            ggbApplet.setVisible('algebra', true);
        }
    }, true);
    ggbApp.inject('geogebra');
    hideGraphAndDownloadButton();
}

// Función para descargar el gráfico como SVG
function downloadGeoGebraSVG() {
    if (typeof ggbApplet !== 'undefined' && typeof ggbApplet.exportSVG === 'function') {
        ggbApplet.exportSVG(function (svgContent) {
            if (!svgContent || !svgContent.startsWith('<svg')) {
                alert("El contenido exportado no es un SVG válido.");
                return;
            }
            let link = document.createElement('a');
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

// Ejecutar la función de inicialización cuando se cargue la página
window.onload = initializeApp;
