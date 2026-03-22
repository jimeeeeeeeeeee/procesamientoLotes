import pygame
# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_CAJAS = (200, 76, 12)
COLOR_BORDES = (0, 0, 0)


def dibujar_columna_ejecucion(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, cola_listos, cola_nuevos,
                              cola_bloqueados, proceso_en_ejecucion, ALTO):
    titulo_listos = fuente_etiquetas.render("COLA DE LISTOS", True, COLOR_TEXTO)
    pantalla.blit(titulo_listos, (350, 25))

    lbl_nuevos = fuente_etiquetas.render(f"NUEVOS: {len(cola_nuevos)}", True, COLOR_TEXTO)
    pantalla.blit(lbl_nuevos, (500, 25))

    fondo_listos = pygame.Rect(350, 50, 350, 150)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_listos)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_listos, 3)

    pantalla.blit(fuente_pequena.render("ID      TME        T.RESTANTE", True, COLOR_TEXTO_BLANCO), (360, 55))
    pygame.draw.line(pantalla, COLOR_BORDES, (350, 75), (700, 75), 3)

    y_lote = 80
    for p in cola_listos:
        if y_lote > 180: break
        txt = f"{p.id:<8}{p.tme:<11}{p.tiempo_restante}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (360, y_lote))
        y_lote += 20

    titulo_proceso = fuente_titulo.render("PROCESO EN EJECUCIÓN", True, COLOR_TEXTO)
    pantalla.blit(titulo_proceso, (410, 210))

    labels_proc = ["ID", "Operación", "TME", "T.Ejecutado", "T.Restante"]
    vals_proc = ["", "", "", "", ""]
    if proceso_en_ejecucion:
        vals_proc = [
            str(proceso_en_ejecucion.id),
            proceso_en_ejecucion.operacion,
            str(proceso_en_ejecucion.tme),
            str(proceso_en_ejecucion.tiempo_transcurrido),
            str(proceso_en_ejecucion.tiempo_restante)
        ]

    y_pos = 240
    for i, etiqueta in enumerate(labels_proc):
        pantalla.blit(fuente_etiquetas.render(etiqueta, True, COLOR_TEXTO_BLANCO), (350, y_pos + 5))
        caja_info = pygame.Rect(520, y_pos, 180, 25)
        pygame.draw.rect(pantalla, COLOR_CAJAS, caja_info)
        pygame.draw.rect(pantalla, COLOR_BORDES, caja_info, 2)
        pantalla.blit(fuente_etiquetas.render(vals_proc[i], True, COLOR_TEXTO_BLANCO), (525, y_pos + 5))
        y_pos += 35

    # Dibujar Bloqueados
    pantalla.blit(fuente_etiquetas.render(f"BLOQUEADOS ({len(cola_bloqueados)})", True, COLOR_TEXTO), (350, y_pos + 10))
    fondo_bloq = pygame.Rect(350, y_pos + 35, 350, 110)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_bloq)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_bloq, 3)
    pantalla.blit(fuente_pequena.render("ID      TIEMPO EN BLOQUEO", True, COLOR_TEXTO_BLANCO), (360, y_pos + 40))

    y_bloq = y_pos + 60
    for p in cola_bloqueados:
        if y_bloq > y_pos + 120: break
        pantalla.blit(fuente_pequena.render(f"{p.id:<8}{p.tiempo_bloqueado} / 10s", True, COLOR_TEXTO_BLANCO),
                      (360, y_bloq))
        y_bloq += 20

    pygame.draw.line(pantalla, COLOR_BORDES, (730, 0), (730, ALTO), 4)


def dibujar_columna_terminados(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, procesos_terminados,
                               reloj_global):
    titulo_final = fuente_titulo.render("PROCESOS TERMINADOS", True, COLOR_TEXTO)
    pantalla.blit(titulo_final, (780, 25))
    fondo_term = pygame.Rect(750, 60, 330, 480)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_term)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_term, 3)
    pantalla.blit(fuente_pequena.render("ID    OPER         RES", True, COLOR_TEXTO_BLANCO), (760, 65))  # Lote borrado
    pygame.draw.line(pantalla, COLOR_BORDES, (750, 85), (1080, 85), 3)

    y_term = 90
    for p in procesos_terminados:
        if y_term > 520:
            continue
        txt = f"{p.id:<6}{p.operacion:<13}{p.resultado}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (760, y_term))
        y_term += 25

    pantalla.blit(fuente_etiquetas.render("RELOJ GLOBAL:", True, COLOR_TEXTO), (750, 580))
    pantalla.blit(fuente_etiquetas.render(f"{reloj_global} s", True, COLOR_TEXTO_BLANCO), (930, 580))

def dibujar_reporte_final(pantalla, fuente_titulo, fuente_pequena, procesos_terminados):
    pantalla.blit(fuente_titulo.render("REPORTE FINAL DE TIEMPOS", True, COLOR_TEXTO), (50, 20))
    encabezado = "ID  | OPERACIÓN  | RESULTADO | TME | LLEGADA | FIN | RETORNO | RESPUESTA | ESPERA | SERVICIO"
    pantalla.blit(fuente_pequena.render(encabezado, True, (255, 255, 0)), (50, 60))

    y = 90
    for p in procesos_terminados:
        p.calcular_tiempos()
        res = p.resultado if str(p.resultado) == "ERROR" else f"{p.resultado}"
        fila = f"{p.id:<3} | {p.operacion:<10} | {res:<9} | {p.tme:<3} | {p.t_llegada:<7} | {p.t_finalizacion:<3} | {p.t_retorno:<7} | {p.t_respuesta:<9} | {p.t_espera:<6} | {p.t_servicio:<8}"
        pantalla.blit(fuente_pequena.render(fila, True, COLOR_TEXTO), (50, y))
        y += 20