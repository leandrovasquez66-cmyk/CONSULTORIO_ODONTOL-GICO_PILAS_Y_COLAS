# ==============================================================================
# EDUARD LEANDRO VASQUEZ HIDALGO
# Código: 106202622568
# Universidad de Manizales
# ==============================================================================

import datetime

class Cliente:
    """Modelo de datos para los pacientes del consultorio."""
    
    def __init__(self, cedula, nombre, telefono, tipo_atencion, prioridad, fecha):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_atencion = tipo_atencion
        self.prioridad = prioridad
        self.estado = "Pendiente"
        self.fecha_str = fecha
        # Convertimos la fecha a objeto date para poder comparar y ordenar en la Pila
        self.fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()

    def __str__(self):
        return f"Cédula: {self.cedula} | Nombre: {self.nombre} | Tel: {self.telefono} | Atención: {self.tipo_atencion.capitalize()} | Prioridad: {self.prioridad} | Fecha: {self.fecha_str}"