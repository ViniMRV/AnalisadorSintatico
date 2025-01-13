#Eric Goulart da Cunha - 2110778
#Vinícius Machado da Rocha Viana - 2111343

import ply.lex as lex
import ply.yacc as yacc

# Palavras reservadas
palavras_reservadas = {
    'INICIO': 'INICIO',
    'MONITOR': 'MONITOR',
    'EXECUTE': 'EXECUTE',
    'TERMINO': 'TERMINO',
    'ENQUANTO': 'ENQUANTO',
    'FACA': 'FACA',
    'FIM': 'FIM',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'EVAL': 'EVAL',
    'ZERO': 'ZERO',
}

# Lista de tokens
tokens = [
        'SOMA', 'MULT', 'IGUAL', 'VIRGULA', 'EPAREN', 'DPAREN', 'NUMERO', 'ID'
] + list(palavras_reservadas.values())

# Regras de análise léxica
t_SOMA = r'\+'
t_MULT = r'\*'
t_IGUAL = r'='
t_VIRGULA = r','
t_EPAREN = r'\('
t_DPAREN = r'\)'


def t_RESERVED(t):
        r'[A-Z][A-Z]*'
        t.type = palavras_reservadas.get(t.value, 'ID')
        return t


def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t


def t_NUMERO(t):
        r'\d+'
        t.value = int(t.value)
        return t


# Ignorar espaços em branco e caracteres de tabulação
t_ignore = ' \t\n'


# Manipulador de erros léxicos
def t_error(t):
        print("Error: caractere ilegal " + t.value[0])
        t.lexer.skip(1)
        exit(1)


lexer = lex.lex()

start = 'programa'

# Variável global para monitoradas
monitoradas = []


# Regras da análise sintática
def p_programa(p):
        'programa : INICIO varlist MONITOR monitorados EXECUTE cmds TERMINO'
        vars = p[2].split(", ") + p[4].split(", ")
        initialize_vars = ""
        for var in vars:
                if var not in ', ':
                        initialize_vars += f'{var} = 0\n'
                        if var in p[4].split(", "):
                                initialize_vars += f'print({var})\n'

        p[0] = f'{initialize_vars}\n{p[6]}\n\n'


def p_monitorados(p):
        '''monitorados : varlist'''
        p[0] = p[1]
        global monitoradas
        qtd_monitorados = len(p[1].split(", "))
        monitoradas = monitoradas[-qtd_monitorados:]


def p_varlist(p):
        '''varlist : ID VIRGULA varlist 
                   | ID'''
        if len(p) > 2:
                p[0] = f'{p[1]}, {p[3]}'
        else:
                p[0] = p[1]
        global monitoradas
        monitoradas.append(p[1])


def p_cmds(p):
        '''cmds : cmd cmds 
                | cmd'''
        if len(p) > 2:
                p[0] = f'{p[1]}\n{p[2]}'
        else:
                p[0] = f'{p[1]}'


def p_cmd(p):
        '''cmd : while 
               | if 
               | ifelse 
               | eval 
               | zero
               | soma
               | mult
               | atr'''
        p[0] = p[1]


def p_while(p):
        'while : ENQUANTO ID FACA cmds FIM'
        indentation = f'{p[4]}'.replace('\n', '\n\t')
        p[0] = f'while {p[2]} != 0:\n\t{indentation}'


def p_if(p):
        'if : IF ID THEN cmds FIM'
        indentation = f'{p[4]}'.replace('\n', '\n\t')
        p[0] = f'if {p[2]} != 0:\n\t{indentation}'


def p_ifelse(p):
        'ifelse : IF ID THEN cmds ELSE cmds FIM'
        indentation_if = f'{p[4]}'.replace('\n', '\n\t')
        indentation_else = f'{p[6]}'.replace('\n', '\n\t')
        p[0] = f'if {p[2]} != 0:\n\t{indentation_if}\nelse:\n\t{indentation_else}'


def p_eval(p):
        'eval : EVAL EPAREN ID VIRGULA ID VIRGULA cmds DPAREN'
        indentation = f'{p[7]}'.replace('\n', '\n\t')
        p[0] = f'for i in range({p[3]}-{p[5]}):\n\t{indentation}'


def p_zero(p):
        'zero : ZERO EPAREN ID DPAREN'
        p[0] = f'{p[3]} = 0'
        if p[3] in monitoradas:
                p[0] += f'\nprint("{p[3]} =", {p[3]})'


def p_soma(p):
        '''soma : ID SOMA expr
                | NUMERO SOMA expr'''

        p[0] = f'{p[1]} + {p[3]}'


def p_mult(p):
        '''mult : ID MULT expr
                | NUMERO MULT expr'''

        p[0] = f'{p[1]} * {p[3]}'


def p_expr(p):
        '''expr : ID
                | NUMERO
                | soma
                | mult'''
        p[0] = p[1]


def p_atr(p):
        '''atr : ID IGUAL expr'''
        global monitoradas
        p[0] = f'{p[1]} = {p[3]}'
        if p[1] in monitoradas:
                p[0] += f'\nprint("{p[1]} =", {p[1]})'


# Manipulador de erros sintáticos
def p_error(p):
        print("Error: erro de sintaxe na entrada...", p)
        exit(1)


parser = yacc.yacc()

nome_entrada = input(
    "Digite o nome do arquivo Provol-One (.provol) que será convertido: ")
nome_saida = input("Digite o nome do arquivo de saída com a extensão .py: ")

with open(nome_entrada, "r") as arquivo_entrada, open(nome_saida,
                                                      "w") as arquivo_saida:
        codigo = arquivo_entrada.read()

        lexer.input(codigo)
        codigo_gerado = parser.parse(codigo)
        if codigo_gerado:
                arquivo_saida.write(codigo_gerado)
                print("Arquivo de saída gerado. Operação finalizada.")
        else:
                print(
                    "Não foi possível realizar conversão... Operação abortada."
                )
