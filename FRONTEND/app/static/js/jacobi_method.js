const maxSize = 6; // Tamaño máximo de 6x6 para la matriz

// Función para generar la matriz, el vector b y el vector de inicialización x0 basados en el tamaño ingresado
function generateMatrix() {
    const size = parseInt(document.getElementById('matrixSize').value);

    // Validar el tamaño de la matriz
    if (isNaN(size) || size < 2 || size > maxSize) {
        alert('Por favor ingresa un tamaño válido entre 2 y 6.');
        return;
    }

    // Limpiar las tablas existentes
    document.getElementById('matrixInput').innerHTML = '';
    document.getElementById('vectorInput').innerHTML = '';
    document.getElementById('xInitialInput').innerHTML = '';

    // Generar la matriz de coeficientes A
    generateMatrixInput(size);

    // Generar el vector de soluciones b
    generateVectorInput('vectorInput', size);

    // Generar el vector de inicialización x0
    generateVectorInput('xInitialInput', size);

    // Aplicar restricción de solo números a todos los inputs
    applyInputRestrictions();

    // Ocultar la gráfica y el botón de descarga cuando se genera una matriz nueva
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

    // Verificar si hay valores vacíos o no válidos
    if (matrix.some(row => row.includes(NaN)) || vectorB.includes(NaN) || xInitial.includes(NaN)) {
        alert("Por favor, rellena todos los campos de la matriz, el vector y el vector inicial.");
        return;
    }

    const precision = document.getElementById('precision').value || 16;
    const maxIter = document.getElementById('max_iter').value || 100;
    const tol = document.getElementById('tolerance').value || 1e-7;

    const methodType = document.getElementById('method_type').value;
    const errorType = document.getElementById('error_type').value;

    // Crear el objeto de datos para enviar a la API
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

    console.log("Datos enviados a la API:", JSON.stringify(data));

    // Enviar los datos a la API
    sendDataToAPI(data);
}

// Función para enviar los datos a la API
function sendDataToAPI(data) {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg2MDM2MjMsImlhdCI6MTcyODQzMDgyMywidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.VIpuHO5lvZBT93IEkKaHt5zlnoOpRkkqmx0PcLzpKW0";

    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/linear_equations_system/jacobi/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw response.json();  // Lanza la respuesta como un error en JSON
            }
            return response.json();
        })
        .then(result => {
            displayResults(result);

            // Graficar solo si la matriz es 2x2
            if (data.A.length === 2 && data.A[0].length === 2) {
                plotSystemInGeoGebra(data.A, data.b);
            } else {
                hideGraphAndDownloadButton();
            }
        })
        .catch(error => handleError(error));
}

// Función para mostrar los resultados en la tabla
function displayResults(result) {
   const resultsTable = document.querySelector("#resultsTable tbody");
   const resultsTableHead = document.querySelector("#resultsTable thead");
   resultsTable.innerHTML = ''; // Limpiar la tabla antes de añadir los nuevos resultados
   resultsTableHead.innerHTML = ''; // Limpiar la cabecera antes de añadir nuevas columnas

   // Obtener las listas de iteraciones, X y errores del resultado de la API
   const iterations = result.iterations;  // Array de iteraciones
   const solutions = result.x;            // Lista de listas de soluciones
   const errors = result.error;           // Array de errores

   const numSolutions = solutions.length; // Número de columnas Xn (dependerá del tamaño de la matriz)

   // Crear las cabeceras de la tabla de forma dinámica
   const headerRow = document.createElement('tr');
   const headerIteration = document.createElement('th');
   headerIteration.textContent = 'Iteración';
   headerRow.appendChild(headerIteration);

   // Generar dinámicamente las cabeceras X1, X2, ..., Xn según el número de soluciones
   for (let i = 0; i < numSolutions; i++) {
       const headerX = document.createElement('th');
       headerX.textContent = `X${i + 1}`;
       headerRow.appendChild(headerX);
   }

   const headerError = document.createElement('th');
   headerError.textContent = 'Error';
   headerRow.appendChild(headerError);
   resultsTableHead.appendChild(headerRow);

   // Iterar sobre los datos y añadir cada fila a la tabla
   iterations.forEach((iteration, index) => {
       const newRow = document.createElement('tr');

       // Crear celda para la iteración
       const cellIteration = document.createElement('td');
       cellIteration.textContent = iteration; // Número de iteración
       newRow.appendChild(cellIteration);

       // Crear celdas dinámicas para cada solución Xn
       for (let i = 0; i < numSolutions; i++) {
           const cellXn = document.createElement('td');
           cellXn.textContent = solutions[i][index]; // Valor de la solución Xn en esa iteración
           newRow.appendChild(cellXn);
       }

       // Crear celda para el error
       const cellError = document.createElement('td');
       cellError.textContent = errors[index]; // Error asociado a esa iteración
       newRow.appendChild(cellError);

       // Añadir la fila a la tabla
       resultsTable.appendChild(newRow);
   });

   // Mostrar el mensaje de convergencia si existe
   const convergenceMessage = document.getElementById('convergence-message');
   if (result.message) {
       convergenceMessage.textContent = result.message;
   } else {
       convergenceMessage.textContent = 'Método completado sin mensaje de convergencia.';
   }
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

    console.log("Ecuaciones graficadas en GeoGebra:", eq1, eq2);

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
            console.log("GeoGebra cargado");
            ggbApplet.setVisible('algebra', true);
        }
    }, true);
    ggbApp.inject('geogebra');

    hideGraphAndDownloadButton();
}


function downloadGeoGebraSVG() {
   console.log("Botón de descarga SVG presionado"); // Verificar si la función se llama
   if (typeof ggbApplet !== 'undefined' && typeof ggbApplet.exportSVG === 'function') {
       // Llamar a exportSVG con una función de callback para procesar el SVG
       ggbApplet.exportSVG(function(svgContent) {
           console.log("SVG Content: ", svgContent); // Verificar el contenido del SVG

           // Asegurarse de que el SVG no esté vacío o indefinido
           if (!svgContent || !svgContent.startsWith('<svg')) {
               alert("El contenido exportado no es un SVG válido.");
               return;
           }

           // Crear un enlace para descargar el archivo SVG
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
window.onload = function () {
    initializeGeoGebra();
};
