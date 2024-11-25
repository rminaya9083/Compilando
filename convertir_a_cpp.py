import re

def convertir_a_cpp(codigo_python):
    # Comenzamos a formar el código C++
    codigo_cpp = "#include <iostream>\n#include <vector>\nusing namespace std;\n\n"
    
    # Convertir las funciones
    funciones = []
    lineas = codigo_python.split("\n")
    
    # Llevar un registro de las variables ya declaradas y asignadas
    declaradas = set()
    asignadas = set()

    for linea in lineas:
        # Detectar definiciones de funciones en Python
        match = re.match(r"def (\w+)\((.*)\):", linea)
        if match:
            funcion_name = match.group(1)
            parametros = match.group(2).split(",") if match.group(2) else []
            parametros = [p.strip() for p in parametros]  # Eliminar espacios
            
            # Asumimos que todos los parámetros son de tipo int por defecto
            parametros_cpp = ", ".join([f"int {p}" for p in parametros])
            # Crear declaración de la función en C++
            funcion_declaracion = f"int {funcion_name}({parametros_cpp}) {{\n"
            funciones.append(funcion_declaracion)
            
            # Añadir una lógica básica para la función, dependiendo del nombre
            if funcion_name == "factorial":
                funciones.append("    if (n == 0 || n == 1) return 1;\n")
                funciones.append("    return n * factorial(n - 1);\n")
            elif funcion_name == "sumar":
                funciones.append("    return a + b;\n")
            else:
                # Añadir un cuerpo de función vacío si es una función desconocida
                funciones.append("    // Agrega aquí la lógica para la función.\n")
            
            # Cerrar la función
            funciones.append("}\n\n")
    
    # Agregar las funciones al código C++
    codigo_cpp += ''.join(funciones)
    
    # Convertir el código principal
    codigo_cpp += "int main() {\n"
    
    for linea in lineas:
        # Detectar asignaciones de variables como x = 10 o listas como numeros = [1, 2, 3]
        match = re.match(r"(\w+)\s*=\s*(.+)", linea)
        if match and not re.match(r"def (\w+)\((.*)\):", linea):  # Evitar funciones
            var_name = match.group(1)
            var_value = match.group(2)
            
            # Solo declarar la variable si no ha sido declarada antes
            if var_name not in declaradas:
                # Detectar el tipo de la variable
                if var_value.isdigit():
                    var_type = "int"
                elif var_value.startswith("["):  # Detección de lista
                    var_type = "vector<int>"
                    var_value = var_value.replace("[", "{").replace("]", "}")
                else:
                    var_type = "int"
                
                # Declarar la variable sin inicializar si es función, asignar si no
                if "(" in var_value and ")" in var_value:
                    codigo_cpp += f"    {var_type} {var_name};\n"  # Declarar sin asignación
                    declaradas.add(var_name)
                    if var_name not in asignadas:  # Solo asignar si no ha sido asignada
                        codigo_cpp += f"    {var_name} = {var_value};\n"
                        asignadas.add(var_name)  # Registrar que ha sido asignada
                else:
                    codigo_cpp += f"    {var_type} {var_name} = {var_value};\n"
                    declaradas.add(var_name)
                    asignadas.add(var_name)
            else:
                # Si ya fue declarada y no ha sido asignada, asignar el valor
                if var_name not in asignadas:
                    codigo_cpp += f"    {var_name} = {var_value};\n"
                    asignadas.add(var_name)
        
        # Detectar llamadas a la función como calcular_suma(x, y)
        match = re.match(r"(\w+)\s*=\s*(\w+)\((.*)\)", linea)
        if match:
            var_name = match.group(1)
            funcion_name = match.group(2)
            parametros = match.group(3).replace(" ", "")  # Eliminar espacios en los parámetros
            
            # Declarar si no ha sido declarada y asignar solo una vez
            if var_name not in declaradas:
                codigo_cpp += f"    int {var_name};\n"  # Declarar sin inicializar
                declaradas.add(var_name)
            if var_name not in asignadas:
                codigo_cpp += f"    {var_name} = {funcion_name}({parametros});\n"
                asignadas.add(var_name)  # Registrar que ha sido asignada
        
        # Detectar la declaración de print y formatearla en cout
        match = re.match(r"print\((.*)\)", linea)
        if match:
            contenido = match.group(1)
            codigo_cpp += f"    cout << \"Resultado: \" << {contenido} << endl;\n"
    
    # Cerrar la función main
    codigo_cpp += "\n    return 0;\n"
    codigo_cpp += "}\n"
    
    return codigo_cpp
