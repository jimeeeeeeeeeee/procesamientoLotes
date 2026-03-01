import pygame

# Colores
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_BORDES = (0, 0, 0)
COLOR_BOTON = (0, 168, 0)
COLOR_ERROR = (228, 0, 88)

def dibujar_columna_captura(pantalla, fuente_titulo, fuente_etiquetas, fuente_pequena, cajas, menu_operador, procesos_capturados, mensaje_error, ALTO):
    titulo = fuente_titulo.render("CAPTURAR PROCESOS", True, COLOR_TEXTO)
    pantalla.blit(titulo, (60, 20))

    pantalla.blit(fuente_etiquetas.render("Nombre", True, COLOR_TEXTO_BLANCO), (15, 85))
    cajas[0].dibujar(pantalla) # caja_nombre

    pantalla.blit(fuente_etiquetas.render("Operación", True, COLOR_TEXTO_BLANCO), (15, 145))
    cajas[1].dibujar(pantalla) # caja_num1
    menu_operador.dibujar(pantalla)
    cajas[2].dibujar(pantalla) # caja_num2

    pantalla.blit(fuente_etiquetas.render("Tiempo(TME)", True, COLOR_TEXTO_BLANCO), (15, 205))
    cajas[3].dibujar(pantalla) # caja_tme

    pantalla.blit(fuente_etiquetas.render("ID", True, COLOR_TEXTO_BLANCO), (15, 265))
    cajas[4].dibujar(pantalla) # caja_id

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
    menu_operador.dibujar_opciones(pantalla)