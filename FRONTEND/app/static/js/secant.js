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
   let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjczNzU3OTUsImlhdCI6MTcyNzIwMjk5NSwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.Sl-r-muvfEsq2x3PFlGbJTV8dY1SSQL4mknyWez5BZQ";

   // Realizar la solicitud POST a la API con el token en el encabezado
   fetch("http://localhost:8000/api/v1.3.0/backend_numerical_methods/methods/secant/", {
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
       console.log(result); // Verificar la estructura del resultado antes de usarlo

       // Limpiar resultados anteriores en la tabla
       let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
       resultsTable.innerHTML = ''; // Limpiar resultados anteriores

       // Verificar la estructura y existencia de las propiedades antes de llenar la tabla
       if (result.Iterations && result.Xn && result.Fx && result.Error) {
           // Iterar a través de las iteraciones y llenar la tabla
           result.Iterations.forEach((iteration, index) => {
               let row = resultsTable.insertRow();
               let xi_1 = result.Xn[index];
               let xi = result.Xn[index + 1]; // xi es el siguiente valor en la secuencia
               let xi_next = result.Xn[index + 2]; // xi+1 es el siguiente al siguiente valor en la secuencia
               let fx = result.Fx[index];
               let error = result.Error[index];

               // Crear las celdas de la tabla
               let iterationCell = row.insertCell(0);
               let xi_1Cell = row.insertCell(1);
               let xiCell = row.insertCell(2);
               let xiNextCell = row.insertCell(3);
               let fxCell = row.insertCell(4);
               let errorCell = row.insertCell(5);

               // Rellenar las celdas con los valores
               iterationCell.textContent = iteration;
               xi_1Cell.textContent = xi_1;
               xiCell.textContent = xi;
               xiNextCell.textContent = xi_next;
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
