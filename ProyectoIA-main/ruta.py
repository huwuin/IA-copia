import math
import networkx as nx
from flask import jsonify

#Radio de la Tierra en metros
RADIO_TIERRA = 6371000.0
#Imposiciones del usuario
accesibilidad = False
bici = False

#Función que recibe las coordenadas de dos puntos (latitud y longitud en grados) y retorna la distancia entre ellos en metros.
def haversine(latitud1, longitud1, latitud2, longitud2):
    #Convertir grados a radianes
    lat1_rad = math.radians(latitud1)
    lat2_rad = math.radians(latitud2)
    delta_lat_rad = math.radians(latitud2 - latitud1)
    delta_lon_rad = math.radians(longitud2 - longitud1)

    a = (math.sin(delta_lat_rad / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon_rad / 2) ** 2)
    angulo_central = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return RADIO_TIERRA * angulo_central

#Inicializa el grafo que representa las líneas y estaciones del metro
def inicializar_grafo():
    grafo = nx.Graph()
    #Agregar nodos con coordenadas (latitud y longitud)
    grafo.add_node("Balderas", latitud=19.427581967055374, longitud=-99.14762784249862,
                    px=1546, py=357, accesibilidad=True, bici=True, lineas=["1", "3"])
    grafo.add_node("Cuauhtémoc", latitud=19.425796516896693, longitud=-99.15463964895125,
                    px=1360, py=353, accesibilidad=True, bici=True, lineas=["1"])
    grafo.add_node("Insurgentes", latitud=19.424199545463196, longitud=-99.16323859128006,
                    px=1145, py= 353, accesibilidad=True, bici=True, lineas=["1"])
    grafo.add_node("Sevilla", latitud=19.421677038575385, longitud=-99.17069365319718,
                    px=997, py=490, accesibilidad=True, bici=True, lineas=["1"])
    grafo.add_node("Chapultepec", latitud=19.4207172842136, longitud=-99.17661859737528,
                    px=841, py=658, accesibilidad=False, bici=True, lineas=["1"])
    grafo.add_node("Juanacatlán", latitud=19.413120121539066, longitud=-99.18131535929254,
                    px=681, py=805, accesibilidad=False, bici=True, lineas=["1"])
    grafo.add_node("Tacubaya", latitud=19.402089994777743, longitud=-99.1874125777875,
                    px=521, py=965, accesibilidad=False, bici=False, lineas=["1", "7", "9"])
    grafo.add_node("Juárez", latitud=19.433637318098473, longitud=-99.1465687792223,
                    px=1546, py=62, accesibilidad=True, bici=True, lineas=["3"])
    grafo.add_node("Niños Héroes", latitud=19.41938394784802, longitud=-99.15030828021668,
                    px=1549, py=508, accesibilidad=False, bici=False, lineas=["3"])
    grafo.add_node("Hospital General", latitud=19.41372633561362, longitud=-99.1532687185439,
                    px=1549, py=671, accesibilidad=True, bici=True, lineas=["3"])
    grafo.add_node("Centro Médico", latitud=19.40649816936503, longitud=-99.15520083736972,
                    px=1549, py=966, accesibilidad=True, bici=True, lineas=["3", "9"])
    grafo.add_node("Etiopía", latitud=19.395996847288366, longitud=-99.15585164945027,
                    px=1549, py=1127, accesibilidad=True, bici=True, lineas=["3"])
    grafo.add_node("Eugenia", latitud=19.386115304363674, longitud=-99.15719035312618,
                    px=1549, py=1279, accesibilidad=False, bici=True, lineas=["3"])
    grafo.add_node("División del Norte", latitud=19.37929638161199, longitud=-99.1592749567583,
                    px=1549, py=1442, accesibilidad=False, bici=True, lineas=["3"])
    grafo.add_node("Zapata", latitud=19.370727509779332, longitud=-99.16514120440691,
                    px=1549, py=1597, accesibilidad=True, bici=True, lineas=["3", "12"])
    grafo.add_node("Coyoacán", latitud=19.361285721501574, longitud=-99.17082355361505,
                    px=1549, py=1758, accesibilidad=False, bici=True, lineas=["3"])
    grafo.add_node("Viveros", latitud=19.353986310569425, longitud=-99.17572124227962,
                    px=1549, py=1910, accesibilidad=False, bici=False, lineas=["3"])
    grafo.add_node("Miguel Ángel de Quevedo", latitud=19.346064801837734, longitud=-99.18118723696888,
                    px=1549, py=2074, accesibilidad=False, bici=False, lineas=["3"])
    grafo.add_node("Copilco", latitud=19.336113516532745, longitud=-99.17691806169765,
                    px=1549, py=2227, accesibilidad=True, bici=False, lineas=["3"])
    grafo.add_node("Polanco", latitud=19.433894110333178, longitud=-99.19104369737502,
                    px=521, py=110, accesibilidad=False, bici=True, lineas=["7"])
    grafo.add_node("Auditorio", latitud=19.42511182099693, longitud=-99.19191273307231,
                    px=521, py=410, accesibilidad=False, bici=True, lineas=["7"])
    grafo.add_node("Constituyentes", latitud=19.411720682784683, longitud=-99.19134876816813,
                    px=521, py= 694, accesibilidad=False, bici=True, lineas=["7"])
    grafo.add_node("San Pedro de los Pinos", latitud=19.39138344423236, longitud=-99.18581668033438,
                    px=521, py=1235, accesibilidad=False, bici=True, lineas=["7"])
    grafo.add_node("San Antonio", latitud=19.384926617725515, longitud=-99.18624583378435,
                    px=521, py=1386, accesibilidad=False, bici=True, lineas=["7"])
    grafo.add_node("Mixcoac", latitud=19.376135540543526, longitud=-99.18786945363773,
                    px=521, py=1591, accesibilidad=True, bici=True, lineas=["7", "12"])
    grafo.add_node("Lázaro Cardenas", latitud=19.407204136564253, longitud=-99.14468662342163,
                    px=1969, py=966, accesibilidad=False, bici=False, lineas=["9"])
    grafo.add_node("Chilpancingo", latitud=19.405917115614272, longitud=-99.16847983106982,
                    px=1289, py=966, accesibilidad=False, bici=True, lineas=["9"])
    grafo.add_node("Patriotismo", latitud=19.40601315449567, longitud=-99.1789407161755,
                    px=885, py=966, accesibilidad=False, bici=True, lineas=["9"])
    grafo.add_node("Eje Central", latitud=19.3613532779116, longitud=-99.15150662283324,
                    px=2014, py=1590, accesibilidad=True, bici=False, lineas=["12"])
    grafo.add_node("Parque de los Venados", latitud=19.3708019292425, longitud=-99.15846897567188,
                    px=1785, py=1591, accesibilidad=True, bici=True, lineas=["12"])
    grafo.add_node("Hospital 20 de Noviembre", latitud=19.371882163132256, longitud=-99.17177970091232,
                    px=1158, py=1590, accesibilidad=True, bici=True, lineas=["12"])
    grafo.add_node("Insurgentes del Sur", latitud=19.373502745432333, longitud=-99.1784683959002,
                    px=809, py=1590, accesibilidad=True, bici=True, lineas=["12"])
    grafo.add_node("Barranca del Muerto", latitud=19.361458309525723, longitud=-99.18926375664034,
                    px=521, py=1862, accesibilidad=False, bici=False, lineas=["7"])
    grafo.add_node("Observatorio", latitud=19.398266522973344, longitud=-99.20033572803825,
                    px=341, py=1147, accesibilidad=True, bici=False, lineas=["1"])
    grafo.add_node("Universidad", latitud=19.324280705331546, longitud=-99.17393134832986,
                    px=1549, py=2369, accesibilidad=True, bici=False, lineas=["3"])
    # Agregar aristas con pesos (distancias reales en metros)
    #Línea 1
    grafo.add_edge("Balderas", "Cuauhtémoc", distancia=709)
    grafo.add_edge("Cuauhtémoc", "Insurgentes", distancia=1093)
    grafo.add_edge("Insurgentes", "Sevilla", distancia=945)
    grafo.add_edge("Sevilla", "Chapultepec", distancia=801)
    grafo.add_edge("Chapultepec", "Juanacatlán", distancia=1273)
    grafo.add_edge("Juanacatlán", "Tacubaya", distancia=1458)
    grafo.add_edge("Tacubaya", "Observatorio", distancia=1562)
    #Línea 3
    grafo.add_edge("Juárez", "Balderas", distancia=959)
    grafo.add_edge("Balderas", "Niños Héroes", distancia=965)
    grafo.add_edge("Niños Héroes", "Hospital General", distancia=859)
    grafo.add_edge("Hospital General", "Centro Médico", distancia=953)
    grafo.add_edge("Centro Médico", "Etiopía", distancia=1419)
    grafo.add_edge("Etiopía", "Eugenia", distancia=1250)
    grafo.add_edge("Eugenia", "División del Norte", distancia=1015)
    grafo.add_edge("División del Norte", "Zapata", distancia=1094)
    grafo.add_edge("Zapata", "Coyoacán", distancia=1453)
    grafo.add_edge("Coyoacán", "Viveros", distancia=1208)
    grafo.add_edge("Viveros", "Miguel Ángel de Quevedo", distancia=1124)
    grafo.add_edge("Miguel Ángel de Quevedo", "Copilco", distancia=1595)
    grafo.add_edge("Copilco", "Universidad", distancia=1606)
    #Línea 7
    grafo.add_edge("Polanco", "Auditorio", distancia=1112)
    grafo.add_edge("Auditorio", "Constituyentes", distancia=1730)
    grafo.add_edge("Constituyentes", "Tacubaya", distancia=1305)
    grafo.add_edge("Tacubaya", "San Pedro de los Pinos", distancia=1384)
    grafo.add_edge("San Pedro de los Pinos", "San Antonio", distancia=906)
    grafo.add_edge("San Antonio", "Mixcoac", distancia=1088)
    grafo.add_edge("Mixcoac", "Barranca del Muerto", distancia=1776)
    #Línea 9
    grafo.add_edge("Lázaro Cardenas", "Centro Médico", distancia=1359)
    grafo.add_edge("Centro Médico", "Chilpancingo", distancia=1452)
    grafo.add_edge("Chilpancingo", "Patriotismo", distancia=1295)
    grafo.add_edge("Patriotismo", "Tacubaya", distancia=1433)
    #Línea 12
    grafo.add_edge("Eje Central", "Parque de los Venados", distancia=1580)
    grafo.add_edge("Parque de los Venados", "Zapata", distancia=863)
    grafo.add_edge("Zapata", "Hospital 20 de Noviembre", distancia=750)
    grafo.add_edge("Hospital 20 de Noviembre", "Insurgentes del Sur", distancia=1025)
    grafo.add_edge("Insurgentes del Sur", "Mixcoac", distancia=951)
    return grafo

#Grafo global
G = inicializar_grafo()

def peso_arista(u, v, data):
    d = data.get('distancia', 0)

    #Penalización por cambio de línea si activaste accesibilidad (solo afecta a Tacubaya)
    if accesibilidad and u == "Tacubaya":
        #Aplicar penalización si se cambia de línea 
        d += 5000

    return d

def estacion_biciparking_mas_cercana(origen):
    lat_origen = G.nodes[origen]['latitud']
    lon_origen = G.nodes[origen]['longitud']
    
    #Filtramos solo las estaciones que sí tienen biciparking
    bici_estaciones = [(nodo, G.nodes[nodo]['latitud'], G.nodes[nodo]['longitud'])
                        for nodo in G.nodes if G.nodes[nodo].get('bici', False)]
    
    if not bici_estaciones:
        return origen  #por si ninguna tiene biciparking
    
    #Buscamos la más cercana
    estacion_cercana = min(
        bici_estaciones,
        key=lambda x: haversine(lat_origen, lon_origen, x[1], x[2])
    )
    
    return estacion_cercana[0]


#Función heurística para A*
def h(actual, objetivo):
    output = 0
    lat1 = G.nodes[actual]['latitud']
    lon1 = G.nodes[actual]['longitud']
    lat2 = G.nodes[objetivo]['latitud']
    lon2 = G.nodes[objetivo]['longitud']
    output = haversine(lat1, lon1, lat2, lon2)
    return output

#Algoritmo A* para encontrar la ruta más corta
def a_estrella(origen, destino, G):
    ruta = nx.astar_path(G, origen, destino, heuristic=h, weight=peso_arista)
    distancia_total = nx.astar_path_length(G, origen, destino, heuristic=h, weight=peso_arista)
    #Calcular líneas visitadas
    lineas_visitadas = []
    for i in range(len(ruta)-1):
        inter = set(G.nodes[ruta[i]]['lineas']).intersection(G.nodes[ruta[i+1]]['lineas'])
        if inter:
            lineas_visitadas.append(inter.pop())
    lineas_visitadas = sorted(set(lineas_visitadas), key=int)

    tiempo_minutos = round(distancia_total / 666) + 3 * (len(lineas_visitadas) - 1) #666 metros por minuto aprox

    return ruta, tiempo_minutos, lineas_visitadas