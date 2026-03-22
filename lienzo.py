import pygame
import sys
from elementos_ui import InputBox
from punto2_logica import generar_procesos_aleatorios
from punto1_captura import dibujar_columna_captura
from punto3_visualizacion import dibujar_columna_ejecucion, dibujar_columna_terminados, dibujar_tabla_bcp

pygame.init()
ANCHO, ALTO = 1100, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación FCFS - Práctica 5")

COLOR_FONDO = (92, 148, 252)
COLOR_CAJAS_ACTIVAS = (248, 216, 32)
COLOR_BORDES = (0, 0, 0)
COLOR_TEXTO_OSCURO = (0, 0, 0)

fuente_titulo = pygame.font.SysFont("couriernew", 22, bold=True)
fuente_etiquetas = pygame.font.SysFont("couriernew", 16, bold=True)
fuente_pequena = pygame.font.SysFont("couriernew", 14, bold=True)

estado = "CAPTURA"
procesos_capturados = []
procesos_totales = []
cola_nuevos = []
cola_listos = []
cola_bloqueados = []
procesos_terminados = []
proceso_en_ejecucion = None

reloj_global = 0
ultimo_tick = 0
mensaje_error = ""
id_consecutivo = 1

caja_cantidad = InputBox(200, 80, 80, 30, solo_numeros=True)

def generar_procesos():
    global mensaje_error, procesos_capturados, procesos_totales, id_consecutivo
    cant_str = caja_cantidad.texto.strip()
    if not cant_str:
        return
    cant = int(cant_str)
    if cant <= 0:
        return

    nuevos = generar_procesos_aleatorios(cant, id_consecutivo)
    procesos_capturados.extend(nuevos)
    procesos_totales.extend(nuevos)
    id_consecutivo += cant
    mensaje_error = f"OK: {cant} CREADOS."
    caja_cantidad.texto = ''
    caja_cantidad.txt_surface = fuente_etiquetas.render('', True, caja_cantidad.color_texto)

def iniciar_ejecucion():
    global estado, cola_nuevos, ultimo_tick, mensaje_error
    if len(procesos_capturados) == 0:
        mensaje_error = "GENERA PRIMERO."
        return
    cola_nuevos = procesos_capturados.copy()
    estado = "EJECUCION"
    ultimo_tick = pygame.time.get_ticks()

def main():
    global estado, proceso_en_ejecucion, reloj_global, ultimo_tick, id_consecutivo

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
                    if btn_generar_rect.collidepoint(evento.pos): generar_procesos()
                    if btn_ejecutar_rect.collidepoint(evento.pos): iniciar_ejecucion()

            elif estado in ["EJECUCION", "PAUSA", "TABLA_BCP"]:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p and estado == "EJECUCION":
                        estado = "PAUSA"
                    elif evento.key == pygame.K_b and estado == "EJECUCION":
                        estado = "TABLA_BCP"
                    elif evento.key == pygame.K_c and estado in ["PAUSA", "TABLA_BCP"]:
                        estado = "EJECUCION"
                        ultimo_tick = pygame.time.get_ticks()

                    elif evento.key == pygame.K_n and estado in ["EJECUCION", "PAUSA"]:
                        nuevo = generar_procesos_aleatorios(1, id_consecutivo)[0]
                        procesos_totales.append(nuevo)
                        cola_nuevos.append(nuevo)
                        id_consecutivo += 1

                    if estado == "EJECUCION" and proceso_en_ejecucion:
                        if evento.key == pygame.K_e: # Interrupción
                            proceso_en_ejecucion.tiempo_bloqueado = 0
                            proceso_en_ejecucion.estado = "Bloqueado"
                            cola_bloqueados.append(proceso_en_ejecucion)
                            proceso_en_ejecucion = None
                        elif evento.key == pygame.K_w: # Error
                            proceso_en_ejecucion.resultado = "ERROR"
                            proceso_en_ejecucion.estado = "Terminado"
                            proceso_en_ejecucion.t_finalizacion = reloj_global
                            proceso_en_ejecucion.t_servicio = proceso_en_ejecucion.tiempo_transcurrido
                            procesos_terminados.append(proceso_en_ejecucion)
                            proceso_en_ejecucion = None

        if estado == "EJECUCION":
            tiempo_actual = pygame.time.get_ticks()

            en_memoria = len(cola_listos) + len(cola_bloqueados) + (1 if proceso_en_ejecucion else 0)
            while en_memoria < 3 and len(cola_nuevos) > 0:
                p_nuevo = cola_nuevos.pop(0)
                p_nuevo.estado = "Listo"
                p_nuevo.t_llegada = reloj_global
                cola_listos.append(p_nuevo)
                en_memoria += 1

            if tiempo_actual - ultimo_tick >= 1000:
                ultimo_tick = tiempo_actual
                reloj_global += 1

                procesos_a_desbloquear = 0
                for p in cola_bloqueados:
                    p.tiempo_bloqueado += 1
                    if p.tiempo_bloqueado >= 9:
                        procesos_a_desbloquear += 1

                for _ in range(procesos_a_desbloquear):
                    p_listo = cola_bloqueados.pop(0)
                    p_listo.tiempo_bloqueado = 0
                    p_listo.estado = "Listo"
                    cola_listos.append(p_listo)

                if proceso_en_ejecucion is None and len(cola_listos) > 0:
                    proceso_en_ejecucion = cola_listos.pop(0)
                    proceso_en_ejecucion.estado = "Ejecucion"
                    if proceso_en_ejecucion.t_respuesta is None:
                        proceso_en_ejecucion.t_respuesta = reloj_global - proceso_en_ejecucion.t_llegada

                if proceso_en_ejecucion:
                    proceso_en_ejecucion.tiempo_transcurrido += 1
                    proceso_en_ejecucion.tiempo_restante -= 1

                    if proceso_en_ejecucion.tiempo_restante <= 0:
                        proceso_en_ejecucion.ejecutar()
                        proceso_en_ejecucion.estado = "Terminado"
                        proceso_en_ejecucion.t_finalizacion = reloj_global
                        proceso_en_ejecucion.t_servicio = proceso_en_ejecucion.tiempo_transcurrido
                        procesos_terminados.append(proceso_en_ejecucion)
                        proceso_en_ejecucion = None

                if len(cola_nuevos) == 0 and len(cola_listos) == 0 and not proceso_en_ejecucion and len(cola_bloqueados) == 0:
                    estado = "REPORTE"

        pantalla.fill(COLOR_FONDO)

        if estado == "REPORTE" or estado == "TABLA_BCP":
            dibujar_tabla_bcp(pantalla, fuente_titulo, fuente_pequena, procesos_totales, reloj_global)
            if estado == "TABLA_BCP":
                pantalla.blit(fuente_titulo.render(" SIMULACION PAUSADA - PRESIONA 'C' PARA CONTINUAR ", True, COLOR_TEXTO_OSCURO), (100, 620))
        else:
            dibujar_columna_captura(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, caja_cantidad, procesos_capturados, mensaje_error, ALTO)
            dibujar_columna_ejecucion(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, cola_listos, cola_nuevos, cola_bloqueados, proceso_en_ejecucion, ALTO)
            dibujar_columna_terminados(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, procesos_terminados, reloj_global)

            if estado == "PAUSA":
                fondo_pausa = pygame.Rect(450, 300, 200, 50)
                pygame.draw.rect(pantalla, COLOR_CAJAS_ACTIVAS, fondo_pausa)
                pygame.draw.rect(pantalla, COLOR_BORDES, fondo_pausa, 3)
                pantalla.blit(fuente_titulo.render(" SIM. PAUSADA ", True, COLOR_TEXTO_OSCURO), (455, 315))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()