// Inicializar el applet de GeoGebra
function initializeGeoGebra() {
   const ggbApp = new GGBApplet({
      "appName": "graphing",
      "width": 800,
      "height": 450,
      "showToolBar": false,
      "showAlgebraInput": false,
      "showMenuBar": false,
      "enableRightClick": false,
      "enableShiftDragZoom": true,
      "showResetIcon": true,
      "language": "es",
      "showZoomButtons": true,
      "capturingThreshold": null,
      "enableFileFeatures": true,  // Habilitar características de archivo
      "appletOnLoad": function () {
         // Insertar función predeterminada en el gráfico
         ggbApplet.evalCommand("f(x) = x^2");
      }
   }, true);
   ggbApp.inject('graph');
}

// Función para trazar la función ingresada por el usuario
function plotFunction() {
   const expression = document.getElementById('expression').value;
   const xLower = parseFloat(document.getElementById('xLower').value);
   const xUpper = parseFloat(document.getElementById('xUpper').value);
   const yLower = parseFloat(document.getElementById('yLower').value);
   const yUpper = parseFloat(document.getElementById('yUpper').value);

   // Validar y formatear la expresión
   const formattedExpression = validateAndFormatExpression(expression);

   if (!formattedExpression) {
      alert("La expresión ingresada no es válida. Por favor, verifica la sintaxis.");
      return;
   }

   // Actualizar el subtítulo de la gráfica con la función ingresada en formato LaTeX
   const graphSubtitle = document.getElementById('graphSubtitle');
   const latexExpression = convertToLatex(expression);
   graphSubtitle.innerHTML = `Función: \\(${latexExpression}\\)`; // Usar MathJax con LaTeX

   // Actualizar MathJax para que renderice el contenido
   MathJax.typesetPromise([graphSubtitle]).catch(function (err) {
      console.error('Error renderizando MathJax: ', err.message);
   });

   // Configurar los ejes del gráfico
   ggbApplet.setCoordSystem(xLower, xUpper, yLower, yUpper);

   // Limpiar el gráfico y agregar la nueva función
   ggbApplet.evalCommand("Delete[f]");
   ggbApplet.evalCommand(`f(x) = ${formattedExpression}`);
}

// Función para convertir la expresión en formato LaTeX
function convertToLatex(expression) {
   return expression
      .replace(/Sum/g, '\\sum')  // Convertir Sum a símbolo de sumatoria
      .replace(/\^/g, '^')       // Potencias
      .replace(/pi/g, '\\pi')    // Convertir pi a símbolo LaTeX
      .replace(/\*/g, '\\cdot')  // Multiplicación
      .replace(/sqrt/g, '\\sqrt') // Raíz cuadrada
      .replace(/log/g, '\\log')   // Logaritmo
      .replace(/sin/g, '\\sin')   // Seno
      .replace(/cos/g, '\\cos')   // Coseno
      .replace(/tan/g, '\\tan')   // Tangente
      .replace(/cot/g, '\\cot')   // Cotangente
      .replace(/sec/g, '\\sec')   // Secante
      .replace(/csc/g, '\\csc')   // Cosecante
      .replace(/asin/g, '\\arcsin') // Arcoseno
      .replace(/acos/g, '\\arccos') // Arcocoseno
      .replace(/atan/g, '\\arctan') // Arcotangente
      .replace(/acot/g, '\\arccot') // Arcocotangente
      .replace(/asec/g, '\\arcsec') // Arcosecante
      .replace(/acsc/g, '\\arccsc') // Arcocosecante
      .replace(/abs/g, '\\abs');   // Valor absoluto
}

// Función para validar y formatear la expresión
function validateAndFormatExpression(expression) {
   try {
      return expression.replace(/\s+/g, ''); // Elimina espacios
   } catch (error) {
      console.error("Error al formatear la expresión: ", error);
      return null;
   }
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



// Ejecutar la función de graficado inicial con valores por defecto
window.onload = function () {
   initializeGeoGebra();
};
