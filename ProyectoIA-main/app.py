import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ruta import a_estrella, G, estacion_biciparking_mas_cercana
from PIL import Image, ImageTk
from styles import aplicar_estilos
import ruta
import math

class App:
    def __init__(self, root, origen_param=None, destino_param=None):
        self.root = root
        self.origen_param = origen_param
        self.destino_param = destino_param

        # ✅ CONFIGURACIÓN PARA PRIMER PLANO - AL INICIO
        self.root.title("Metro CDMX - Calculador de Ruta")
        self.root.geometry("1000x750")
        
        # Forzar que esté siempre al frente al iniciar
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        self.root.lift()
        
        # Después de 1 segundo, quitar el 'always on top' pero mantener foco
        self.root.after(1000, lambda: self.root.attributes('-topmost', False))

        # ----------------- Tamaño de la ventana -----------------
        self.VENTANA_ANCHO = 910
        self.VENTANA_ALTO  = 750
        self.ANCHO_PANEL = 200

        root.resizable(False, False)

        # ----------------- Frame principal -----------------
        self.frame_principal = ttk.Frame(root, padding=0)
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        # Panel lateral
        self.panel = ttk.Frame(self.frame_principal, padding=10)
        self.panel.pack(side=tk.LEFT, fill=tk.Y, ipadx=20)

        # ----------------- Selector de hora -----------------

        horas = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
        minutos = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]

        ttk.Label(self.panel, text="Escoge la hora a la que viajarás:",
                    style="FieldLabel.TLabel").pack(anchor=tk.W)


        # Frame horizontal para reunir hora : minutos
        hora_frame = ttk.Frame(self.panel)
        hora_frame.pack(anchor=tk.W, pady=(0,10))

        # Combobox hora
        self.hora_spin = ttk.Combobox(hora_frame, values=horas, state="readonly",
                                        width=3, style="Select.TCombobox")

        self.hora_spin.pack(side=tk.LEFT)

        # Etiqueta :
        ttk.Label(hora_frame, text=":", padding=(5,0)).pack(side=tk.LEFT)

        # Combobox minutos
        self.min_spin = ttk.Combobox(hora_frame, values=minutos, state="readonly",
                                        width=3, style="Select.TCombobox")

        self.min_spin.pack(side=tk.LEFT)

        # Valores por defecto
        self.hora_spin.set("12")
        self.min_spin.set("00")

        # Lista de estaciones
        estaciones = sorted(G.nodes)

        ttk.Label(self.panel, text="Estación origen:",
                    style="FieldLabel.TLabel").pack(anchor=tk.W, pady=(0,2))

        self.origen_combo = ttk.Combobox(self.panel, values=estaciones,
                                            state="readonly", style="Select.TCombobox")

        self.origen_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.panel, text="Estación destino:",
                    style="FieldLabel.TLabel").pack(anchor=tk.W, pady=(10,2))

        self.destino_combo = ttk.Combobox(self.panel, values=estaciones,
                                            state="readonly", style="Select.TCombobox")

        self.destino_combo.pack(fill=tk.X, pady=5)

        # ✅ ESTABLECER VALORES DESDE PARÁMETROS
        if self.origen_param and self.origen_param in estaciones:
            self.origen_combo.set(self.origen_param)
        else:
            self.origen_combo.set(estaciones[0])
            
        if self.destino_param and self.destino_param in estaciones:
            self.destino_combo.set(self.destino_param)
        else:
            self.destino_combo.set(estaciones[0])

        # ----------------- Checkboxes -----------------
        self.checkbox_frame = ttk.Frame(self.panel)
        self.checkbox_frame.pack(pady=(5,10), fill=tk.X)

        # Accesibilidad
        try:
            img_acc = Image.open("accesibilidad.png")
            img_acc.thumbnail((25,25), Image.LANCZOS)
            self.img_acc_tk = ImageTk.PhotoImage(img_acc)
        except Exception as e:
            print("Error cargando accesibilidad.png:", e)
            self.img_acc_tk = None

        self.accesibilidad_var = tk.BooleanVar(value=False)
        if self.img_acc_tk:
            self.accesibilidad_cb = ttk.Checkbutton(self.checkbox_frame, text="Accesibilidad",
                                                variable=self.accesibilidad_var,
                                                bootstyle="info-round-toggle",
                                                image=self.img_acc_tk)
        else:
            self.accesibilidad_cb = ttk.Checkbutton(self.checkbox_frame, text="Accesibilidad",
                                                    variable=self.accesibilidad_var,
                                                    bootstyle="info-round-toggle")
        self.accesibilidad_cb.pack(side=tk.LEFT, padx=(0,5))

        # Bici
        try:
            img_bici = Image.open("logo-ecobici.png")
            img_bici.thumbnail((25,25), Image.LANCZOS)
            self.img_bici_tk = ImageTk.PhotoImage(img_bici)
        except Exception as e:
            print("Error cargando logo-ecobici.png:", e)
            self.img_bici_tk = None

        self.bici_var = tk.BooleanVar(value=False)
        if self.img_bici_tk:
            self.bici_cb = ttk.Checkbutton(self.checkbox_frame, text="Bici",
                                        variable=self.bici_var,
                                        bootstyle="success-round-toggle",
                                        image=self.img_bici_tk)
        else:
            self.bici_cb = ttk.Checkbutton(self.checkbox_frame, text="Bici",
                                        variable=self.bici_var,
                                        bootstyle="success-round-toggle")
        self.bici_cb.pack(side=tk.LEFT, padx=(5,0))

        # Botón de mostrar ruta
        ttk.Button(self.panel, text="Mostrar ruta", bootstyle="success-outline",
                    command=self.calcular_ruta).pack(pady=(10,5), fill=tk.X)

        # ----------------- Label tiempo estimado -----------------
        self.tiempo_label = ttk.Label(self.panel, text="", wraplength=200, justify=tk.CENTER)
        self.tiempo_label.pack(fill=tk.X, pady=(5,5))

        # Espacio ruta
        self.ruta_frame = ttk.Frame(self.panel, padding=5)
        self.ruta_frame.pack(fill=tk.X, pady=5)

        self.linea_superior = tk.Frame(self.ruta_frame, height=1, bg="gray")
        self.linea_superior.pack(fill=tk.X, pady=(0,3))

        self.resultado_label = ttk.Label(self.ruta_frame, text="Aquí se mostrará tu ruta",
                                        wraplength=200, justify=tk.CENTER)
        self.resultado_label.pack(fill=tk.X)

        self.linea_inferior = tk.Frame(self.ruta_frame, height=1, bg="gray")
        self.linea_inferior.pack(fill=tk.X, pady=(3,0))

        # Área derecha canvas
        self.area = ttk.Frame(self.frame_principal, padding=0)
        self.area.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.area, bg="white",
                                width=self.VENTANA_ANCHO - self.ANCHO_PANEL,
                                height=self.VENTANA_ALTO)
        self.canvas.pack()

        # ----------------- Imagen mapa -----------------
        try:
            self.mapa_img_original = Image.open("mapa_metro_HD.png")
            self.imagen_width_original, self.imagen_height_original = self.mapa_img_original.size

            max_width = self.VENTANA_ANCHO - self.ANCHO_PANEL
            max_height = self.VENTANA_ALTO
            escala = min(max_width / self.imagen_width_original, max_height / self.imagen_height_original)

            self.imagen_canvas_width = int(self.imagen_width_original * escala)
            self.imagen_canvas_height = int(self.imagen_height_original * escala)

            img = self.mapa_img_original.resize((self.imagen_canvas_width, self.imagen_canvas_height), Image.LANCZOS)
            self.mapa_tk = ImageTk.PhotoImage(img)

            self.offset_x = (max_width - self.imagen_canvas_width)//2
            self.offset_y = (max_height - self.imagen_canvas_height)//2

            self.canvas.create_image(self.offset_x, self.offset_y, anchor="nw", image=self.mapa_tk, tags="mapa")
        except Exception as e:
            print("Error cargando mapa_metro_HD.png:", e)
            self.mapa_img_original = None

        # ----------------- Imagen tren -----------------
        try:
            self.tren_img_original = Image.open("tren.png")
            self.tren_img_original.thumbnail((30, 30), Image.LANCZOS)
            self.tren_tk = ImageTk.PhotoImage(self.tren_img_original)
        except Exception as e:
            print("Error cargando tren.png:", e)
            self.tren_tk = None

        self.tren = None
        self.animacion_id = None

        # ✅ CALCULAR RUTA AUTOMÁTICAMENTE SI HAY PARÁMETROS VÁLIDOS
        if (self.origen_param and self.destino_param and 
            self.origen_param in estaciones and self.destino_param in estaciones and
            self.origen_param != self.destino_param):
            
            print(f"✅ Calculando ruta automática: {self.origen_param} -> {self.destino_param}")
            # Esperar a que la interfaz se cargue completamente
            self.root.after(1500, self.calcular_ruta)

    # ----------------- Rutas -----------------
    def calcular_ruta(self):
        origen_usuario = self.origen_combo.get()
        destino = self.destino_combo.get()

        # Paradas iguales → error
        if origen_usuario == destino:
            self.resultado_label.config(text="Selecciona dos paradas distintas.")
            self.tiempo_label.config(text="")
            self.detener_animacion()
            return

        hora = int(self.hora_spin.get())

        # Metro cerrado 1:00 - 6:00
        if 1 <= hora < 6:
            self.resultado_label.config(text="El metro está cerrado de 1:00 a 6:00.")
            self.tiempo_label.config(text="")
            self.detener_animacion()
            return

        ruta.accesibilidad = self.accesibilidad_var.get()
        ruta.bici = self.bici_var.get()

        origen = origen_usuario
        origen_cambiado = False
        if ruta.bici:
            nuevo_origen = estacion_biciparking_mas_cercana(origen)
            if nuevo_origen != origen:
                origen = nuevo_origen
                origen_cambiado = True

        # --- Tiempo adicional por tramo en bici ---
        tiempo_bici_min = 0
        if origen_cambiado:
            # Coordenadas del punto original y del nuevo punto con biciparking
            lat1 = G.nodes[origen_usuario]["latitud"]
            lon1 = G.nodes[origen_usuario]["longitud"]
            lat2 = G.nodes[origen]["latitud"]
            lon2 = G.nodes[origen]["longitud"]

            # Distancia en metros
            dist_m = ruta.haversine(lat1, lon1, lat2, lon2)

            # Velocidad media de bici: 15 km/h ≈ 250 m/min
            velocidad_bici_m_min = 250

            tiempo_bici_min = int(dist_m / velocidad_bici_m_min)

        if origen not in G.nodes or destino not in G.nodes:
            self.resultado_label.config(text="Error: estación no válida")
            self.tiempo_label.config(text="")
            return

        # ----------------- Usar ruta y tiempo devueltos por a_estrella -----------------
        try:
            ruta_calc, tiempo_min, lineas_unicas = a_estrella(origen, destino, G)
            
            # ---- Sumamos el tiempo que se tarda en bici (0 si no se viaja en bici)
            tiempo_min += tiempo_bici_min

            # ---- Aumentar tiempo en horas punta ----
            factor_hora_punta = 1.3
            if 7 <= hora < 10 or 13 <= hora < 15 or 17 <= hora < 19:
                tiempo_min = int(tiempo_min * factor_hora_punta)

            texto_lineas = "Línea " + lineas_unicas[0] if len(lineas_unicas) == 1 else "Líneas " + ", ".join(lineas_unicas)

            self.tiempo_label.config(text=f"Tiempo estimado:\n {tiempo_min} minutos \n {texto_lineas}")

            # ----------------- Mostrar ruta con posible cambio de origen bici -----------------
            if origen_cambiado:
                texto_bici = f"Bici: {origen_usuario} → {origen}"
                texto_metro = "Metro: " + " → ".join(ruta_calc)
                self.resultado_label.config(text=f"{texto_bici}\n{texto_metro}")
            else:
                self.resultado_label.config(text=" → ".join(ruta_calc))

            self.ultima_ruta = ruta_calc
            self.dibujar_ruta(ruta_calc)

            # Preparar animación
            if self.mapa_img_original:
                escala_x = self.imagen_canvas_width / self.imagen_width_original
                escala_y = self.imagen_canvas_height / self.imagen_height_original
                self.coords_ruta = [(G.nodes[n]['px']*escala_x + self.offset_x,
                                    G.nodes[n]['py']*escala_y + self.offset_y) for n in ruta_calc]

                if self.tren:
                    self.canvas.delete(self.tren)
                    self.tren = None

                self.cancelar_animacion()
                self.animar_tren()

        except Exception as e:
            self.resultado_label.config(text=f"Error calculando ruta: {str(e)}")
            self.tiempo_label.config(text="")

    # ----------------- Dibujar ruta -----------------
    def dibujar_ruta(self, ruta_calc):
        if self.mapa_img_original is None:
            return
            
        self.canvas.delete("ruta")
        escala_x = self.imagen_canvas_width / self.imagen_width_original
        escala_y = self.imagen_canvas_height / self.imagen_height_original

        coords = [(G.nodes[n]['px']*escala_x + self.offset_x,
                    G.nodes[n]['py']*escala_y + self.offset_y) for n in ruta_calc]

        for i in range(len(coords)-1):
            self.canvas.create_line(coords[i][0], coords[i][1],
                                    coords[i+1][0], coords[i+1][1],
                                    fill="blue", width=3, tags="ruta")
        for x, y in coords:
            r = 5
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue", tags="ruta")

        self.coords_ruta = coords

    # ----------------- Animación tren -----------------
    def animar_tren(self, idx_segmento=0, progreso=0.0, en_pausa=False):
        if self.tren_tk is None or not hasattr(self, "coords_ruta") or len(self.coords_ruta) < 2:
            return

        coords = self.coords_ruta

        if idx_segmento >= len(coords) - 1:
            x_fin, y_fin = coords[-1]
            if self.tren is None:
                self.tren = self.canvas.create_image(x_fin, y_fin, image=self.tren_tk)
            else:
                self.canvas.coords(self.tren, x_fin, y_fin)
            self.animacion_id = self.root.after(1000, lambda: self.animar_tren(0, 0.0, True))
            return

        x1, y1 = coords[idx_segmento]
        x2, y2 = coords[idx_segmento + 1]

        x = x1 + (x2 - x1) * progreso
        y = y1 + (y2 - y1) * progreso

        angulo = math.degrees(math.atan2(y2 - y1, x2 - x1))
        img_rotada = self.tren_img_original.rotate(-angulo, expand=True)
        self.tren_tk_rotada = ImageTk.PhotoImage(img_rotada)

        if self.tren is None:
            self.tren = self.canvas.create_image(x, y, image=self.tren_tk_rotada)
        else:
            self.canvas.coords(self.tren, x, y)
            self.canvas.itemconfig(self.tren, image=self.tren_tk_rotada)

        if en_pausa:
            self.animacion_id = self.root.after(1000, lambda: self.animar_tren(idx_segmento, progreso, False))
            return

        nuevo_progreso = progreso + 0.02
        if nuevo_progreso >= 1.0:
            self.animacion_id = self.root.after(20, lambda: self.animar_tren(idx_segmento + 1, 0.0))
        else:
            self.animacion_id = self.root.after(20, lambda: self.animar_tren(idx_segmento, nuevo_progreso))

    def cancelar_animacion(self):
        if self.animacion_id is not None:
            self.root.after_cancel(self.animacion_id)
            self.animacion_id = None

    def detener_animacion(self):
        # 1. Cancelar animación en curso
        if hasattr(self, "animacion_id") and self.animacion_id is not None:
            self.root.after_cancel(self.animacion_id)
            self.animacion_id = None

        # 2. Eliminar icono del tren (usa self.tren, no tren_icono)
        if hasattr(self, "tren") and self.tren is not None:
            self.canvas.delete(self.tren)
            self.tren = None

        # 3. Eliminar la línea azul y los puntos de la ruta
        self.canvas.delete("ruta")   # borra todo lo dibujado con tags="ruta"

        # 4. Limpiar también coordenadas de ruta para evitar animaciones residuales
        if hasattr(self, "coords_ruta"):
            self.coords_ruta = []

if __name__ == "__main__":
    import sys
    
    root = ttk.Window(themename="flatly")

    aplicar_estilos(root)
    
    # ✅ OBTENER PARÁMETROS DE LA LÍNEA DE COMANDOS
    origen_param = sys.argv[1] if len(sys.argv) > 1 else None
    destino_param = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🔧 Parámetros recibidos: origen='{origen_param}', destino='{destino_param}'")
    
    app = App(root, origen_param, destino_param)
    root.mainloop()
