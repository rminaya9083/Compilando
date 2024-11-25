class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add(self, name, data_type, line, value=None, scope="Global"):
        # Verifica si la variable ya existe antes de agregarla
        for symbol in self.symbols:
            if symbol['Name'] == name and symbol['Scope'] == scope:
                return  # No agregar duplicados
        self.symbols.append({
            'Name': name,
            'Type': data_type,
            'Line': line,
            'Value': value,
            'Scope': scope
        })

    def lookup(self, name):
        """Verifica si una variable está en la tabla de símbolos."""
        for symbol in self.symbols:
            if symbol['Name'] == name:
                return symbol
        return None

    def clear(self):
        """Limpia la tabla de símbolos."""
        self.symbols = []

    def get_symbols(self):
        """Devuelve la lista de símbolos."""
        return self.symbols
