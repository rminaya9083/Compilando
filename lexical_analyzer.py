import re

class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add(self, name, data_type, line, value=None, scope="Global"):
        for symbol in self.symbols:
            if symbol['Name'] == name and symbol['Scope'] == scope:
                return
        self.symbols.append({
            'Name': name,
            'Type': data_type,
            'Line': line,
            'Value': value,
            'Scope': scope
        })

    def clear(self):
        self.symbols = []

    def get_symbols(self):
        return sorted(self.symbols, key=lambda x: (x['Name'], x['Line']))

class LexicalAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.tokens = []

    def analyze(self, code):
        self.tokens = []
        self.symbol_table.clear()

        token_specification = [
            ('KEYWORD', r'\b(if|else|while|return|def|class|import|from|as|with|for|in|try|except|raise)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
            ('NUMBER', r'\b\d+(\.\d+)?\b'),
            ('STRING', r'(\".*?\"|\'.*?\')'),
            ('OPERATOR', r'[+\-*/%=<>!&|~^:]'),
            ('DELIMITER', r'[\[\]{}(),.;:]'),
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'#.*'),
            ('MISMATCH', r'.')
        ]

        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        line_num = 1
        scope = "Global"

        for match in re.finditer(tok_regex, code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'WHITESPACE':
                if '\n' in value:
                    line_num += value.count('\n')
                continue
            elif kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                raise ValueError(f'Unexpected character: {value}')
            else:
                if kind == 'IDENTIFIER':
                    if '=' in code.splitlines()[line_num - 1]:
                        assigned_value = code.splitlines()[line_num - 1].split('=')[-1].strip()
                        self.symbol_table.add(value, "Variable", line_num, value=assigned_value, scope=scope)
                    else:
                        self.symbol_table.add(value, "Variable", line_num, scope=scope)
                elif kind == 'STRING':
                    self.symbol_table.add(value, "String", line_num, value=value, scope=scope)
                elif kind == 'NUMBER':
                    self.symbol_table.add(value, "Number", line_num, value=value, scope=scope)
                self.tokens.append((kind, value, line_num))

        return self.tokens
