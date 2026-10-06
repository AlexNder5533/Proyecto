import os

COLORES = {
    "ROJO": "",
    "VERDE": "",
    "AZUL": "",
    "AMARILLO": "",
    "CYAN": "",
    "BLANCO": "",
    "RESET": "",
}

RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    print(texto)


def imprimir_titulo(texto):
    limpiar_pantalla()
    print("=" * 65)
    print(f"  {texto}".center(65))
    print("=" * 65)
    print()


def imprimir_exito(mensaje):
    print(f" {mensaje}")


def imprimir_error(mensaje):
    print(f" {mensaje}")


def imprimir_info(mensaje):
    print(f" {mensaje}")


def confirmar(pregunta):
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")