from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, registrar_nota,
    materias_ofertadas, estudiantes_en_comun
)
from views import (
    crear_cliente,
    obtener_todos,
    obtener_por_id,
    buscar_clientes,
    actualizar_cliente,
    eliminar_cliente,
    estadisticas,
    clientes_por_ciudad,  # <-- AGREGAR AQUÍ
)

# ---------- EXTRA · AGRUPADOS POR CIUDAD ----------
def opcion_clientes_por_ciudad():
    imprimir_titulo("CLIENTES AGRUPADOS POR CIUDAD")
    agrupados = clientes_por_ciudad()

    if not agrupados:
        imprimir_info("No hay clientes registrados en el sistema.")
    else:
        for ciudad, nombres in agrupados.items():
            print(f"{ciudad} ({len(nombres)} cliente(s)):")
            for nombre in nombres:
                print(f"    • {nombre}")
            print()  

    pausa()

def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<14}{'NOMBRE':<25}{'EMAIL':<28}{'PROM':<6}")
    print("-" * 78)
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<14}{est.obtener_nombre_completo():<25}"
              f"{est.email:<28}{est.obtener_promedio():<6}")
    print("-" * 78)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("REGISTRAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Término (nombre, apellido, carnet o email): ")
    encontrados = buscar_estudiantes(termino)
    if not encontrados:
        imprimir_info(f"No se hallaron coincidencias para '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser numérico")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco si no desea modificar el campo.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser numérico")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Se eliminará a: {estudiante}")
    if confirmar("¿Está seguro de continuar?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Acción cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("ASIGNAR CALIFICACIÓN")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Estudiante: {estudiante.obtener_nombre_completo()}")
    materia = input("Materia: ").strip()
    nota = input("Calificación (0 - 20): ").strip()

    exito, mensaje = registrar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_detalle():
    imprimir_titulo("DETALLE ACADÉMICO Y PROMEDIO")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser numérico")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    print(f"\nEstudiante : {estudiante.obtener_nombre_completo()}")
    print(f"Carnet     : {estudiante.carnet}")
    print(f"Email      : {estudiante.email}")
    print(f"Materias   : {', '.join(sorted(estudiante.materias)) if estudiante.materias else 'Ninguna'}")
    print("\nNotas registradas:")
    if not estudiante.notas:
        print("  (Sin calificaciones)")
    else:
        for materia, calificaciones in estudiante.notas.items():
            prom_materia = round(sum(calificaciones) / len(calificaciones), 2)
            print(f"  - {materia:<18}: {calificaciones} -> Promedio: {prom_materia}")

    imprimir_exito(f"\nPromedio General: {estudiante.obtener_promedio()}")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("COMPARAR MATERIAS EN COMÚN")
    try:
        id_a = int(input("ID del primer estudiante: "))
        id_b = int(input("ID del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    if id_a == id_b:
        imprimir_error("Debe ingresar dos IDs distintos")
        return pausa()

    comunes, mensaje = estudiantes_en_comun(id_a, id_b)
    if comunes is None:
        imprimir_error(mensaje)
    else:
        imprimir_info(mensaje)
        if comunes:
            print(f"\nMaterias compartidas ({len(comunes)}):")
            for mat in sorted(comunes):
                print(f"  - {mat}")
        else:
            print("\nNo comparten ninguna materia inscrita.")
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("CATÁLOGO DE MATERIAS ACTIVAS")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias registradas aún en el sistema.")
    else:
        imprimir_info(f"Total de materias registradas: {len(materias)}")
        for mat in sorted(materias):
            print(f"  - {mat}")
    pausa()


def salir():
    imprimir_info("¡Hasta pronto!")
    return "salir"


OPCIONES = {
    "1": ("Registrar estudiante", opcion_crear),
    "2": ("Listar todos", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Actualizar datos", opcion_actualizar),
    "5": ("Eliminar estudiante", opcion_eliminar),
    "6": ("Agregar nota a materia", opcion_agregar_nota),
    "7": ("Ver ficha y promedio", opcion_ver_detalle),
    "8": ("Materias en común entre dos estudiantes", opcion_materias_en_comun),
    "9": ("Ver todas las materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA (ESTUDIANTES)")
    for tecla, (texto, _) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción incorrecta")
            pausa()
            continue

        _, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución cancelada por el usuario.")