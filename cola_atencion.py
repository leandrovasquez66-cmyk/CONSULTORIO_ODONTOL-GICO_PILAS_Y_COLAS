# ==============================================================================
# EDUARD LEANDRO VASQUEZ HIDALGO
# Código: 106202622568
# Universidad de Manizales
# ==============================================================================

from collections import deque

class ColaAtencion:
    """Manejo de la Agenda Diaria mediante una Cola (FIFO)."""
    
    def __init__(self):
        # deque nos da enqueue (append) y dequeue (popleft) en O(1)
        self._cola = deque()

    def enqueue(self, cliente):
        self._cola.append(cliente)

    def dequeue(self):
        if not self.es_vacia():
            return self._cola.popleft()
        return None

    def remove(self, cliente):
        # Permite sacar de la cola a alguien atendido por urgencias
        try:
            self._cola.remove(cliente)
            return True
        except ValueError:
            return False

    def peek(self):
        if not self.es_vacia():
            return self._cola[0]
        return None

    def es_vacia(self):
        return len(self._cola) == 0

    def mostrar_agenda(self):
        if self.es_vacia():
            print("\nNo hay clientes esperando en la cola de la agenda diaria.")
            return

        print("\n=========================================================================================")
        print("                         AGENDA DIARIA - COLA DE ATENCIÓN (FIFO)")
        print("=========================================================================================")
        for idx, cliente in enumerate(self._cola, 1):
            print(f"Turno #{idx}: {cliente}")
        print("=========================================================================================")