import random

class Proceso:
    def __init__(self, id_prog, operacion_eval, operacion_visual, tme):
        self.id = id_prog
        self.operacion_eval = operacion_eval
        self.operacion = operacion_visual
        self.tme = int(tme)
        self.tiempo_transcurrido = 0
        self.tiempo_restante = self.tme
        self.resultado = None

        #5 estados
        self.tiempo_bloqueado = 0
        self.t_llegada = 0
        self.t_finalizacion = 0
        self.t_respuesta = -1
        self.t_servicio = 0
        self.t_retorno = 0
        self.t_espera = 0

    def ejecutar(self):
        try:
            self.resultado = eval(self.operacion_eval)
        except Exception:
            self.resultado = "Error"

    def calcular_tiempos(self):
        self.t_retorno = self.t_finalizacion - self.t_llegada
        self.t_espera = self.t_retorno - self.t_servicio


def generar_procesos_aleatorios(cantidad, id_inicial=1):
    procesos = []
    operadores = ['+', '-', '*', '/', '%']

    for i in range(cantidad):
        id_prog = str(id_inicial + i)
        tme = random.randint(7, 18)
        op = random.choice(operadores)
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        # Validación
        if op in ['/', '%'] and num2 == 0:
            num2 = 1
        operacion_visual = f"{num1} {op} {num2}"
        operacion_eval = operacion_visual
        p = Proceso(id_prog, operacion_eval, operacion_visual, tme)
        procesos.append(p)

    return procesos