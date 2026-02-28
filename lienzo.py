import pygame
import sys

# --- Inicialización y Configuración ---
pygame.init()
ANCHO, ALTO = 1100, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Procesos por Lotes - Primera Versión")

# --- Colores (Estilo Retro/8-bits) ---
COLOR_FONDO = (92, 148, 252)  # Azul cielo clásico
COLOR_TEXTO = (255, 255, 255)  # Blanco puro
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_TEXTO_OSCURO = (0, 0, 0)  # Negro para contraste en cajas activas
COLOR_CAJAS = (200, 76, 12)  # Naranja ladrillo
COLOR_CAJAS_ACTIVAS = (248, 216, 32)  # Amarillo bloque/moneda
COLOR_BORDES = (0, 0, 0)  # Negro puro (borde grueso retro)
COLOR_BOTON = (0, 168, 0)  # Verde tubería
COLOR_ERROR = (228, 0, 88)  # Rojo brillante

# Fuentes (Courier simula bien el aspecto retro/pixelado sin instalar fuentes extra)
fuente_titulo = pygame.font.SysFont("couriernew", 22, bold=True)
fuente_etiquetas = pygame.font.SysFont("couriernew", 16, bold=True)
fuente_pequena = pygame.font.SysFont("couriernew", 14, bold=True)


# --- CLASES ---
class InputBox:
    def __init__(self, x, y, w, h, texto=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_CAJAS
        self.color_texto = COLOR_TEXTO_BLANCO
        self.texto = texto
        self.txt_surface = fuente_etiquetas.render(texto, True, self.color_texto)
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False

            # Cambia color de fondo y de texto si está activa
            if self.activo:
                self.color = COLOR_CAJAS_ACTIVAS
                self.color_texto = COLOR_TEXTO_OSCURO
            else:
                self.color = COLOR_CAJAS
                self.color_texto = COLOR_TEXTO_BLANCO

            self.txt_surface = fuente_etiquetas.render(self.texto, True, self.color_texto)

        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    pass
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    self.texto += evento.unicode
                self.txt_surface = fuente_etiquetas.render(self.texto, True, self.color_texto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, COLOR_BORDES, self.rect, 3)  # Borde grueso de 3px
        pantalla.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class Proceso:
    def __init__(self, id_prog, nombre, operacion, tme):
        self.id = id_prog
        self.nombre = nombre
        self.operacion = operacion
        self.tme = int(tme)
        self.tiempo_transcurrido = 0
        self.tiempo_restante = self.tme
        self.resultado = None

    def ejecutar(self):
        try:
            self.resultado = eval(self.operacion)
        except ZeroDivisionError:
            self.resultado = "Err: Div/0"
        except:
            self.resultado = "Error"


# --- VARIABLES GLOBALES ---
estado = "CAPTURA"
procesos_capturados = []
lotes_pendientes = []
lote_actual = []
procesos_terminados = []
proceso_en_ejecucion = None

reloj_global = 0
ultimo_tick = 0
mensaje_error = ""
lotes_procesados_contador = 0

# Instanciar Cajas de Texto
caja_nombre = InputBox(120, 80, 180, 30)
caja_operacion = InputBox(120, 140, 180, 30)
caja_tme = InputBox(120, 200, 180, 30)
caja_id = InputBox(120, 260, 180, 30)
cajas = [caja_nombre, caja_operacion, caja_tme, caja_id]


# --- FUNCIONES DE LÓGICA ---
def limpiar_cajas():
    for caja in cajas:
        caja.texto = ''
        caja.txt_surface = fuente_etiquetas.render('', True, caja.color_texto)


def agregar_proceso():
    global mensaje_error
    nom = caja_nombre.texto.strip()
    ope = caja_operacion.texto.strip()
    tme = caja_tme.texto.strip()
    id_p = caja_id.texto.strip()

    if not nom or not ope or not tme or not id_p:
        mensaje_error = "LLENA TODO."
        return
    if not tme.isdigit() or int(tme) <= 0:
        mensaje_error = "TME > 0."
        return
    if any(p.id == id_p for p in procesos_capturados):
        mensaje_error = "ID YA EXISTE."
        return

    procesos_capturados.append(Proceso(id_p, nom, ope, tme))
    mensaje_error = "PROCESO OK."
    limpiar_cajas()


def iniciar_ejecucion():
    global estado, lotes_pendientes, ultimo_tick, mensaje_error
    if len(procesos_capturados) == 0:
        mensaje_error = "AGREGA PRIMERO."
        return

    for i in range(0, len(procesos_capturados), 4):
        lotes_pendientes.append(procesos_capturados[i:i + 4])

    estado = "EJECUCION"
    ultimo_tick = pygame.time.get_ticks()


# --- FUNCIONES DE DIBUJO ---
def dibujar_columna_captura(pantalla):
    titulo = fuente_titulo.render("CAPTURAR PROCESOS", True, COLOR_TEXTO)
    pantalla.blit(titulo, (60, 20))

    etiquetas = ["Nombre", "Operacion", "Tiempo(TME)", "ID"]
    y_pos = 80
    for i, etiqueta in enumerate(etiquetas):
        lbl = fuente_etiquetas.render(etiqueta, True, COLOR_TEXTO_BLANCO)
        pantalla.blit(lbl, (15, y_pos + 5))
        cajas[i].dibujar(pantalla)
        y_pos += 60

    # Botones cuadrados y gruesos
    btn_agregar = pygame.Rect(40, 350, 100, 40)
    pygame.draw.rect(pantalla, COLOR_BOTON, btn_agregar)
    pygame.draw.rect(pantalla, COLOR_BORDES, btn_agregar, 3)
    pantalla.blit(fuente_etiquetas.render("AGREGAR", True, COLOR_TEXTO_BLANCO), (55, 360))

    btn_ejecutar = pygame.Rect(170, 350, 110, 40)
    pygame.draw.rect(pantalla, COLOR_BOTON, btn_ejecutar)
    pygame.draw.rect(pantalla, COLOR_BORDES, btn_ejecutar, 3)
    pantalla.blit(fuente_etiquetas.render("EJECUTAR", True, COLOR_TEXTO_BLANCO), (180, 360))

    lbl_contador = fuente_etiquetas.render(f"AGREGADOS: {len(procesos_capturados)}", True, COLOR_TEXTO_BLANCO)
    pantalla.blit(lbl_contador, (100, 420))
    if mensaje_error:
        lbl_err = fuente_pequena.render(mensaje_error, True, COLOR_ERROR)
        pantalla.blit(lbl_err, (20, 450))

    pygame.draw.line(pantalla, COLOR_BORDES, (330, 0), (330, ALTO), 4)
    return btn_agregar, btn_ejecutar


def dibujar_columna_ejecucion(pantalla):
    titulo_lote = fuente_etiquetas.render("LOTE ACTUAL", True, COLOR_TEXTO)
    pantalla.blit(titulo_lote, (350, 25))

    lbl_restantes = fuente_etiquetas.render(f"PENDIENTES: {len(lotes_pendientes)}", True, COLOR_TEXTO)
    pantalla.blit(lbl_restantes, (550, 25))

    fondo_lote = pygame.Rect(350, 60, 350, 200)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_lote)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_lote, 3)

    pantalla.blit(fuente_pequena.render("ID      T.MAX      OPERACION", True, COLOR_TEXTO_BLANCO), (360, 65))
    pygame.draw.line(pantalla, COLOR_BORDES, (350, 85), (700, 85), 3)

    y_lote = 90
    for p in lote_actual:
        txt = f"{p.id:<8}{p.tme:<11}{p.operacion}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (360, y_lote))
        y_lote += 25

    titulo_proceso = fuente_titulo.render("PROCESO ACTUAL", True, COLOR_TEXTO)
    pantalla.blit(titulo_proceso, (450, 280))

    labels_proc = ["Nombre", "Operacion", "T.Transcurrido", "T.Restante", "ID"]
    vals_proc = ["", "", "", "", ""]
    if proceso_en_ejecucion:
        vals_proc = [
            proceso_en_ejecucion.nombre,
            proceso_en_ejecucion.operacion,
            str(proceso_en_ejecucion.tiempo_transcurrido),
            str(proceso_en_ejecucion.tiempo_restante),
            proceso_en_ejecucion.id
        ]

    y_pos = 330
    for i, etiqueta in enumerate(labels_proc):
        pantalla.blit(fuente_etiquetas.render(etiqueta, True, COLOR_TEXTO_BLANCO), (350, y_pos + 5))

        caja_info = pygame.Rect(520, y_pos, 180, 30)
        pygame.draw.rect(pantalla, COLOR_CAJAS, caja_info)
        pygame.draw.rect(pantalla, COLOR_BORDES, caja_info, 3)
        pantalla.blit(fuente_etiquetas.render(vals_proc[i], True, COLOR_TEXTO_BLANCO), (525, y_pos + 5))
        y_pos += 50

    pygame.draw.line(pantalla, COLOR_BORDES, (730, 0), (730, ALTO), 4)


def dibujar_columna_terminados(pantalla):
    titulo_final = fuente_titulo.render("PROCESOS TERMINADOS", True, COLOR_TEXTO)
    pantalla.blit(titulo_final, (800, 25))

    fondo_term = pygame.Rect(750, 60, 330, 480)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_term)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_term, 3)

    pantalla.blit(fuente_pequena.render("LOTE  ID    OPER    RES", True, COLOR_TEXTO_BLANCO), (760, 65))
    pygame.draw.line(pantalla, COLOR_BORDES, (750, 85), (1080, 85), 3)

    y_term = 90
    for p, lote_num in procesos_terminados:
        if y_term > 520:
            continue
        txt = f"{lote_num:<6}{p.id:<6}{p.operacion:<8}{p.resultado}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (760, y_term))
        y_term += 25

    pantalla.blit(fuente_etiquetas.render("RELOJ GLOBAL:", True, COLOR_TEXTO), (750, 580))
    caja_reloj = pygame.Rect(900, 575, 100, 35)
    pygame.draw.rect(pantalla, COLOR_BORDES, caja_reloj)  # Fondo negro para reloj
    pygame.draw.rect(pantalla, COLOR_TEXTO_BLANCO, caja_reloj, 3)
    pantalla.blit(fuente_etiquetas.render(f"{reloj_global} s", True, COLOR_TEXTO_BLANCO), (920, 582))


# --- BUCLE PRINCIPAL ---
def main():
    global estado, lote_actual, lotes_pendientes, proceso_en_ejecucion, reloj_global, ultimo_tick, lotes_procesados_contador

    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        btn_agregar_rect = None
        btn_ejecutar_rect = None
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

            if estado == "CAPTURA":
                for caja in cajas:
                    caja.manejar_evento(evento)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if btn_agregar_rect and btn_agregar_rect.collidepoint(evento.pos):
                        agregar_proceso()
                    if btn_ejecutar_rect and btn_ejecutar_rect.collidepoint(evento.pos):
                        iniciar_ejecucion()

        # LÓGICA DE SIMULACIÓN
        if estado == "EJECUCION":
            tiempo_actual = pygame.time.get_ticks()

            if proceso_en_ejecucion is None:
                if len(lote_actual) > 0:
                    proceso_en_ejecucion = lote_actual.pop(0)
                elif len(lotes_pendientes) > 0:
                    lote_actual = lotes_pendientes.pop(0)
                    lotes_procesados_contador += 1
                else:
                    estado = "TERMINADO"

            if proceso_en_ejecucion and (tiempo_actual - ultimo_tick >= 1000):
                ultimo_tick = tiempo_actual
                reloj_global += 1
                proceso_en_ejecucion.tiempo_transcurrido += 1
                proceso_en_ejecucion.tiempo_restante -= 1

                if proceso_en_ejecucion.tiempo_restante <= 0:
                    proceso_en_ejecucion.ejecutar()
                    procesos_terminados.append((proceso_en_ejecucion, lotes_procesados_contador))
                    proceso_en_ejecucion = None

        # DIBUJO
        pantalla.fill(COLOR_FONDO)
        btn_agregar_rect, btn_ejecutar_rect = dibujar_columna_captura(pantalla)
        dibujar_columna_ejecucion(pantalla)
        dibujar_columna_terminados(pantalla)

        if estado == "TERMINADO":
            # Efecto de texto parpadeante o de victoria simple
            fondo_fin = pygame.Rect(350, 600, 300, 40)
            pygame.draw.rect(pantalla, COLOR_CAJAS_ACTIVAS, fondo_fin)
            pygame.draw.rect(pantalla, COLOR_BORDES, fondo_fin, 3)
            pantalla.blit(fuente_titulo.render(" FIN DEL JUEGO ", True, COLOR_TEXTO_OSCURO), (400, 605))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()