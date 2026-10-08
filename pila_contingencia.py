# ==============================================================================
# EDUARD LEANDRO VASQUEZ HIDALGO
# Código: 106202622568
# Universidad de Manizales
# ==============================================================================

from collections import deque

class PilaContingencia:
    """Pila (LIFO) para el plan de contingencia de extracciones urgentes."""
    
    def __init__(self):
        self._elementos = deque()

    def push(self, cliente):
        self._elementos.append(cliente)

    def pop(self):
        if not self.es_vacia():
            return self._elementos.pop()
        return None

    def peek(self):
        if not self.es_vacia():
            return self._elementos[-1]
        return None

    def es_vacia(self):
        return len(self._elementos) == 0

    def construir_pila_desde_lista(self, lista_clientes):
        self._elementos.clear()
        
        # Filtrado: extracciones + urgentes + pendientes
        filtrados = [
            c for c in lista_clientes 
            if c.tipo_atencion == "extraccion"
            and c.prioridad == "Urgente"
            and c.estado == "Pendiente"
        ]
        
        # Ordenamos de fecha más lejana a más cercana para que la más próxima
        # quede en el tope de la Pila al hacer push
        for i in range(len(filtrados)):
            for j in range(len(filtrados) - 1 - i):
                if filtrados[j].fecha_dt < filtrados[j + 1].fecha_dt:
                    filtrados[j], filtrados[j + 1] = filtrados[j + 1], filtrados[j]

        for c in filtrados:
            self.push(c)

    def generar_informe(self):
        if self.es_vacia():
            print("\nNo hay clientes urgentes pendientes para extracción dental.")
            return

        print("\n=========================================================================================")
        print("          INFORME DE PILA DE CONTINGENCIA - LLAMADAS PRIORITARIAS (EXTRACCIONES URGENTES)")
        print("=========================================================================================")
        # Mostramos en orden de salida LIFO (del tope hacia abajo)
        temp_lista = list(reversed(self._elementos))
        for idx, cliente in enumerate(temp_lista, 1):
            print(f"Llamada #{idx} -> {cliente}")
        print("=========================================================================================")