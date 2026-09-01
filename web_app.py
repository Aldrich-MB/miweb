# web_app.py
# Aplicación web para el conversor de sistemas numéricos
# Integra main.py, conversor.py y conversor_avanzado.py

from flask import Flask, render_template_string, request, jsonify
import conversor
import conversor_avanzado

app = Flask(__name__)

# HTML Template con diseño moderno
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔄 Conversor Numérico Interactivo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            border: 2px solid #e9ecef;
            transition: all 0.3s;
        }
        
        .card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
        }
        
        .card h2 {
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        textarea, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 16px;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
            resize: vertical;
        }
        
        textarea:focus, input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            min-height: 60px;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            flex: 1;
            min-width: 100px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5a67d8;
        }
        
        .btn-success {
            background: #48bb78;
            color: white;
        }
        
        .btn-success:hover {
            background: #38a169;
        }
        
        .btn-danger {
            background: #fc8181;
            color: white;
        }
        
        .btn-danger:hover {
            background: #f56565;
        }
        
        .btn-info {
            background: #63b3ed;
            color: white;
        }
        
        .btn-info:hover {
            background: #4299e1;
        }
        
        .btn-warning {
            background: #f6ad55;
            color: white;
        }
        
        .btn-warning:hover {
            background: #ed8936;
        }
        
        .result {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            word-break: break-all;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            min-height: 30px;
        }
        
        .result-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 5px;
            font-family: 'Segoe UI', sans-serif;
        }
        
        .error {
            border-left-color: #fc8181;
            color: #e53e3e;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 5px;
        }
        
        .badge-binario { background: #bee3f8; color: #2a69ac; }
        .badge-hexadecimal { background: #c6f6d5; color: #276749; }
        .badge-texto { background: #fefcbf; color: #975a16; }
        .badge-base64 { background: #e9d8fd; color: #6b46c1; }
        .badge-octal { background: #fed7d7; color: #9b2c2c; }
        
        .copy-btn {
            background: #e2e8f0;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .copy-btn:hover {
            background: #cbd5e0;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #718096;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 Conversor Numérico Interactivo</h1>
        <p class="subtitle">Convierte entre texto, binario, hexadecimal, octal y Base64</p>
        
        <div class="grid">
            <!-- Tarjeta 1: Texto ↔ Binario -->
            <div class="card">
                <h2>📝 ↔ 🔢 Texto ↔ Binario</h2>
                <textarea id="input_binario" placeholder="Ingresa texto o binario...">Hola Mundo</textarea>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="convertir('texto_a_binario')">Texto → Binario</button>
                    <button class="btn btn-success" onclick="convertir('binario_a_texto')">Binario → Texto</button>
                </div>
                <div id="result_binario" class="result">Resultado aparecerá aquí</div>
                <button class="copy-btn" onclick="copiarResultado('result_binario')">📋 Copiar</button>
            </div>
            
            <!-- Tarjeta 2: Texto ↔ Hexadecimal -->
            <div class="card">
                <h2>📝 ↔ 🔢 Texto ↔ Hexadecimal</h2>
                <textarea id="input_hexadecimal" placeholder="Ingresa texto o hexadecimal...">Hola Mundo</textarea>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="convertir('texto_a_hexadecimal')">Texto → Hexadecimal</button>
                    <button class="btn btn-success" onclick="convertir('hexadecimal_a_texto')">Hexadecimal → Texto</button>
                </div>
                <div id="result_hexadecimal" class="result">Resultado aparecerá aquí</div>
                <button class="copy-btn" onclick="copiarResultado('result_hexadecimal')">📋 Copiar</button>
            </div>
            
            <!-- Tarjeta 3: Detección Automática -->
            <div class="card full-width">
                <h2>🔍 Detección Automática de Formato</h2>
                <textarea id="input_deteccion" placeholder="Ingresa cualquier texto, binario, hexadecimal, octal o Base64...">01001000 01101111 01101100 01100001</textarea>
                <div class="btn-group">
                    <button class="btn btn-info" onclick="convertir('detectar')">🔍 Detectar y Convertir</button>
                    <button class="btn btn-warning" onclick="limpiarDeteccion()">🔄 Limpiar</button>
                </div>
                <div id="result_deteccion" class="result">Resultado aparecerá aquí</div>
                <button class="copy-btn" onclick="copiarResultado('result_deteccion')">📋 Copiar</button>
            </div>
            
            <!-- Tarjeta 4: Conversiones Avanzadas -->
            <div class="card full-width">
                <h2>🚀 Conversiones Avanzadas</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <h3 style="font-size: 1em; color: #4a5568;">📝 ↔ Base64</h3>
                        <textarea id="input_base64" placeholder="Texto o Base64..." style="min-height: 40px;">Hola Mundo</textarea>
                        <div class="btn-group">
                            <button class="btn btn-primary" onclick="convertir('texto_a_base64')">→ Base64</button>
                            <button class="btn btn-success" onclick="convertir('base64_a_texto')">→ Texto</button>
                        </div>
                        <div id="result_base64" class="result" style="min-height: 20px; font-size: 12px;">Resultado</div>
                    </div>
                    
                    <div>
                        <h3 style="font-size: 1em; color: #4a5568;">📝 ↔ Octal</h3>
                        <textarea id="input_octal" placeholder="Texto u octal..." style="min-height: 40px;">Hola Mundo</textarea>
                        <div class="btn-group">
                            <button class="btn btn-primary" onclick="convertir('texto_a_octal')">→ Octal</button>
                            <button class="btn btn-success" onclick="convertir('octal_a_texto')">→ Texto</button>
                        </div>
                        <div id="result_octal" class="result" style="min-height: 20px; font-size: 12px;">Resultado</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>💡 Tip: Los resultados se pueden copiar con el botón 📋 | Usa la detección automática para identificar el formato</p>
            <p>🔧 Desarrollado con Flask + Python</p>
        </div>
    </div>
    
    <script>
        function convertir(operacion) {
            let inputId, resultId, url;
            
            // Determinar qué inputs usar según la operación
            const operaciones = {
                'texto_a_binario': { input: 'input_binario', result: 'result_binario' },
                'binario_a_texto': { input: 'input_binario', result: 'result_binario' },
                'texto_a_hexadecimal': { input: 'input_hexadecimal', result: 'result_hexadecimal' },
                'hexadecimal_a_texto': { input: 'input_hexadecimal', result: 'result_hexadecimal' },
                'texto_a_base64': { input: 'input_base64', result: 'result_base64' },
                'base64_a_texto': { input: 'input_base64', result: 'result_base64' },
                'texto_a_octal': { input: 'input_octal', result: 'result_octal' },
                'octal_a_texto': { input: 'input_octal', result: 'result_octal' },
                'detectar': { input: 'input_deteccion', result: 'result_deteccion' }
            };
            
            const config = operaciones[operacion];
            if (!config) return;
            
            const inputElement = document.getElementById(config.input);
            const resultElement = document.getElementById(config.result);
            const valor = inputElement.value;
            
            if (!valor.trim()) {
                resultElement.innerHTML = '⚠️ Por favor, ingresa algún valor';
                resultElement.className = 'result error';
                return;
            }
            
            // Mostrar estado de carga
            resultElement.innerHTML = '⏳ Procesando...';
            resultElement.className = 'result';
            
            // Hacer petición al servidor
            fetch('/convertir', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    operacion: operacion,
                    valor: valor
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultElement.innerHTML = '❌ ' + data.error;
                    resultElement.className = 'result error';
                } else {
                    let resultado = data.resultado;
                    
                    // Si es detección, mostrar formato detectado
                    if (operacion === 'detectar' && data.formato) {
                        const badges = {
                            'binario': '<span class="badge badge-binario">🔢 Binario</span>',
                            'hexadecimal': '<span class="badge badge-hexadecimal">🔢 Hexadecimal</span>',
                            'texto': '<span class="badge badge-texto">📝 Texto</span>',
                            'base64': '<span class="badge badge-base64">🔐 Base64</span>',
                            'octal': '<span class="badge badge-octal">🔢 Octal</span>'
                        };
                        const badge = badges[data.formato] || '';
                        resultElement.innerHTML = `
                            <div class="result-label">🔍 Formato detectado: ${badge}</div>
                            <div style="margin-top: 10px;"><strong>Resultado:</strong> ${resultado}</div>
                        `;
                    } else {
                        // Mostrar el resultado con un label
                        const label = {
                            'texto_a_binario': 'Binario',
                            'binario_a_texto': 'Texto',
                            'texto_a_hexadecimal': 'Hexadecimal',
                            'hexadecimal_a_texto': 'Texto',
                            'texto_a_base64': 'Base64',
                            'base64_a_texto': 'Texto',
                            'texto_a_octal': 'Octal',
                            'octal_a_texto': 'Texto'
                        }[operacion] || 'Resultado';
                        
                        resultElement.innerHTML = `
                            <div class="result-label">✅ ${label}:</div>
                            <div>${resultado}</div>
                        `;
                    }
                    resultElement.className = 'result';
                }
            })
            .catch(error => {
                resultElement.innerHTML = '❌ Error de conexión: ' + error.message;
                resultElement.className = 'result error';
            });
        }
        
        function copiarResultado(elementId) {
            const element = document.getElementById(elementId);
            // Extraer solo el texto del resultado (sin etiquetas HTML)
            const textContent = element.textContent.replace('Resultado aparecerá aquí', '').trim();
            
            if (!textContent || textContent.includes('⚠️') || textContent.includes('❌')) {
                alert('⚠️ No hay un resultado válido para copiar');
                return;
            }
            
            navigator.clipboard.writeText(textContent).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ ¡Copiado!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            }).catch(() => {
                alert('❌ No se pudo copiar al portapapeles');
            });
        }
        
        function limpiarDeteccion() {
            document.getElementById('input_deteccion').value = '';
            document.getElementById('result_deteccion').innerHTML = 'Resultado aparecerá aquí';
            document.getElementById('result_deteccion').className = 'result';
        }
        
        // Ejecutar conversiones automáticas al cargar
        window.addEventListener('DOMContentLoaded', function() {
            // Mostrar ejemplos iniciales
            setTimeout(() => {
                convertir('texto_a_binario');
                convertir('texto_a_hexadecimal');
                convertir('texto_a_base64');
                convertir('texto_a_octal');
                convertir('detectar');
            }, 500);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/convertir', methods=['POST'])
def convertir():
    """Endpoint para conversiones"""
    try:
        data = request.get_json()
        operacion = data.get('operacion')
        valor = data.get('valor', '').strip()
        
        if not valor:
            return jsonify({'error': 'Valor vacío'})
        
        resultado = ""
        formato = None
        
        # Mapeo de operaciones a funciones
        if operacion == 'texto_a_binario':
            resultado = conversor.texto_a_binario(valor)
        elif operacion == 'binario_a_texto':
            resultado = conversor.binario_a_texto(valor)
        elif operacion == 'texto_a_hexadecimal':
            resultado = conversor.texto_a_hexadecimal(valor)
        elif operacion == 'hexadecimal_a_texto':
            resultado = conversor.hexadecimal_a_texto(valor)
        elif operacion == 'texto_a_base64':
            resultado = conversor_avanzado.texto_a_base64(valor)
        elif operacion == 'base64_a_texto':
            resultado = conversor_avanzado.base64_a_texto(valor)
        elif operacion == 'texto_a_octal':
            resultado = conversor_avanzado.texto_a_octal(valor)
        elif operacion == 'octal_a_texto':
            resultado = conversor_avanzado.octal_a_texto(valor)
        elif operacion == 'detectar':
            # Usar detección avanzada primero
            formato = conversor_avanzado.detectar_formato_avanzado(valor)
            
            if formato == 'binario':
                resultado = conversor.binario_a_texto(valor)
            elif formato == 'hexadecimal':
                resultado = conversor.hexadecimal_a_texto(valor)
            elif formato == 'base64':
                resultado = conversor_avanzado.base64_a_texto(valor)
            elif formato == 'octal':
                resultado = conversor_avanzado.octal_a_texto(valor)
            else:  # texto
                resultado = f"📝 Texto detectado\nBinario: {conversor.texto_a_binario(valor)}\nHexadecimal: {conversor.texto_a_hexadecimal(valor)}\nBase64: {conversor_avanzado.texto_a_base64(valor)}\nOctal: {conversor_avanzado.texto_a_octal(valor)}"
        else:
            return jsonify({'error': f'Operación no soportada: {operacion}'})
        
        return jsonify({
            'resultado': resultado,
            'formato': formato
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'})

if __name__ == '__main__':
    print("="*60)
    print("🚀 Iniciando Conversor Web...")
    print("📱 Abre tu navegador en: http://127.0.0.1:5000")
    print("="*60)
    app.run(debug=True, host='127.0.0.1', port=5000)