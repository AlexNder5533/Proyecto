import json

# TUPLA fija con los campos editables/básicos de un Estudiante
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """
    MODELO: Representa a un estudiante.
    Demuestra las 4 colecciones de Python:
    - dict: self.notas agrupadas por materia {"Matemática": [18, 19]}
    - list: listas de notas dentro del diccionario
    - set: self.materias donde está inscrito (sin repetidos)
    - tuple: CAMPOS_ESTUDIANTE (constante inmutable a nivel módulo)
    """

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        # DICCIONARIO de LISTAS: {"Materia": [calificaciones]}
        self.notas = notas if notas is not None else {}
        # CONJUNTO: materias sin duplicados
        self.materias = set(materias) if materias is not None else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # set.add() garantiza elementos únicos
        self.materias.add(materia.strip().title())

    def agregar_nota(self, materia, nota):
        materia_limpia = materia.strip().title()
        self.inscribir_materia(materia_limpia)
        # setdefault genera la lista si la materia no estaba en el diccionario
        self.notas.setdefault(materia_limpia, []).append(round(float(nota), 2))

    def obtener_promedio(self):
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)
        if not todas:
            return 0.0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN DE CONJUNTOS (&)
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        # Conversión objeto -> dict compatible con JSON (set se transforma a list ordenada)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        # Conversión dict -> objeto (la list de JSON vuelve a ser set)
        return cls(
            id_estudiante=datos["id"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            email=datos["email"],
            carnet=datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"