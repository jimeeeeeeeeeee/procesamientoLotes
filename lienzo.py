import pygame
import sys

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Procesos por Lotes")
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (220, 220, 220)
GRIS_OSCURO = (150, 150, 150)
AZUL_CLARO = (173, 216, 230)

# 4. Fuentes de texto
fuente_titulo = pygame.font.SysFont("arial", 18, bold=True)
fuente_texto = pygame.font.SysFont("arial", 14)


def dibujar_interfaz():
    pantalla.fill(BLANCO)

    # --- BARRA SUPERIOR ---
    # Etiqueta y caja simulada para "# Procesos"
    texto_procesos = fuente_texto.render("# Procesos:", True, NEGRO)
    pantalla.blit(texto_procesos, (20, 25))
    pygame.draw.rect(pantalla, GRIS_CLARO, (100, 20, 60, 30))  # Caja de texto simulada
    pygame.draw.rect(pantalla, NEGRO, (100, 20, 60, 30), 1)  # Borde

    # Botón "Generar"
    pygame.draw.rect(pantalla, GRIS_CLARO, (180, 20, 80, 30))
    pygame.draw.rect(pantalla, NEGRO, (180, 20, 80, 30), 1)
    texto_btn_generar = fuente_texto.render("Generar", True, NEGRO)
    pantalla.blit(texto_btn_generar, (195, 25))

    # Reloj Global
    # Requerimiento: desplegar un reloj global desde el inicio hasta el fin
    texto_reloj = fuente_texto.render("Reloj global:  00:00:00", True, NEGRO)
    pantalla.blit(texto_reloj, (700, 25))

    # --- SECCIÓN IZQUIERDA: Lote en Ejecución ---
    titulo_espera = fuente_titulo.render("Lote en Ejecución", True, NEGRO)
    pantalla.blit(titulo_espera, (80, 80))
    pygame.draw.rect(pantalla, AZUL_CLARO, (30, 110, 250, 380))  # Contenedor
    pygame.draw.rect(pantalla, NEGRO, (30, 110, 250, 380), 2)  # Borde

    # Lotes Pendientes
    texto_lotes_pendientes = fuente_texto.render("# Lotes pendientes: 0", True, NEGRO)
    pantalla.blit(texto_lotes_pendientes, (30, 510))

    # SECCIÓN CENTRAL: Proceso en Ejecución ---
    titulo_ejecucion = fuente_titulo.render("Proceso en Ejecución", True, NEGRO)
    pantalla.blit(titulo_ejecucion, (340, 180))
    pygame.draw.rect(pantalla, AZUL_CLARO, (310, 210, 260, 250))  # Contenedor
    pygame.draw.rect(pantalla, NEGRO, (310, 210, 260, 250), 2)  # Borde

    # --- SECCIÓN DERECHA: Procesos Terminados ---
    titulo_terminados = fuente_titulo.render("Procesos Terminados", True, NEGRO)
    pantalla.blit(titulo_terminados, (650, 80))
    pygame.draw.rect(pantalla, AZUL_CLARO, (600, 110, 270, 380))  # Contenedor
    pygame.draw.rect(pantalla, NEGRO, (600, 110, 270, 380), 2)  # Borde


def main():
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        dibujar_interfaz()
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()