let apiToken;

// Inicializa la aplicación al cargar la página
async function initializeApp() {
   await fetchApiToken();
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

// Inicializa la aplicación y GeoGebra
initializeApp();
initializeGeoGebra();

// Agrega un nuevo punto (x, y) en el formulario
function addPoint() {
   const container = document.getElementById('points-container');
   if (container.children.length >= 6) {
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

// Función para calcular el método de Spline y graficar el polinomio y puntos
function calculateSpline() {
   const xInputs = document.querySelectorAll('input[name="x[]"]');
   const yInputs = document.querySelectorAll('input[name="y[]"]');
   const xValues = Array.from(xInputs).map(input => parseFloat(input.value));
   const yValues = Array.from(yInputs).map(input => parseFloat(input.value));
   const degree = parseInt(document.getElementById('degree').value);

   if (xValues.length < 2 || yValues.length < 2 || xValues.includes(NaN) || yValues.includes(NaN)) {
      alert("Por favor, rellena todos los campos de los puntos (x, y).");
      return;
   }

   const precision = document.getElementById('precision').value ? parseInt(document.getElementById('precision').value) : 16;

   const data = {
      x: xValues,
      y: yValues,
      precision: precision,
      degree: degree
   };

   fetch("http://localhost:8000/api/v1.5.0/backend_numerical_methods/interpolation/spline/", {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
         "Authorization": apiToken
      },
      body: JSON.stringify(data)
   })
      .then(response => response.json())
      .then(result => {
         displayResults(result);
         plotSplineFunctionsInGeoGebra(result.functions, xValues, yValues);
      })
      .catch(error => console.error("Error en la solicitud:", error));
}


// Muestra los resultados en formato LaTeX
function displayResults(result) {
   // Formatear cada función e intervalo
   const functionsLatex = result.functions.map(f => {
      const formattedFunction = f.function
         .replace(/\*\*([0-9]+)/g, "^{$1}")
         .replace(/\s?\*\s?/g, "");
      return `\\( ${formattedFunction} \\) \ en el intervalo \\( ${f.interval} \\)`;
   }).join("<br>");

   const coefficientsLatex = `
       \\[
       \\begin{bmatrix}
       ${result.coefficients.map(row => row.join(' & ')).join(' \\\\ ')}
       \\end{bmatrix}
       \\]
   `;

   const resultsContainer = document.getElementById('results');
   resultsContainer.innerHTML = `
       <h3>Funciones Spline:</h3> ${functionsLatex}<br><br>
       <h3>Coeficientes:</h3> ${coefficientsLatex}
   `;

   MathJax.typesetPromise();
}



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

// Graficar las funciones Spline en GeoGebra
function plotSplineFunctionsInGeoGebra(functions, xValues, yValues) {
   ggbApplet.reset();

   // Graficar cada función a tramos en su intervalo correspondiente
   functions.forEach((f, index) => {
      // Extraer el intervalo y los límites inferior y superior
      const intervalMatch = f.interval.match(/([-+]?\d*\.?\d+)\s*<=\s*x\s*<=\s*([-+]?\d*\.?\d+)/);
      if (intervalMatch) {
         const lowerBound = parseFloat(intervalMatch[1]);
         const upperBound = parseFloat(intervalMatch[2]);
         const functionCommand = `If(${lowerBound} <= x <= ${upperBound}, ${f.function})`;

         // Graficar la función a tramos en GeoGebra
         ggbApplet.evalCommand(`f${index + 1}: ${functionCommand}`);
      }
   });

   // Graficar los puntos
   xValues.forEach((x, index) => {
      const y = yValues[index];
      ggbApplet.evalCommand(`P${index + 1} = (${x}, ${y})`);
   });

   // Ajustar el sistema de coordenadas
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
