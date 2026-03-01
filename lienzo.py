import pygame
import sys
from elementos_ui import InputBox, MenuDesplegable, validar_operacion
from punto2_logica import Proceso
from punto1_captura import dibujar_columna_captura
from punto3_visualizacion import dibujar_columna_ejecucion, dibujar_columna_terminados

#Configuración
pygame.init()
ANCHO, ALTO = 1100, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Procesos por Lotes")

# Colores
COLOR_FONDO = (92, 148, 252)
COLOR_CAJAS_ACTIVAS = (248, 216, 32)
COLOR_BORDES = (0, 0, 0)
COLOR_TEXTO_OSCURO = (0, 0, 0)

fuente_titulo = pygame.font.SysFont("couriernew", 22, bold=True)
fuente_etiquetas = pygame.font.SysFont("couriernew", 16, bold=True)
fuente_pequena = pygame.font.SysFont("couriernew", 14, bold=True)

# Variables globales
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

# Interfaz
caja_nombre = InputBox(120, 80, 180, 30)
caja_num1 = InputBox(120, 140, 50, 30, solo_numeros=True)
menu_operador = MenuDesplegable(175, 140, 75, 30, ['+', '-', '*', '/', '%', 'pow'])
caja_num2 = InputBox(255, 140, 50, 30, solo_numeros=True)
caja_tme = InputBox(120, 200, 180, 30, solo_numeros=True)
caja_id = InputBox(120, 260, 180, 30, solo_numeros=True)

cajas = [caja_nombre, caja_num1, caja_num2, caja_tme, caja_id]


# Logica del simulador
def limpiar_cajas():
    for caja in cajas:
        caja.texto = ''
        caja.txt_surface = fuente_etiquetas.render('', True, caja.color_texto)


def agregar_proceso():
    global mensaje_error
    nom = caja_nombre.texto.strip()
    num1 = caja_num1.texto.strip()
    num2 = caja_num2.texto.strip()
    op = menu_operador.seleccionado
    tme = caja_tme.texto.strip()
    id_p = caja_id.texto.strip()

    es_valida, msj_val = validar_operacion(num1, op, num2)
    if not es_valida:
        mensaje_error = msj_val
        return

    if not nom or not tme or not id_p:
        mensaje_error = "LLENA TODO."
        return
    if int(tme) <= 0:
        mensaje_error = "TME > 0."
        return
    if any(p.id == id_p for p in procesos_capturados):
        mensaje_error = "YA EXISTE EL ID."
        return

    op_matematica = op
    if op == '%':
        op_matematica = '%'
    elif op == 'pow':
        op_matematica = '**'

    operacion_eval = f"{num1}{op_matematica}{num2}"
    operacion_visual = f"{num1} {op} {num2}"

    nuevo_proceso = Proceso(id_p, nom, operacion_eval, tme)
    nuevo_proceso.operacion = operacion_visual

    procesos_capturados.append(nuevo_proceso)
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


# Principal (bucle)
def main():
    global estado, lote_actual, lotes_pendientes, proceso_en_ejecucion, reloj_global, ultimo_tick, lotes_procesados_contador

    reloj = pygame.time.Clock()
    corriendo = True

    btn_agregar_rect = pygame.Rect(40, 350, 100, 40)
    btn_ejecutar_rect = pygame.Rect(170, 350, 110, 40)

    while corriendo:
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

            if estado == "CAPTURA":
                for caja in cajas:
                    caja.manejar_evento(evento)
                menu_operador.manejar_evento(evento)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if btn_agregar_rect.collidepoint(evento.pos):
                        agregar_proceso()
                    if btn_ejecutar_rect.collidepoint(evento.pos):
                        iniciar_ejecucion()

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

        pantalla.fill(COLOR_FONDO)
        # Llamadas a los MÓDULOS externos para dibujar
        dibujar_columna_captura(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, cajas, menu_operador,
                                procesos_capturados, mensaje_error, ALTO)
        dibujar_columna_ejecucion(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, lote_actual,
                                  lotes_pendientes, proceso_en_ejecucion, ALTO)
        dibujar_columna_terminados(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, procesos_terminados,
                                   reloj_global)

        if estado == "TERMINADO":
            fondo_fin = pygame.Rect(350, 600, 300, 40)
            pygame.draw.rect(pantalla, COLOR_CAJAS_ACTIVAS, fondo_fin)
            pygame.draw.rect(pantalla, COLOR_BORDES, fondo_fin, 3)
            pantalla.blit(fuente_titulo.render(" FIN DE SIMULACIÓN ", True, COLOR_TEXTO_OSCURO), (400, 605))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()