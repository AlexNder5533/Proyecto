from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# TUPLAS fijas
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# ===================== UTILIDADES INTERNAS =====================

def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets existentes para validación O(1)."""
    return {
        registro["carnet"].strip().upper()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails existentes."""
    return {
        registro["email"].strip().lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """datos: dict con claves de CAMPOS_ESTUDIANTE. Retorna (bool, mensaje)."""
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [c for c in CAMPOS_OBLIGATORIOS if not valores[c]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado por otro estudiante"

        carnet_normalizado = valores["carnet"].upper()
        if carnet_normalizado in carnets_registrados():
            return False, f"El carnet '{carnet_normalizado}' ya se encuentra registrado"

        valores["carnet"] = carnet_normalizado
        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "Error al escribir en el almacenamiento"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} registrado con éxito"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """Retorna una LISTA de objetos Estudiante."""
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]


def obtener_por_id(id_estudiante):
    for est in obtener_todos():
        if est.id == id_estudiante:
            return est
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    """Búsqueda lineal evaluando contra los campos de la tupla CAMPOS_BUSCABLES."""
    termino = termino.strip().lower()
    if not termino:
        return []

    coincidencias = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                coincidencias.append(Estudiante.desde_diccionario(registro))
                break
    return coincidencias


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """cambios: dict con campos a modificar."""
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se suministraron cambios"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El formato de email no es válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya está en uso"

        if "carnet" in cambios:
            cambios["carnet"] = cambios["carnet"].strip().upper()
            if cambios["carnet"] in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya está en uso"

        registros = gestor.leer()
        posicion = None
        for indice, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe estudiante con ID {id_estudiante}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado correctamente"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    filtrados = [r for r in registros if r["id"] != id_estudiante]

    if len(filtrados) == len(registros):
        return False, f"No existe estudiante con ID {id_estudiante}"

    gestor.guardar(filtrados)
    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== FUNCIONALIDADES ACADÉMICAS =====================

def registrar_nota(id_estudiante, materia, nota):
    """Valida rango [0, 20], asocia la nota y actualiza el archivo JSON."""
    try:
        valor_nota = float(nota)
        if not (0 <= valor_nota <= 20):
            return False, "La calificación debe situarse entre 0 y 20"
    except (ValueError, TypeError):
        return False, "La nota debe ser un valor numérico"

    if not materia.strip():
        return False, "El nombre de la materia es obligatorio"

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No existe el estudiante con ID {id_estudiante}"

    estudiante.agregar_nota(materia, valor_nota)

    # Actualizar en la lista general de diccionarios
    registros = gestor.leer()
    for i, r in enumerate(registros):
        if r["id"] == id_estudiante:
            registros[i] = estudiante.a_diccionario()
            break

    gestor.guardar(registros)
    return True, f"Nota {valor_nota} agregada a {materia.strip().title()} para {estudiante.obtener_nombre_completo()}"


def materias_ofertadas():
    """Devuelve un CONJUNTO con todas las materias registradas sin duplicados."""
    todas = set()
    for reg in gestor.leer():
        todas.update(reg.get("materias", []))
    return todas


def estudiantes_en_comun(id_a, id_b):
    """Calcula la INTERSECCIÓN de conjuntos de materias entre dos estudiantes."""
    est_a = obtener_por_id(id_a)
    est_b = obtener_por_id(id_b)

    if not est_a or not est_b:
        return None, "Uno o ambos estudiantes no existen"

    comunes = est_a.materias_en_comun(est_b)
    return comunes, f"Materias comunes entre {est_a.nombre} y {est_b.nombre}"

# EJERCICIO 6
def clientes_por_ciudad():
    """Devuelve un DICCIONARIO agrupando: {'Guayaquil': ['Ana', 'Luis'], 'Quito': ['Sol']}."""
    agrupados = {}
    for registro in gestor.leer():
        # Obtenemos la ciudad formateada o un valor por defecto si está vacía
        ciudad = registro.get("ciudad", "").strip().title() or "Sin ciudad asignada"
        nombre_completo = f"{registro.get('nombre', '')} {registro.get('apellido', '')}".strip()

        # setdefault crea la lista vacía si la clave aún no existe y luego hace append
        agrupados.setdefault(ciudad, []).append(nombre_completo)
    return agrupados