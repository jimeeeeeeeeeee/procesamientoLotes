import pygame
import sys
from elementos_ui import InputBox
from punto2_logica import generar_procesos_aleatorios
from punto1_captura import dibujar_columna_captura
from punto3_visualizacion import dibujar_columna_ejecucion, dibujar_columna_terminados

# Configuración
pygame.init()
ANCHO, ALTO = 1100, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Multiprogramación por Lotes")

# Colores
COLOR_FONDO = (92, 148, 252)
COLOR_CAJAS_ACTIVAS = (248, 216, 32)
COLOR_BORDES = (0, 0, 0)
COLOR_TEXTO_OSCURO = (0, 0, 0)

fuente_titulo = pygame.font.SysFont("couriernew", 22, bold=True)
fuente_etiquetas = pygame.font.SysFont("couriernew", 16, bold=True)
fuente_pequena = pygame.font.SysFont("couriernew", 14, bold=True)

# Variables globales
estado = "CAPTURA"  # Estados: CAPTURA, EJECUCION, PAUSA, TERMINADO
procesos_capturados = []
lotes_pendientes = []
lote_actual = []
procesos_terminados = []
proceso_en_ejecucion = None

reloj_global = 0
ultimo_tick = 0
mensaje_error = ""
lotes_procesados_contador = 0
id_consecutivo = 1

# Interfaz
caja_cantidad = InputBox(200, 80, 80, 30, solo_numeros=True)


def generar_procesos():
    global mensaje_error, procesos_capturados, id_consecutivo
    cant_str = caja_cantidad.texto.strip()

    if not cant_str:
        mensaje_error = "INGRESA CANTIDAD."
        return

    cant = int(cant_str)
    if cant <= 0:
        mensaje_error = "CANTIDAD > 0."
        return

    nuevos = generar_procesos_aleatorios(cant, id_consecutivo)
    procesos_capturados.extend(nuevos)
    id_consecutivo += cant

    mensaje_error = f"OK: {cant} CREADOS."
    caja_cantidad.texto = ''
    caja_cantidad.txt_surface = fuente_etiquetas.render('', True, caja_cantidad.color_texto)


def iniciar_ejecucion():
    global estado, lotes_pendientes, ultimo_tick, mensaje_error
    if len(procesos_capturados) == 0:
        mensaje_error = "GENERA PRIMERO."
        return

    # LOTES DE 3 EN 3
    for i in range(0, len(procesos_capturados), 3):
        lotes_pendientes.append(procesos_capturados[i:i + 3])

    estado = "EJECUCION"
    ultimo_tick = pygame.time.get_ticks()


def main():
    global estado, lote_actual, lotes_pendientes, proceso_en_ejecucion, reloj_global, ultimo_tick, lotes_procesados_contador

    reloj = pygame.time.Clock()
    corriendo = True

    btn_generar_rect = pygame.Rect(40, 150, 100, 40)
    btn_ejecutar_rect = pygame.Rect(170, 150, 110, 40)

    while corriendo:
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

            if estado == "CAPTURA":
                caja_cantidad.manejar_evento(evento)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if btn_generar_rect.collidepoint(evento.pos):
                        generar_procesos()
                    if btn_ejecutar_rect.collidepoint(evento.pos):
                        iniciar_ejecucion()

            elif estado in ["EJECUCION", "PAUSA"]:
                if evento.type == pygame.KEYDOWN:
                    # Controles de Pausa
                    if evento.key == pygame.K_p and estado == "EJECUCION":
                        estado = "PAUSA"
                    elif evento.key == pygame.K_c and estado == "PAUSA":
                        estado = "EJECUCION"
                        ultimo_tick = pygame.time.get_ticks()

                        # Interrupción y Error
                    if estado == "EJECUCION" and proceso_en_ejecucion:
                        if evento.key == pygame.K_i:
                            lote_actual.append(proceso_en_ejecucion)
                            proceso_en_ejecucion = None
                        elif evento.key == pygame.K_e:
                            proceso_en_ejecucion.resultado = "ERROR"
                            procesos_terminados.append((proceso_en_ejecucion, lotes_procesados_contador))
                            proceso_en_ejecucion = None

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

        dibujar_columna_captura(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, caja_cantidad,
                                procesos_capturados, mensaje_error, ALTO)
        dibujar_columna_ejecucion(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, lote_actual,
                                  lotes_pendientes, proceso_en_ejecucion, ALTO)
        dibujar_columna_terminados(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, procesos_terminados,
                                   reloj_global)

        if estado == "PAUSA":
            fondo_pausa = pygame.Rect(450, 300, 200, 50)
            pygame.draw.rect(pantalla, COLOR_CAJAS_ACTIVAS, fondo_pausa)
            pygame.draw.rect(pantalla, COLOR_BORDES, fondo_pausa, 3)
            pantalla.blit(fuente_titulo.render(" SIM. PAUSADA ", True, COLOR_TEXTO_OSCURO), (455, 315))

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