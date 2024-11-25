# Traductor_Python.py

def translate_data_type(py_type):
    """
    Traduce un tipo de dato de Python a su equivalente en C++.
    
    Argumentos:
        py_type (str): El tipo de dato en Python (por ejemplo, "int", "float", "str", "bool", "list").
        
    Retorna:
        str: El tipo de dato equivalente en C++.
    
    Ejemplo:
        translate_data_type("int") -> "int"
        translate_data_type("str") -> "std::string"
    """
    type_map = {
        "int": "int",                   # Entero en Python se convierte a int en C++
        "float": "double",               # Flotante en Python se convierte a double en C++
        "str": "std::string",            # Cadena en Python se convierte a std::string en C++
        "bool": "bool",                  # Booleano en Python se convierte a bool en C++
        "list": "std::vector<auto>",     # Lista en Python se convierte a std::vector<auto> en C++
    }
    return type_map.get(py_type, "auto")  # Si el tipo no está en el mapeo, usa "auto" como predeterminado


def translate_print_statement(argument):
    """
    Traduce una declaración de impresión en Python a una instrucción de salida en C++.
    
    Argumentos:
        argument (str): El argumento que se va a imprimir en la declaración de print.
        
    Retorna:
        str: La declaración de impresión en C++ usando std::cout.
    
    Ejemplo:
        translate_print_statement("x") -> "std::cout << x << std::endl;"
    """
    return f"std::cout << {argument} << std::endl;"


def translate_for_loop(loop_var, start, end):
    """
    Traduce un bucle for en Python a un bucle for en C++.
    
    Argumentos:
        loop_var (str): El nombre de la variable de control del bucle.
        start (str): El valor inicial de la variable de control.
        end (str): El valor de fin de la variable de control (no inclusivo).
        
    Retorna:
        str: La declaración de un bucle for en C++.
    
    Ejemplo:
        translate_for_loop("i", "0", "10") -> "for (int i = 0; i < 10; ++i) {"
    """
    return f"for (int {loop_var} = {start}; {loop_var} < {end}; ++{loop_var}) {{"


def translate_if_statement(condition):
    """
    Traduce una declaración if en Python a una declaración if en C++.
    
    Argumentos:
        condition (str): La condición para evaluar en la instrucción if.
        
    Retorna:
        str: La declaración if en C++.
    
    Ejemplo:
        translate_if_statement("x > 5") -> "if (x > 5) {"
    """
    return f"if ({condition}) {{"
