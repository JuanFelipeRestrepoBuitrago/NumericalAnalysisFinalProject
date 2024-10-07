const maxSize = 6; // Tamaño máximo de 6x6 para la matriz

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

// Función principal de eliminación gaussiana
function calculateGaussElimination() {
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
    const order = parseInt(document.getElementById('order').value);

    // Crear el objeto de datos para enviar a la API
    const data = {
        A: matrix,
        b: vector,
        precision: precision,
        pivot_type: pivotType,
        order: order
    };

    console.log("Datos enviados a la API:", JSON.stringify(data));

    // Token de autenticación
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg0MTIwMzEsImlhdCI6MTcyODIzOTIzMSwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.3JoKuJVgq7_XX7hxJqRKrE7UODHIUSWiXoznRjdMthQ";

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/linear_equations_system/gauss_elimination/", {
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
        return response.json();  // Parsear la respuesta a JSON
    })
    .then(result => {
        console.log(result); // Verificar la estructura del resultado antes de usarlo

        // Limpiar cualquier mensaje de error previo
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.style.display = 'none';
        errorMessageElement.textContent = '';

        const resultsContainer = document.getElementById('results');
        const absoluteErrorContainer = document.getElementById('absolute-error');

        // Limpiar contenedores anteriores
        resultsContainer.innerHTML = '';
        absoluteErrorContainer.innerHTML = '';

        // Mostrar los resultados de X en formato LaTeX
        const xResult = result.x[0];
        const vectorialError = result.vectorial_error[0];
        const absoluteError = result.absolute_error;

        // Crear una matriz en LaTeX con los elementos de x en una columna
        let xLatex = `x = \\begin{pmatrix} ${xResult.join(' \\\\ ')} \\end{pmatrix}`;
        
        // Crear una matriz en LaTeX con los elementos del error vectorial
        let errorVectorialLatex = `\\text{Error Vectorial} = \\begin{pmatrix} ${vectorialError.join(' \\\\ ')} \\end{pmatrix}`;
        
        // Mensaje para el error absoluto
        let absoluteErrorText = `Error absoluto: ${absoluteError}`;

        // Insertar las expresiones en el contenedor
        resultsContainer.innerHTML = `\\[ ${xLatex} \\] \\[ ${errorVectorialLatex} \\]`;
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

           // Extraer y mostrar el mensaje enviado por la API, manejando ambos casos (string o array de objetos)
           if (typeof err.detail === 'string') {
               errorMessageElement.textContent = err.detail;  // Si `detail` es string, lo mostramos
           } else if (Array.isArray(err.detail) && err.detail[0].msg) {
               errorMessageElement.textContent = err.detail[0].msg;  // Si `detail` es array, mostramos el mensaje
           } else {
               errorMessageElement.textContent = 'Ocurrió un error al procesar la solicitud.';  // Mensaje genérico
           }

           errorMessageElement.style.textAlign = 'center';  // Centrar el mensaje de error
           document.getElementById('geogebra-container').style.display = 'none'; // Ocultar el gráfico si hay error de API
           document.getElementById('downloadButton').style.display = 'none';  // Ocultar el botón de descarga
       });
   });
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

// Función para inicializar GeoGebra vacío (sin ecuaciones)
function initializeEmptyGeoGebra() {
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

   console.log("Ecuaciones graficadas en GeoGebra:", eq1, eq2);

   // Mostrar el contenedor de GeoGebra
   document.getElementById('geogebra-container').style.display = 'block';
     // Mostrar el botón de descarga
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
            console.log("GeoGebra cargado");
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