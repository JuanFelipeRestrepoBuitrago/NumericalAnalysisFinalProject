// Inicializar el applet de GeoGebra
function initializeGeoGebra(expression, derivative_expression, second_derivative_expression, root = null) {
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
            // Graficar la función f(x), f'(x) y f''(x)
            ggbApplet.evalCommand(`f(x) = ${expression}`);
            if (derivative_expression) {
                ggbApplet.evalCommand(`g(x) = ${derivative_expression}`);
            }
            if (second_derivative_expression) {
                ggbApplet.evalCommand(`h(x) = ${second_derivative_expression}`);
            }

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

// Función para calcular la derivada automáticamente si no se proporciona
function calculateDerivative(expression) {
    try {
        let node = math.parse(expression);
        let derivative = math.derivative(node, 'x');
        return derivative.toString(); // Convertir la derivada a cadena para GeoGebra
    } catch (error) {
        console.error("Error al derivar la función:", error);
        return null;
    }
}

// Función para calcular la segunda derivada automáticamente si no se proporciona
function calculateSecondDerivative(expression) {
    try {
        let node = math.parse(expression);
        let second_derivative = math.derivative(math.derivative(node, 'x'), 'x');
        return second_derivative.toString(); // Convertir la segunda derivada a cadena para GeoGebra
    } catch (error) {
        console.error("Error al derivar la segunda derivada:", error);
        return null;
    }
}

// Ejecutar la inicialización de GeoGebra al cargar la página con funciones por defecto
window.onload = function () {
    initializeGeoGebra('x^3 - x - 2', '3x^2 - 1', '6x');
};

function calculateSecondModifiedNewton() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let derivative_expression = document.getElementById('derivative_expression').value;
    let second_derivative_expression = document.getElementById('second_derivative_expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Si no se proporciona la derivada, calcularla automáticamente
    if (!derivative_expression || derivative_expression.trim() === "") {
        derivative_expression = calculateDerivative(expression);
        if (!derivative_expression) {
            alert("No se pudo calcular la derivada de la función proporcionada.");
            return;
        }
    }

    // Si no se proporciona la segunda derivada, calcularla automáticamente
    if (!second_derivative_expression || second_derivative_expression.trim() === "") {
        second_derivative_expression = calculateSecondDerivative(expression);
        if (!second_derivative_expression) {
            alert("No se pudo calcular la segunda derivada de la función proporcionada.");
            return;
        }
    }

    // Crear el objeto de datos para enviar a la API
    let data = {
        "expression": expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "derivative_expression": derivative_expression,
        "second_derivative_expression": second_derivative_expression
    };

    // Agregar "precision" solo si el usuario lo ha proporcionado
    if (precisionInput && precisionInput.trim() !== "") {
        data.precision = parseInt(precisionInput);
    }

    console.log('Datos enviados a la API:', JSON.stringify(data)); // Mostrar los datos enviados

    // Define el token de autenticación
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg0OTYyNjQsImlhdCI6MTcyODMyMzQ2NCwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.VbzqMestAYMgOSIW-Bg5lF179l-aVu3ZqSujniYXUx4";

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/second_modified_newton_method/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.statusText}`);
        }
        return response.json();  // Parsear la respuesta a JSON
    })
    .then(result => {
        console.log('Respuesta de la API:', result); // Verificar la estructura del resultado antes de usarlo

        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = ''; // Limpiar resultados anteriores

        // Verificar la estructura y existencia de las propiedades antes de llenar la tabla
        if (result.Iterations && result.Xn && result.Fx && result.Error) {
            // Iterar a través de las iteraciones y llenar la tabla
            result.Iterations.forEach((iteration, index) => {
                let row = resultsTable.insertRow();
                let xi = result.Xn[index];
                let fx = result.Fx[index];
                let error = result.Error[index];

                // Crear las celdas de la tabla
                let iterationCell = row.insertCell(0);  // Número de iteración
                let xiCell = row.insertCell(1);          // Valor de Xn
                let fxCell = row.insertCell(2);          // Valor de f(Xn)
                let errorCell = row.insertCell(3);       // Valor del error

                // Rellenar las celdas con los valores
                iterationCell.textContent = iteration + 1;  // Mostrar iteración comenzando desde 1
                xiCell.textContent = xi;
                fxCell.textContent = fx;
                errorCell.textContent = error;
            });

            // Obtener la raíz final
            let root = result.Xn[result.Xn.length - 1];

            // Actualizar el gráfico con la nueva función y la raíz
            initializeGeoGebra(expression, derivative_expression, second_derivative_expression, root);

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
        });
    });
 }
 

