# ==============================================================================
# EDUARD LEANDRO VASQUEZ HIDALGO
# Código: 106202622568
# Universidad de Manizales
# ==============================================================================

import calendar
import datetime
from cliente import Cliente
from pila_contingencia import PilaContingencia
from cola_atencion import ColaAtencion

class ConsultorioOdontologico:
    """Controlador principal que vincula la Pila, la Cola y el registro."""
    
    def __init__(self):
        self.lista_general = []
        self.pila_contingencia = PilaContingencia()
        self.cola_atencion = ColaAtencion()

    def registrar_cliente(self):
        print("\n--- REGISTRO DE CLIENTE PARA AGENDA ---")
        
        # Validar cédula única en estado Pendiente
        while True:
            cedula = input("Cédula: ").strip()
            if cedula.isdigit() and 7 <= len(cedula) <= 10:
                ya_existe = any(
                    cliente.cedula == cedula and cliente.estado == "Pendiente"
                    for cliente in self.lista_general
                )
                if ya_existe:
                    print("Error: Este paciente ya tiene un turno pendiente en la agenda.")
                    return
                break
            print("Opción inválida. La cédula debe ser numérica y contener entre 7 y 10 dígitos.")

        # Validar nombre (solo letras/espacios)
        while True:
            nombre = input("Nombre completo: ").strip()
            if len(nombre) >= 3 and all(c.isalpha() or c.isspace() for c in nombre):
                break
            print("Opción inválida. El nombre debe tener al menos 3 caracteres y contener únicamente letras.")

        # Validar teléfono
        while True:
            telefono = input("Teléfono: ").strip()
            if telefono.isdigit() and len(telefono) == 10:
                break
            print("Opción inválida. El teléfono debe contener exactamente 10 dígitos numéricos.")

        # Selección de tipo de atención
        mapa_atencion = {"1": "limpieza", "2": "calzas", "3": "extraccion", "4": "diagnostico"}
        while True:
            print("\nTipo de Atención: 1. Limpieza | 2. Calzas | 3. Extracción | 4. Diagnóstico")
            opcion_atencion = input("Seleccione una opción (1-4): ").strip()
            if opcion_atencion in mapa_atencion:
                tipo_atencion = mapa_atencion[opcion_atencion]
                break
            print("Opción inválida. Seleccione un número de 1 a 4.")

        # Selección de prioridad
        while True:
            print("\nPrioridad: 1. Normal | 2. Urgente")
            opcion_prioridad = input("Seleccione opción (1-2): ").strip()
            if opcion_prioridad in ["1", "2"]:
                prioridad = "Urgente" if opcion_prioridad == "2" else "Normal"
                break
            print("Opción inválida. Seleccione un número de 1 a 2.")

        # Registro guiado de Fecha de la Cita con validación
        fecha_hoy = datetime.date.today()
        print(f"\n--- FECHA DE LA CITA (Hoy es {fecha_hoy.strftime('%d/%m/%Y')}) ---")
        
        # 1. Validar Año (Año actual o siguiente)
        while True:
            anio_in = input(f"Año [{fecha_hoy.year} - {fecha_hoy.year + 1}]: ").strip()
            if anio_in.isdigit() and fecha_hoy.year <= int(anio_in) <= fecha_hoy.year + 1:
                anio = int(anio_in)
                break
            print(f"Opción inválida. Ingrese un año válido ({fecha_hoy.year} o {fecha_hoy.year + 1}).")

        # 2. Determinar mes mínimo permitido según el año elegido
        mes_minimo = fecha_hoy.month if anio == fecha_hoy.year else 1
        
        while True:
            mes_in = input(f"Mes ({mes_minimo}-12): ").strip()
            if mes_in.isdigit() and mes_minimo <= int(mes_in) <= 12:
                mes = int(mes_in)
                break
            print(f"Opción inválida. Para el año {anio}, el mes debe estar entre {mes_minimo} y 12.")

        # 3. Calcular el límite total de días para ese mes y año 
        _, max_dias = calendar.monthrange(anio, mes)

        # 4. Determinar día mínimo permitido si es el mismo año y mes actual
        dia_minimo = fecha_hoy.day if (anio == fecha_hoy.year and mes == fecha_hoy.month) else 1

        while True:
            dia_in = input(f"Día ({dia_minimo}-{max_dias}): ").strip()
            if dia_in.isdigit():
                dia = int(dia_in)
                if dia_minimo <= dia <= max_dias:
                    fecha_dt = datetime.date(anio, mes, dia)
                    fecha_str = fecha_dt.strftime("%d/%m/%Y")
                    break
                else:
                    print(f"Opción inválida. Para esta fecha, el día debe estar entre {dia_minimo} y {max_dias}.")
            else:
                print("Opción inválida. Ingrese únicamente números para el día.")

        nuevo_cliente = Cliente(cedula, nombre, telefono, tipo_atencion, prioridad, fecha_str)
        self.lista_general.append(nuevo_cliente)
        self.cola_atencion.enqueue(nuevo_cliente)
        
        print(f"\n¡Cliente {nombre} registrado en la agenda diaria con éxito!")

    def atender_siguiente_contingencia(self):
        # Reconstruimos la pila para que refleje el estado actual de los clientes
        self.pila_contingencia.construir_pila_desde_lista(self.lista_general)
        siguiente = self.pila_contingencia.peek()
        if siguiente:
            print(f"\n[Siguiente en contingencia - Peek]: {siguiente.nombre} (Cédula: {siguiente.cedula}) | Fecha: {siguiente.fecha_str}")
            confirmar = input("¿Atender cliente urgente ahora? (s/n): ").strip().lower()
            if confirmar == 's':
                atendido = self.pila_contingencia.pop()
                if atendido:
                    atendido.estado = "Atendido"
                    # Al atenderlo por contingencia lo removemos también de la cola diaria
                    self.cola_atencion.remove(atendido)
                    print(f"\n---> Se atendió al cliente urgente: {atendido.nombre} exitosamente.")
        else:
            print("\nNo hay clientes urgentes pendientes en la pila de contingencia.")

    def procesar_pila_contingencia(self):
        self.pila_contingencia.construir_pila_desde_lista(self.lista_general)
        self.pila_contingencia.generar_informe()

    def atender_siguiente_cola(self):
        siguiente = self.cola_atencion.peek()
        if siguiente:
            print(f"\n[Siguiente en el turno - Peek]: {siguiente.nombre} (Cédula: {siguiente.cedula})")
            confirmar = input("¿Atender cliente ahora? (s/n): ").strip().lower()
            if confirmar == 's':
                atendido = self.cola_atencion.dequeue()
                if atendido:
                    atendido.estado = "Atendido"
                    print(f"\n---> Se atendió al cliente: {atendido.nombre} exitosamente.")
        else:
            print("\nNo hay clientes esperando en la cola.")

def main():
    sistema = ConsultorioOdontologico()
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE CONSULTORIO ---")
        print("1. Registrar cliente en Agenda Diaria")
        print("2. Ver Agenda Diaria completa")
        print("3. Consultar / Atender siguiente cliente")
        print("4. Generar Informe Pila de Contingencia")
        print("5. Atender siguiente cliente urgente (Pila)")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ").strip()
        
        if opcion == "1":
            sistema.registrar_cliente()
        elif opcion == "2":
            sistema.cola_atencion.mostrar_agenda()
        elif opcion == "3":
            sistema.atender_siguiente_cola()
        elif opcion == "4":
            sistema.procesar_pila_contingencia()
        elif opcion == "5":
            sistema.atender_siguiente_contingencia()
        elif opcion == "6":
            print("\n¡Gracias por utilizar el sistema!")
            break
        else:
            print("Opción inválida. Seleccione un número de 1 a 6.")

if __name__ == "__main__":
    main()
