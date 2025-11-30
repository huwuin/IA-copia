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

#Control de ejecucion
ultima_ejecucion = 0

#Servir archivos estaticos
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('img', filename)

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    return send_from_directory('docs', filename)

#Servir todas las paginas HTML
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<page_name>')
def serve_page(page_name):
    if page_name.endswith('.html'):
        return send_from_directory('.', page_name)
    return "PPagina no encontrada", 404

@app.route('/ejecutar-app', methods=['POST', 'GET'])
def ejecutar_app():
    """Ejecuta la app con los parametros de origen y destino"""
    global ultima_ejecucion
    
    try:
        #Control de tiempo
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
        
        print(f"dYs? EJECUTANDO APP: {origen} -> {destino}")
        
        #EJECUTAR CON PARAMETROS (usar el interprete actual para evitar problemas de PATH)
        app_path = os.path.join(os.getcwd(), 'app.py')
        python_exec = sys.executable or 'python'

        if os.name == 'nt':
            try:
                #Registrar salida en un archivo para depuracion y cerrar el descriptor
                log_path = os.path.join(os.getcwd(), 'app_launch.log')
                with open(log_path, 'a', encoding='utf-8') as logf:
                    logf.write(f"[LAUNCH] {time.ctime()} - Lanzando: {python_exec} {app_path} {origen} {destino}\n")

                #Intentar usar pythonw y evitar mostrar una consola adicional
                pythonw_exec = python_exec
                if python_exec.lower().endswith('python.exe'):
                    candidate = python_exec[:-len('python.exe')] + 'pythonw.exe'
                    if os.path.exists(candidate):
                        pythonw_exec = candidate

                creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                subprocess.Popen(
                    [pythonw_exec, app_path, origen, destino],
                    cwd=os.getcwd(),
                    creationflags=creation_flags,
                    close_fds=True
                )
            except Exception as e:
                print(f"Error lanzando app en Windows: {e}")
                try:
                    subprocess.Popen(
                        [python_exec, app_path, origen, destino],
                        cwd=os.getcwd(),
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                        close_fds=True
                    )
                except Exception as e2:
                    print(f"Segundo intento fallA3: {e2}")
        else:
            #Para Unix tambien registrar en log
            try:
                logf = open(os.path.join(os.getcwd(), 'app_launch.log'), 'a', encoding='utf-8')
                logf.write(f"[LAUNCH] {time.ctime()} - Lanzando: {python_exec} {app_path} {origen} {destino}\n")
                logf.flush()
                subprocess.Popen([python_exec, app_path, origen, destino], stdout=logf, stderr=logf, cwd=os.getcwd())
            except Exception as e:
                print(f"Error lanzando app en Unix: {e}")
        
        return "OK"
            
    except Exception as e:
        print(f"�?O Error: {e}")
        return "OK"
    

if __name__ == '__main__':
    print("Servidor Flask iniciado")
    print("dY\"? Accede a: http://localhost:5500")
    print("�?1�,?  Presiona Ctrl+C para detener")

    #Ejecutar sin reloader/debug para evitar que Flask cree procesos hijos

    app.run(host='0.0.0.0', port=5500, debug=False)
