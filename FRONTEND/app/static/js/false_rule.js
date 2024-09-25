function calculateFalseRule() {
   // Obtener valores del formulario
   let expression = document.getElementById('expression').value;
   let initial = parseFloat(document.getElementById('initial').value);
   let final = parseFloat(document.getElementById('final').value);
   let tolerance = parseFloat(document.getElementById('tolerance').value);
   let max_iterations = parseInt(document.getElementById('max_iterations').value);
   let error_type = document.getElementById('error_type').value; // Tipo de error
   let precisionInput = document.getElementById('precision').value; // Obtener precisión

   // Crear objeto de datos para la API
   let data = {
       "expression": expression,
       "error_type": error_type,
       "tolerance": tolerance,
       "max_iterations": max_iterations,
       "initial": initial,
       "final": final
   };

   if (precisionInput !== "" && precisionInput !== null) {
       data.precision = parseInt(precisionInput);
   }

   let token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjc0NjE2NDUsImlhdCI6MTcyNzI4ODg0NSwidXNlciI6eyJ1c2VybmFtZSI6ImVhZml0In19.62cBxM-461aHw7ilCJgb6be8IeY2h4lgI41z6CiHXyI";

   // Realizar solicitud POST a la API
   fetch("http://localhost:8000/api/v1.3.0/backend_numerical_methods/methods/false_rule/", {
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
       // Limpiar resultados anteriores en la tabla
       let resultsTable = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];
       resultsTable.innerHTML = ''; // Limpiar resultados anteriores

       result.Iterations.forEach((iteration, index) => {
           let row = resultsTable.insertRow();
           let a = result.Xn[index];
           let xm = result.Xn[index];
           let b = result.Xn[index];
           let fx = result.Fx[index];
           let error = result.Error[index];
           
           // Crear celdas de la tabla
           let iterationCell = row.insertCell(0);
           let aCell = row.insertCell(1);
           let xmCell = row.insertCell(2);
           let bCell = row.insertCell(3);
           let fxCell = row.insertCell(4);
           let errorCell = row.insertCell(5);

           // Asignar valores a las celdas
           iterationCell.textContent = iteration;
           aCell.textContent = a;
           xmCell.textContent = xm;
           bCell.textContent = b;
           fxCell.textContent = fx;
           errorCell.textContent = error;
       });

       // Mostrar mensaje de la raíz
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
