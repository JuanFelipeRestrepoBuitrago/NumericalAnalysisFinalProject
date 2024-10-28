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

// Función para generar la matriz y el vector basados en el tamaño ingresado
function generateMatrix() {
    const size = parseInt(document.getElementById('matrixSize').value);

    if (isNaN(size) || size < 2 || size > maxSize) {
        alert('Por favor ingresa un tamaño válido entre 2 y 6.');
        return;
    }

    // Limpiar las tablas existentes
    document.getElementById('matrixInput').innerHTML = '';
    document.getElementById('vectorInput').innerHTML = '';

    // Generar la matriz de coeficientes A
    for (let i = 0; i < size; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < size; j++) {
            const cell = document.createElement('td');
            cell.innerHTML = '<input type="text" class="matrix-cell" />';
            row.appendChild(cell);
        }
        document.getElementById('matrixInput').appendChild(row);
    }

    // Generar el vector de soluciones b
    for (let i = 0; i < size; i++) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.innerHTML = '<input type="text" class="vector-cell" />';
        row.appendChild(cell);
        document.getElementById('vectorInput').appendChild(row);
    }

    // Aplicar la restricción de solo números a todos los inputs
    document.querySelectorAll('input.matrix-cell, input.vector-cell').forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9.\-]/g, ''); // Solo permitir números y signos negativos
        });
    });

    // Ocultar la gráfica y el botón de descarga cuando se genera una matriz nueva
    document.getElementById('geogebra-container').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'none';
}

// Función para obtener la matriz de la tabla
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

// Función para obtener el vector de la tabla
function getVectorFromTable() {
    const vector = [];
    const cells = document.querySelectorAll('#vectorInput input.vector-cell');
    cells.forEach(cell => vector.push([parseFloat(cell.value)]));  // Hacer cada valor un subarreglo
    return vector;
}

// Función principal de factorization LU
function calculateLUFactorization() {
    const matrix = getMatrixFromTable();
    const vector = getVectorFromTable();

    // Verificar si hay valores vacíos o no válidos
    if (matrix.some(row => row.includes(NaN)) || vector.includes(NaN)) {
        alert("Por favor, rellena todos los campos de la matriz y del vector.");
        document.getElementById('geogebra-container').style.display = 'none'; // Ocultar el gráfico si hay error
        document.getElementById('downloadButton').style.display = 'none';  // Ocultar el botón de descarga
        return; // No continuar si hay un error en los datos
    }

    const precision = document.getElementById('precision').value ? parseInt(document.getElementById('precision').value) : 16;  // Valor por defecto
    const pivotType = parseInt(document.getElementById('pivot_type').value);

    // Crear el objeto de datos para enviar a la API
    const data = {
        A: matrix,
        b: vector,
        precision: precision,
        pivot_type: pivotType
    };

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/linear_equations_system/lu_factorization/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": apiToken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw response.json();  // Lanza la respuesta como un error en JSON
        }
        return response.json();  // Parsear la respuesta a JSON
    })
    .then(result => {
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'none';
        errorMessageElement.textContent = '';

        const resultsContainer = document.getElementById('results');
        const absoluteErrorContainer = document.getElementById('absolute-error');

        // Limpiar contenedores anteriores
        resultsContainer.innerHTML = '';
        absoluteErrorContainer.innerHTML = '';

        // Función para convertir una matriz de strings a LaTeX
        function matrixToLatex(matrix) {
            return matrix.map(row => row.join(' & ')).join(' \\\\ ');
        }

        // Mostrar los resultados en formato LaTeX
        let xLatex = `x = \\begin{pmatrix} ${result.x[0].join(' \\\\ ')} \\end{pmatrix}`;
        let lLatex = `L = \\begin{pmatrix} ${matrixToLatex(result.L)} \\end{pmatrix}`;
        let uLatex = `U = \\begin{pmatrix} ${matrixToLatex(result.U)} \\end{pmatrix}`;
        let errorVectorialLatex = `\\text{Error Vectorial} = \\begin{pmatrix} ${result.vectorial_error[0].join(' \\\\ ')} \\end{pmatrix}`;
        let absoluteErrorText = `Error absoluto: ${result.absolute_error}`;

        resultsContainer.innerHTML = `\\[ ${xLatex} \\] \\[ ${lLatex} \\] \\[ ${uLatex} \\] \\[ ${errorVectorialLatex} \\]`;
        absoluteErrorContainer.textContent = absoluteErrorText;

        // Rerenderizar MathJax para que muestre las fórmulas
        MathJax.typesetPromise();

        // Solo graficar si la matriz es 2x2
        if (matrix.length === 2 && matrix[0].length === 2) {
            plotSystemInGeoGebra(matrix, vector);  // Graficar las ecuaciones ingresadas
        } else {
            document.getElementById('geogebra-container').style.display = 'none'; // Ocultar el gráfico si no es 2x2
            document.getElementById('downloadButton').style.display = 'none';  // Ocultar el botón de descarga
        }
    })
    .catch(error => {
      error.then(err => {
          console.error('Error al conectarse a la API:', err);
          const errorMessageElement = document.getElementById('error-message');
          errorMessageElement.style.display = 'block';

          // Mostrar el mensaje de error que proviene de la API
          if (err.detail) {
              errorMessageElement.textContent = err.detail;  // Si 'detail' existe en el JSON del error
          } else {
              errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';  // Mensaje genérico
          }
      });
  });
}

// Función para inicializar GeoGebra vacío (sin ecuaciones)
function initializeGeoGebra() {
    ggbApplet.reset();  // Limpiar cualquier gráfica anterior en GeoGebra
    ggbApplet.setCoordSystem(-10, 10, -10, 10);  // Ajustar el sistema de coordenadas
}

// Función para graficar el sistema de ecuaciones en GeoGebra
function plotSystemInGeoGebra(matrix, vector) {
   const a1 = matrix[0][0], b1 = matrix[0][1], c1 = vector[0][0];
   const a2 = matrix[1][0], b2 = matrix[1][1], c2 = vector[1][0];

   // Crear las ecuaciones de las líneas
   const eq1 = `(${a1}) * x + (${b1}) * y = ${c1}`;
   const eq2 = `(${a2}) * x + (${b2}) * y = ${c2}`;

   // Limpiar cualquier función o gráfica anterior en GeoGebra
   ggbApplet.reset();

   // Asegurar que la barra de álgebra esté visible
   ggbApplet.setVisible('algebra', true);

   // Agregar las ecuaciones con nombres personalizados en GeoGebra
   ggbApplet.evalCommand(`ec1: ${eq1}`);  // Nombra la primera ecuación como "ec1"
   ggbApplet.evalCommand(`ec2: ${eq2}`);  // Nombra la segunda ecuación como "ec2"

   // Ajustar el sistema de coordenadas
   ggbApplet.setCoordSystem(-10, 10, -10, 10);

   // Mostrar el contenedor de GeoGebra y el botón de descarga
   document.getElementById('geogebra-container').style.display = 'block';
   document.getElementById('downloadButton').style.display = 'block';
}

// Inicializar el applet de GeoGebra y asegurarse de que la barra de álgebra esté visible
function initializeGeoGebra() {
    const ggbApp = new GGBApplet({
        "appName": "graphing",
        "width": 850,
        "height": 450,
        "showToolBar": false,
        "showAlgebraInput": true,  // Mostrar el input de álgebra
        "showMenuBar": false,
        "enableRightClick": false,
        "enableShiftDragZoom": true,
        "showResetIcon": false,
        "language": "es",
        "showZoomButtons": true,
        "capturingThreshold": null,
        "enableFileFeatures": true,
        "appletOnLoad": function () {
            ggbApplet.setVisible('algebra', true); // Mostrar la barra de álgebra al cargar
        }
    }, true);
    ggbApp.inject('geogebra');

    // Ocultar el contenedor de GeoGebra al cargar la página
    document.getElementById('geogebra-container').style.display = 'none';
    document.getElementById('downloadButton').style.display = 'none';  // Ocultar el botón de descarga
}

// Ejecutar la función de graficado inicial con valores por defecto y ocultar el gráfico al cargar la página
window.onload = function () {
    initializeGeoGebra();
};
