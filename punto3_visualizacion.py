import pygame
# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_CAJAS = (200, 76, 12)
COLOR_BORDES = (0, 0, 0)

def dibujar_columna_ejecucion(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, lote_actual, lotes_pendientes, proceso_en_ejecucion, ALTO):
    titulo_lote = fuente_etiquetas.render("LOTE ACTUAL", True, COLOR_TEXTO)
    pantalla.blit(titulo_lote, (350, 25))

    lbl_restantes = fuente_etiquetas.render(f"LOTES PENDIENTES: {len(lotes_pendientes)}", True, COLOR_TEXTO) # [cite: 26]
    pantalla.blit(lbl_restantes, (500, 25))

    fondo_lote = pygame.Rect(350, 60, 350, 200)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_lote)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_lote, 3)

    # Mostrar ID, TME y T.Restante
    pantalla.blit(fuente_pequena.render("ID      T.MAX      T.RESTANTE", True, COLOR_TEXTO_BLANCO), (360, 65))
    pygame.draw.line(pantalla, COLOR_BORDES, (350, 85), (700, 85), 3)

    y_lote = 90
    for p in lote_actual:
        txt = f"{p.id:<8}{p.tme:<11}{p.tiempo_restante}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (360, y_lote))
        y_lote += 25

    titulo_proceso = fuente_titulo.render("PROCESO EN EJECUCIÓN", True, COLOR_TEXTO)
    pantalla.blit(titulo_proceso, (410, 280))

    labels_proc = ["ID", "Operación", "TME", "T.Transcurrido", "T.Restante"]
    vals_proc = ["", "", "", "", ""]
    if proceso_en_ejecucion:
        vals_proc = [
            str(proceso_en_ejecucion.id),
            proceso_en_ejecucion.operacion,
            str(proceso_en_ejecucion.tme),
            str(proceso_en_ejecucion.tiempo_transcurrido),
            str(proceso_en_ejecucion.tiempo_restante)
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

def dibujar_columna_terminados(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, procesos_terminados, reloj_global):
    titulo_final = fuente_titulo.render("TRABAJOS TERMINADOS", True, COLOR_TEXTO)
    pantalla.blit(titulo_final, (780, 25))
    fondo_term = pygame.Rect(750, 60, 330, 480)
    pygame.draw.rect(pantalla, COLOR_CAJAS, fondo_term)
    pygame.draw.rect(pantalla, COLOR_BORDES, fondo_term, 3)
    pantalla.blit(fuente_pequena.render("LOTE  ID    OPER         RES", True, COLOR_TEXTO_BLANCO), (760, 65))
    pygame.draw.line(pantalla, COLOR_BORDES, (750, 85), (1080, 85), 3)

    y_term = 90
    for p, lote_num in procesos_terminados:
        if y_term > 520:
            continue
        # ERROR si fue terminado con  E
        txt = f"{lote_num:<6}{p.id:<6}{p.operacion:<13}{p.resultado}"
        pantalla.blit(fuente_pequena.render(txt, True, COLOR_TEXTO_BLANCO), (760, y_term))
        y_term += 25

    pantalla.blit(fuente_etiquetas.render("RELOJ GLOBAL:", True, COLOR_TEXTO), (750, 580))
    caja_reloj = pygame.Rect(910, 575, 90, 35)
    pygame.draw.rect(pantalla, COLOR_BORDES, caja_reloj)
    pygame.draw.rect(pantalla, COLOR_TEXTO_BLANCO, caja_reloj, 3)
    pantalla.blit(fuente_etiquetas.render(f"{reloj_global} s", True, COLOR_TEXTO_BLANCO), (930, 582))