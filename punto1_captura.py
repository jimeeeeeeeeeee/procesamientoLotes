import pygame

# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_BORDES = (0, 0, 0)
COLOR_BOTON = (0, 168, 0)
COLOR_ERROR = (228, 0, 88)

def dibujar_columna_captura(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, caja_cantidad, procesos_capturados, mensaje_error, ALTO):
    titulo = fuente_titulo.render("DATOS INICIALES", True, COLOR_TEXTO)
    pantalla.blit(titulo, (60, 20))

    pantalla.blit(fuente_etiquetas.render("Número de Procesos:", True, COLOR_TEXTO_BLANCO), (15, 85))
    caja_cantidad.dibujar(pantalla)

    btn_generar = pygame.Rect(40, 150, 100, 40)
    pygame.draw.rect(pantalla, COLOR_BOTON, btn_generar)
    pygame.draw.rect(pantalla, COLOR_BORDES, btn_generar, 3)
    pantalla.blit(fuente_etiquetas.render("GENERAR", True, COLOR_TEXTO_BLANCO), (55, 160))

    btn_ejecutar = pygame.Rect(170, 150, 110, 40)
    pygame.draw.rect(pantalla, COLOR_BOTON, btn_ejecutar)
    pygame.draw.rect(pantalla, COLOR_BORDES, btn_ejecutar, 3)
    pantalla.blit(fuente_etiquetas.render("EJECUTAR", True, COLOR_TEXTO_BLANCO), (180, 160))

    lbl_contador = fuente_etiquetas.render(f"GENERADOS: {len(procesos_capturados)}", True, COLOR_TEXTO_BLANCO)
    pantalla.blit(lbl_contador, (100, 220))
    if mensaje_error:
        lbl_err = fuente_pequena.render(mensaje_error, True, COLOR_ERROR)
        pantalla.blit(lbl_err, (20, 250))

    y_inst = 350
    pantalla.blit(fuente_etiquetas.render("CONTROLES DE TECLADO:", True, COLOR_TEXTO_BLANCO), (15, y_inst))
    pantalla.blit(fuente_pequena.render("[E] Interrupción por E/S", True, COLOR_TEXTO_BLANCO), (15, y_inst + 25))
    pantalla.blit(fuente_pequena.render("[W] Error", True, COLOR_TEXTO_BLANCO), (15, y_inst + 50))
    pantalla.blit(fuente_pequena.render("[P] Pausa", True, COLOR_TEXTO_BLANCO), (15, y_inst + 75))
    pantalla.blit(fuente_pequena.render("[C] Continuar", True, COLOR_TEXTO_BLANCO), (15, y_inst + 100))
    pantalla.blit(fuente_pequena.render("[N] Nuevo Proceso", True, COLOR_TEXTO_BLANCO), (15, y_inst + 125))
    pantalla.blit(fuente_pequena.render("[B] Tabla BCP", True, COLOR_TEXTO_BLANCO), (15, y_inst + 150))

    pygame.draw.line(pantalla, COLOR_BORDES, (330, 0), (330, ALTO), 4)