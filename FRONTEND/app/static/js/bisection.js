function calculateBisection() {
    // Obtener valores del formulario
    let expression = document.getElementById('expression').value;
    let initial = parseFloat(document.getElementById('initial').value);
    let final = parseFloat(document.getElementById('final').value);
    let tolerance = parseFloat(document.getElementById('tolerance').value);
    let max_iterations = parseInt(document.getElementById('max_iterations').value);
    let error_type = document.getElementById('error_type').value; // Obtener el tipo de error seleccionado
    let precisionInput = document.getElementById('precision').value; // Obtener precisión, si se proporciona

    // Crear el objeto de datos para enviar a la API
    let data = {
        "expression": expression,
        "error_type": error_type,  // Usar el tipo de error seleccionado
        "tolerance": tolerance,
        "max_iterations": max_iterations,
        "initial": initial,
        "final": final
    };

    // Agregar "precision" solo si el usuario lo ha proporcionado y no es null
    if (precisionInput !== "" && precisionInput !== null) {
        data.precision = parseInt(precisionInput);
    }

    // Define el token de autenticación
    let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjczNzU3OTUsImlhdCI6MTcyNzIwMjk5NSwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.Sl-r-muvfEsq2x3PFlGbJTV8dY1SSQL4mknyWez5BZQ";

    // Realizar la solicitud POST a la API con el token en el encabezado
    fetch("http://localhost:8000/api/v1.3.1/backend_numerical_methods/methods/bisection/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`  // Añade el token al encabezado de autorización
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
        // Limpiar resultados anteriores en la tabla
        let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
        resultsTable.innerHTML = ''; // Limpiar resultados anteriores
        
        // Verificar la estructura y existencia de las propiedades antes de llenar la tabla
        if (result.Iterations && result.Xn && result.Fx && result.Error) {
            // Iterar a través de las iteraciones y llenar la tabla
            result.Iterations.forEach((iteration, index) => {
                let row = resultsTable.insertRow();
                let xn = result.Xn[index];
                let fx = result.Fx[index];
                let error = result.Error[index];

                // Crear las celdas de la tabla
                let iterationCell = row.insertCell(0);  // Número de iteración
                let xnCell = row.insertCell(1);          // Valor de Xn
                let fxCell = row.insertCell(2);          // Valor de f(X)
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

        // Mostrar el mensaje de la raíz de la función en el contenedor
        let rootMessage = document.getElementById('rootMessage');
        if (result.Message) {
            rootMessage.textContent = result.Message;
        } else {
            rootMessage.textContent = "No se encontró un mensaje de raíz.";
        }
    })
    .catch(error => {
        console.error('Error al conectarse a la API:', error);
        alert(`Error al conectarse a la API: ${error.message}`);
    });
}
