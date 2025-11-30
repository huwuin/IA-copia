import os
import subprocess
import sys
import webbrowser
import time

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")

def ejecutar_comando(comando, descripcion=""):
    """Ejecuta un comando y maneja errores"""
    if descripcion:
        print(f"📦 {descripcion}...")
    
    try:
        resultado = subprocess.run(comando, shell=True, check=True, 
                                 capture_output=True, text=True, cwd=BASE_DIR)
        print(f"✅ {descripcion} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {descripcion}:")
        print(f"   Comando: {e.cmd}")
        print(f"   Error: {e.stderr}")
        return False
    except FileNotFoundError as e:
        print(f"❌ No se pudo encontrar el ejecutable: {e}")
        return False

def main():
    print("🚀 Iniciando aplicación Metro CDMX...")
    
    # 1. Crear entorno virtual si no existe
    if not os.path.exists(VENV_DIR):
        print("🔧 Creando entorno virtual...")
        if not ejecutar_comando(f'"{sys.executable}" -m venv "{VENV_DIR}"', "Creando entorno virtual"):
            print("❌ Falló la creación del entorno virtual")
            return
    
    # 2. Determinar rutas del entorno virtual
    if sys.platform == "win32":
        python_venv = os.path.join(VENV_DIR, "Scripts", "python.exe")
        pip_venv = os.path.join(VENV_DIR, "Scripts", "pip.exe")
        # Rutas alternativas por si las anteriores no funcionan
        python_venv_alt = os.path.join(VENV_DIR, "Scripts", "python")
        pip_venv_alt = os.path.join(VENV_DIR, "Scripts", "pip")
    else:
        python_venv = os.path.join(VENV_DIR, "bin", "python3")
        pip_venv = os.path.join(VENV_DIR, "bin", "pip3")
        python_venv_alt = os.path.join(VENV_DIR, "bin", "python")
        pip_venv_alt = os.path.join(VENV_DIR, "bin", "pip")
    
    # Verificar que los ejecutables existen
    python_final = python_venv if os.path.exists(python_venv) else python_venv_alt
    pip_final = pip_venv if os.path.exists(pip_venv) else pip_venv_alt
    
    if not os.path.exists(python_final):
        print(f"❌ No se pudo encontrar Python en el entorno virtual: {python_final}")
        return
    
    print(f"📍 Python del venv: {python_final}")
    print(f"📍 Pip del venv: {pip_final}")
    
    # 3. Actualizar pip primero
    if not ejecutar_comando(f'"{python_final}" -m pip install --upgrade pip', "Actualizando pip"):
        print("⚠️  Continuando sin actualizar pip...")
    
    # 4. Instalar dependencias
    requirements_file = os.path.join(BASE_DIR, "requirements.txt")
    if os.path.exists(requirements_file):
        if not ejecutar_comando(f'"{python_final}" -m pip install -r "{requirements_file}"', "Instalando dependencias"):
            print("❌ Falló la instalación de dependencias")
            return
    else:
        print("📋 Instalando dependencias manualmente...")
        dependencias = [
            "flask",
            "ttkbootstrap", 
            "pillow",
            "networkx"
        ]
        for dep in dependencias:
            if not ejecutar_comando(f'"{python_final}" -m pip install {dep}', f"Instalando {dep}"):
                print(f"❌ Falló la instalación de {dep}")
                return
    
    # 5. Verificar instalaciones críticas
    print("🔍 Verificando instalaciones...")
    verificaciones = [
        (f'"{python_final}" -c "import flask;', "Flask"),
        (f'"{python_final}" -c "import ttkbootstrap;', "ttkbootstrap"),
        (f'"{python_final}" -c "import PIL;', "Pillow"),
        (f'"{python_final}" -c "import networkx;', "NetworkX"),
        (f'"{python_final}" -c "import tkinter;', "Tkinter")
    ]
    
    for comando, modulo in verificaciones:
        if not ejecutar_comando(comando, f"Verificando {modulo}"):
            print(f"❌ {modulo} no está disponible")
    
    # 6. Lanzar servidor Flask
    print("🌐 Iniciando servidor Flask...")
    server_file = os.path.join(BASE_DIR, "server.py")
    
    try:
        # Lanzar servidor en segundo plano
        proceso_flask = subprocess.Popen(
            [python_final, server_file],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar un poco a que el servidor inicie
        time.sleep(3)
        
        # 7. Abrir navegador automáticamente
        print("🌍 Abriendo navegador en http://localhost:5000")
        webbrowser.open("http://localhost:5000")
        
        print("✅ Aplicación iniciada correctamente!")
        print("📍 URL: http://localhost:5000")
        print("⏹️  Para detener: Cierra esta ventana o presiona Ctrl+C")
        
        # Esperar a que el proceso termine
        proceso_flask.wait()
        
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
    finally:
        if 'proceso_flask' in locals():
            proceso_flask.terminate()

if __name__ == "__main__":
    main()


# import os
# import subprocess
# import sys
# import webbrowser

# # Ruta base del proyecto
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# VENV_DIR = os.path.join(BASE_DIR, "venv")

# # Detectar comandos de python
# PY = "python3" if sys.platform != "win32" else "python"

# # 1. Crear entorno virtual si no existe
# if not os.path.exists(VENV_DIR):
#     print("Creando entorno virtual...")
#     subprocess.check_call([PY, "-m", "venv", VENV_DIR])

# # 2. Activar interprete dentro del venv
# if sys.platform == "win32":
#     PY_VENV = os.path.join(VENV_DIR, "Scripts", "python.exe")
#     PIP_VENV = os.path.join(VENV_DIR, "Scripts", "pip.exe")
# else:
#     PY_VENV = os.path.join(VENV_DIR, "bin", "python3")
#     PIP_VENV = os.path.join(VENV_DIR, "bin", "pip3")

# # 3. Instalar dependencias
# print("Instalando dependencias requeridas...")
# subprocess.check_call([PIP_VENV, "install", "-r", "requirements.txt"])

# # 4. Lanzar servidor Flask
# print("Iniciando servidor Flask...")
# subprocess.Popen([PY_VENV, "server.py"])

# # 5. Abrir navegador automáticamente
# print("Abriendo navegador en http://localhost:5000")
# webbrowser.open("http://localhost:5000")
