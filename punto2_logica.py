class Proceso:
    def __init__(self, id_prog, nombre, operacion_eval, tme):
        self.id = id_prog
        self.nombre = nombre
        self.operacion_eval = operacion_eval
        self.operacion = ""
        self.tme = int(tme)
        self.tiempo_transcurrido = 0
        self.tiempo_restante = self.tme
        self.resultado = None

    def ejecutar(self):
        try:
            self.resultado = eval(self.operacion_eval)
        except Exception:
            self.resultado = "Error"