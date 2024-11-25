# sintactico.py

import sys
from lark import Lark, UnexpectedInput
from pyflakes.api import check
from pyflakes.reporter import Reporter
from io import StringIO

# Gramática con Lark
gramatica = """
    start: statement+

    statement: IDENTIFICADOR "=" expression

    expression: term
              | expression "+" term
              | expression "-" term

    term: factor
        | term "*" factor
        | term "/" factor

    factor: IDENTIFICADOR
          | NUMBER
          | "(" expression ")"

    %import common.CNAME -> IDENTIFICADOR
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

# Crear el parser
parser = Lark(gramatica, parser='lalr', propagate_positions=True)

# Función para analizar el código
def analizar_codigo(codigo_entrada):
    lineas = codigo_entrada.split("\n")
    errores = []
    variables_definidas = set()  # Almacena las variables declaradas

    # Etapa 1: Análisis con Lark
    for i, linea in enumerate(lineas, start=1):
        try:
            tree = parser.parse(linea)

            # Verificar declaración de variables
            if "=" in linea:
                # Extraer la variable declarada
                variable = linea.split("=")[0].strip()
                variables_definidas.add(variable)

            # Validar uso de variables en expresiones
            tokens = [str(token) for token in tree.children if isinstance(token, str)]
            for token in tokens:
                if token not in variables_definidas and not token.isdigit() and not token.startswith("("):
                    errores.append(f"Línea {i}: Variable '{token}' no definida.")

        except UnexpectedInput as e:
            columna = e.column
            contexto = e.get_context(linea)
            errores.append(f"Línea {i}, columna {columna}: {contexto.strip()}")

    # Etapa 2: Análisis con pyflakes
    buffer = StringIO()
    reporter = Reporter(buffer, buffer)
    check(codigo_entrada, reporter)

    # Obtener los errores reportados por pyflakes
    pyflakes_errores = buffer.getvalue()
    if pyflakes_errores:
        errores.append("Errores de pyflakes:\n" + pyflakes_errores)

    # Retornar los errores encontrados
    return errores


# Función para correr el analizador sin interfaz gráfica
def ejecutar_analizador(codigo_entrada):
    errores = analizar_codigo(codigo_entrada)
    resultado = "Errores encontrados:\n" if errores else "No se encontraron errores de sintaxis ni variables no definidas.\n"
    resultado += "\n".join(errores)
    return resultado


# Comprobamos si el script está siendo ejecutado directamente o no
if __name__ == "__main__":
    # Leer el código Python proporcionado como entrada
    codigo_entrada = sys.stdin.read().strip()

    # Ejecutar el análisis sin abrir la interfaz gráfica
    resultado = ejecutar_analizador(codigo_entrada)

    # Devolver el resultado al proceso que ejecutó este script
    print(resultado)
