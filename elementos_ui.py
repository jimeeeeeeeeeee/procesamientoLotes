import pygame

# Colores
COLOR_TEXTO_BLANCO = (255, 255, 255)
COLOR_TEXTO_OSCURO = (0, 0, 0)
COLOR_CAJAS = (200, 76, 12)
COLOR_CAJAS_ACTIVAS = (248, 216, 32)
COLOR_BORDES = (0, 0, 0)
COLOR_DROPDOWN_FONDO = (255, 204, 153)

pygame.font.init()
fuente_etiquetas = pygame.font.SysFont("couriernew", 16, bold=True)

class InputBox:
    def __init__(self, x, y, w, h, texto='', solo_numeros=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_CAJAS
        self.color_texto = COLOR_TEXTO_BLANCO
        self.texto = texto
        self.txt_surface = fuente_etiquetas.render(texto, True, self.color_texto)
        self.activo = False
        self.solo_numeros = solo_numeros # Bandera para validar entradas numericas

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.activo = self.rect.collidepoint(evento.pos)
            self.color = COLOR_CAJAS_ACTIVAS if self.activo else COLOR_CAJAS
            self.color_texto = COLOR_TEXTO_OSCURO if self.activo else COLOR_TEXTO_BLANCO
            self.txt_surface = fuente_etiquetas.render(self.texto, True, self.color_texto)
            
        if evento.type == pygame.KEYDOWN and self.activo:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                # Validar que solo se ingresen números y el signo negativo
                caracter = evento.unicode
                if self.solo_numeros:
                    if caracter.isdigit() or (caracter == '-' and len(self.texto) == 0):
                        self.texto += caracter
                else:
                    self.texto += caracter
            self.txt_surface = fuente_etiquetas.render(self.texto, True, self.color_texto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, COLOR_BORDES, self.rect, 3)
        pantalla.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class MenuDesplegable:
    def __init__(self, x, y, w, h, opciones):
        self.rect_principal = pygame.Rect(x, y, w, h)
        self.opciones = opciones
        self.seleccionado = opciones[0]
        self.desplegado = False
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_principal.collidepoint(evento.pos):
                self.desplegado = not self.desplegado
            elif self.desplegado:
                # Revisar si hizo clic en alguna opción desplegada
                for i, opcion in enumerate(self.opciones):
                    rect_opcion = pygame.Rect(self.rect_principal.x, self.rect_principal.y + (i + 1) * self.rect_principal.height, self.rect_principal.width, self.rect_principal.height)
                    if rect_opcion.collidepoint(evento.pos):
                        self.seleccionado = opcion
                        self.desplegado = False
                        break
                else:
                    self.desplegado = False # Cerrar si hace clic afuera

    def dibujar(self, pantalla):
        # Dibujar caja principal
        pygame.draw.rect(pantalla, COLOR_CAJAS_ACTIVAS if self.desplegado else COLOR_CAJAS, self.rect_principal)
        pygame.draw.rect(pantalla, COLOR_BORDES, self.rect_principal, 3)
        
        color_texto = COLOR_TEXTO_OSCURO if self.desplegado else COLOR_TEXTO_BLANCO
        txt_surface = fuente_etiquetas.render(self.seleccionado, True, color_texto)
        pantalla.blit(txt_surface, (self.rect_principal.x + 5, self.rect_principal.y + 5))

        # Dibujar la flechita (indicador visual)
        pygame.draw.polygon(pantalla, COLOR_BORDES, [
            (self.rect_principal.right - 15, self.rect_principal.centery - 2),
            (self.rect_principal.right - 5, self.rect_principal.centery - 2),
            (self.rect_principal.right - 10, self.rect_principal.centery + 4)
        ])

    def dibujar_opciones(self, pantalla):
        """Se dibuja al final para que quede por encima de los demás elementos."""
        if self.desplegado:
            for i, opcion in enumerate(self.opciones):
                rect_opcion = pygame.Rect(self.rect_principal.x, self.rect_principal.y + (i + 1) * self.rect_principal.height, self.rect_principal.width, self.rect_principal.height)
                pygame.draw.rect(pantalla, COLOR_DROPDOWN_FONDO, rect_opcion)
                pygame.draw.rect(pantalla, COLOR_BORDES, rect_opcion, 2)
                
                txt_opcion = fuente_etiquetas.render(opcion, True, COLOR_TEXTO_OSCURO)
                pantalla.blit(txt_opcion, (rect_opcion.x + 5, rect_opcion.y + 5))

# --- LÓGICA DE VALIDACIÓN ---
def validar_operacion(num1_str, operador, num2_str):
    """Retorna (EsValido, MensajeError) validando matemáticamente la operación."""
    if not num1_str or not num2_str:
        return False, "FALTAN NÚMEROS"
    
    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        return False, "NÚMEROS INVÁLIDOS"

    if operador in ['/', 'residuo'] and num2 == 0:
        return False, "ERROR: DIV ENTRE 0"
    
    return True, "OK"