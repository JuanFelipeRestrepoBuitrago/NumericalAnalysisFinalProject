// Función para formatear la expresión para GeoGebra
function formatExpressionForGeoGebra(expression) {
    return expression
        .replace(/\*\*/g, "^")  // Reemplaza ** por ^ para exponentes en GeoGebra
        .replace(/Math\.sqrt/g, "sqrt")  // Asegura que sqrt se usa correctamente
        .replace(/Math\.sin/g, "sin")   // Reemplaza funciones trigonométricas
        .replace(/Math\.cos/g, "cos")
        .replace(/Math\.tan/g, "tan")
        .replace(/Math\.log/g, "log");  // Logaritmo natural en GeoGebra
}

// Inicializar el applet de GeoGebra
function initializeGeoGebra(expression = "x^2-4", root = null) {
    const formattedExpression = formatExpressionForGeoGebra(expression);

    console.log("Expresión enviada a GeoGebra: ", formattedExpression);

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
            // Insertar la función en el gráfico
            ggbApplet.evalCommand(`f(x) = ${formattedExpression}`);
            
            // Si hay una raíz, marcarla en la gráfica
            if (root !== null) {
                ggbApplet.evalCommand(`RootPoint = (${root}, f(${root}))`);  // Crea un punto en la raíz
                ggbApplet.evalCommand(`SetPointStyle(RootPoint, 3)`);  // Cambia el estilo del punto
                ggbApplet.evalCommand(`SetPointSize(RootPoint, 5)`);   // Aumenta el tamaño del punto
            }
        }
    }, true);
    
    ggbApp.inject('geogebra');  // Inyecta el gráfico en el contenedor 'geogebra'
}

// Ejecutar la inicialización de GeoGebra al cargar la página
window.onload = function () {
    initializeGeoGebra();  // Puedes pasar una expresión predeterminada, o dejar "x^2" como default.
};

// Función que se llama al enviar el formulario
function calculateSecant() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let second_initial = parseFloat(document.getElementById('second_initial').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value;
    let precisionInput = document.getElementById('precision').value;

    // Crear el objeto de datos para enviar a la API
    let data = {
        "expression": expression,
        "error_type": error_type,
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "second_initial": second_initial
    };

    // Agregar "precision" solo si el usuario lo ha proporcionado y no es null
    if (precisionInput !== "" && precisionInput !== null) {
        data.precision = parseInt(precisionInput);
    }

    // Define el token de autenticación
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg0OTYyNjQsImlhdCI6MTcyODMyMzQ2NCwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.VbzqMestAYMgOSIW-Bg5lF179l-aVu3ZqSujniYXUx4";

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/secant/", {
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
        console.log(result);  // Verificar la estructura del resultado antes de usarlo

        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = '';  // Limpiar resultados anteriores

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
                let xiCell = row.insertCell(1);          // Valor de xi
                let fxCell = row.insertCell(2);          // Valor de f(xi+1)
                let errorCell = row.insertCell(3);       // Valor del error

                // Rellenar las celdas con los valores
                iterationCell.textContent = iteration + 1;  // Mostrar iteración comenzando desde 1
                xiCell.textContent = xi;
                fxCell.textContent = fx;
                errorCell.textContent = error;
            });
        } else {
            console.error('Estructura de respuesta incorrecta. Algunas propiedades están indefinidas.');
            alert('Error: La estructura de la respuesta de la API no es la esperada.');
        }

        // Mostrar el mensaje de la raíz de la función en el contenedor
        let rootMessage = document.getElementById('rootMessage');
        let root = null;
        if (result.Message) {
            rootMessage.textContent = result.Message;
            root = result.Xn[result.Xn.length - 1];  // Asumimos que la última Xn es la raíz aproximada
        } else {
            rootMessage.textContent = "No se encontró un mensaje de raíz.";
        }

        // Actualizar el gráfico con la nueva función y la raíz aproximada
        initializeGeoGebra(expression, root);
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
 