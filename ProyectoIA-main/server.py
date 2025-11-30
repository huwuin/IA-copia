from flask import Flask, request, send_from_directory
import subprocess
import sys
import os
import time

app = Flask(__name__)
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Control de ejecución
ultima_ejecucion = 0

# Servir archivos estáticos
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('img', filename)

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    return send_from_directory('docs', filename)

# Servir todas las páginas HTML
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<page_name>')
def serve_page(page_name):
    if page_name.endswith('.html'):
        return send_from_directory('.', page_name)
    return "Página no encontrada", 404

@app.route('/ejecutar-app', methods=['POST', 'GET'])
def ejecutar_app():
    """Ejecuta la app con los parámetros de origen y destino"""
    global ultima_ejecucion
    
    try:
        # Control de tiempo
        ahora = time.time()
        if ahora - ultima_ejecucion < 3:
            return "OK"
        ultima_ejecucion = ahora
        
        if request.method == 'POST':
            data = request.get_json()
            origen = data.get('origen', '')
            destino = data.get('destino', '')
        else:
            origen = request.args.get('origen', '')
            destino = request.args.get('destino', '')
        
        print(f"🚀 EJECUTANDO APP: {origen} -> {destino}")
        
        # ✅ EJECUTAR CON PARÁMETROS
        if os.name == 'nt':
            # Usar python.exe que no abre terminal
            subprocess.Popen(['python', 'app.py', origen, destino],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           stdin=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        
        else:
            subprocess.Popen([sys.executable, 'app.py', origen, destino])
        
        return "OK"
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return "OK"
    

if __name__ == '__main__':
    print("Servidor Flask iniciado")
    print("📍 Accede a: http://localhost:5500")
    print("⏹️  Presiona Ctrl+C para detener")
    app.run(host='0.0.0.0', port=5500, debug=True)