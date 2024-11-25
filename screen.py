# screen.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
from convertir_a_cpp import convertir_a_cpp
from lexical_analyzer import LexicalAnalyzer  # Importar el analizador léxico
import subprocess  # Para ejecutar sintactico.py


# Función para manejar la conversión, el análisis léxico y ejecutar sintactico.py
def procesar_codigo():
    codigo_python = text_input.get("1.0", "end-1c")  # Obtener el texto de la caja de entrada
    if not codigo_python.strip():  # Verificar si el código está vacío
        messagebox.showwarning("Advertencia", "Por favor ingresa un código Python.")
        return
    
    # Procesar la conversión de Python a C++
    try:
        codigo_cpp = convertir_a_cpp(codigo_python)
        text_output.config(state="normal")  # Habilitar la caja de texto de salida  
        text_output.delete("1.0", "end")  # Limpiar el contenido previo
        text_output.insert("1.0", codigo_cpp)  # Insertar el código C++ convertido
        text_output.config(state="disabled")  # Deshabilitar la edición
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al convertir el código: {e}")

    # Procesar el análisis léxico
    try:
        analyzer = LexicalAnalyzer()  # Crear el analizador léxico
        analyzer.analyze(codigo_python)  # Analizar el código
        symbols = analyzer.symbol_table.get_symbols()  # Obtener la lista de símbolos
        
        # Mostrar los símbolos en un cuadro de texto
        symbol_output.config(state="normal")
        symbol_output.delete("1.0", "end")  # Limpiar contenido previo
        for symbol in symbols:
            symbol_output.insert("end", f"Nombre: {symbol['Name']}, Tipo: {symbol['Type']}, Línea: {symbol['Line']}, Valor: {symbol['Value']}, Ámbito: {symbol['Scope']}\n")
        symbol_output.config(state="disabled")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al analizar el código: {e}")

    # Ejecutar sintactico.py y mostrar los resultados en el cuadro de texto
    try:
        result = subprocess.run(
            ['python', 'sintactico.py'], 
            input=codigo_python, 
            text=True, 
            capture_output=True
        )
        output_text.config(state="normal")
        output_text.delete("1.0", "end")  # Limpiar contenido previo
        output_text.insert("1.0", result.stdout)  # Mostrar la salida del análisis sintáctico y semántico
        output_text.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al ejecutar el análisis sintáctico: {e}")


# Crear la ventana principal
root = ttk.Window(themename="darkly")  # Cambia el tema aquí (ej: flatly, darkly, cyborg, etc.)
root.title("Convertidor de Python a C++")
root.geometry("1200x900")  # Ajustar el tamaño de la ventana
root.resizable(True, True)

# Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición x e y para centrar la ventana
x = (screen_width // 2) - (1200 // 2)
y = (screen_height // 2) - (900 // 2)

# Posicionar la ventana en el centro de la pantalla
root.geometry(f"1200x900+{x}+{y}")

# Contenedor principal
frame_main = ttk.Frame(root, padding=20)
frame_main.pack(fill=BOTH, expand=YES)

# Crear un subframe para organizar los cuadros de texto en columnas
frame_text = ttk.Frame(frame_main)
frame_text.pack(fill=BOTH, expand=YES)

# Etiqueta de entrada y caja de texto para el código Python (columna izquierda)
label_input = ttk.Label(frame_text, text="Ingresa tu código Python:", font=("Helvetica", 14))
label_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")

text_input = ttk.Text(frame_text, height=20, width=50)
text_input.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Etiqueta de salida y caja de texto para el código C++ (columna derecha)
label_output = ttk.Label(frame_text, text="Resultado en C++:", font=("Helvetica", 14))
label_output.grid(row=0, column=1, padx=5, pady=5, sticky="w")

text_output = ttk.Text(frame_text, height=20, width=50, state="disabled", bg="#f8f9fa")
text_output.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Etiqueta de salida y caja de texto para la tabla de símbolos (debajo de los cuadros de texto)
label_symbol_output = ttk.Label(frame_main, text="Tabla de Símbolos:", font=("Helvetica", 14))
label_symbol_output.pack(padx=5, pady=5, anchor="w")

symbol_output = scrolledtext.ScrolledText(frame_main, height=10, width=100, state="disabled", bg="#f8f9fa")
symbol_output.pack(padx=5, pady=10)

# Etiqueta de salida y cuadro de texto para los resultados del análisis sintáctico y semántico
label_output_results = ttk.Label(frame_main, text="Resultados del Análisis Sintáctico y Semántico:", font=("Helvetica", 14))
label_output_results.pack(padx=5, pady=5, anchor="w")

output_text = scrolledtext.ScrolledText(frame_main, height=10, width=100, state="normal", bg="#f8f9fa")
output_text.pack(padx=5, pady=10)

# Configurar el grid para que las columnas se expandan igualmente
frame_text.columnconfigure(0, weight=1)
frame_text.columnconfigure(1, weight=1)

# Botón para convertir, analizar léxicamente y ejecutar sintactico.py
button_procesar = ttk.Button(frame_main, text="Convertir y Analizar", command=procesar_codigo, bootstyle="primary")
button_procesar.pack(pady=10)

# Ejecutar la interfaz
root.mainloop()
