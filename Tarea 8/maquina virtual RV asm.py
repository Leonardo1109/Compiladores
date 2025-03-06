# Clase para poder crear mejor las etiquetas
class Etiqueta:
    def __init__(self, nombre, linea):
        self.nombre = nombre
        self.linea = linea

# Función para detectar si es un caracter especial
def es_simbolo_esp(caracter):
    return caracter in "+-*;,.:!#=%&/(){}[]<><=>=="

# Funcion para separar con los separadores (espacio, tabulador, salto de linea)
def es_separador(caracter):
    return caracter in " \n\t"

# Funcion para reemplaza las comas por un espacio seguido de una coma 
def tokenizar(cadena):
    # Reemplaza las comas por un espacio seguido de una coma
    cadena = cadena.replace(',', ' ,')
    # Divide la cadena por espacios y devuelve la lista de tokens
    tokens = cadena.split()
    return tokens

# Creamos un array
instrucciones = []

# Abrimos el archivo "prog1.txt" para leerlo
arch = open('prog1.txt', 'r')
# Leemos cada linea
for ren in arch:
    # Si la linea leida es mayor a 2
    if len(ren)>2:
        # Tokenizamos la linea
        datos = tokenizar(ren)
        # Metemos los tokens al array que creamos
        instrucciones.append(datos)
# Cerramos el archivo
arch.close()

# Creamos una variable pc igual a 0 (para saber en que linea nos encontramos)
pc = 0
# Creamos un array que simulará ser nuestro procesador
registros = []
# usando una varialbe c hasta llegar a 32
for c in range(32):
    # Agregaremos 0 32 veces a nuestro procesador
    registros.append(0)

# encontrar todas las etiquetas
etiquetas = []
# Leemos todas las instrucciones tokenizadas que tenemos
for c in range(len(instrucciones)):
    # Si encuentra un % (es una funcion)
    if instrucciones[c][0] == '%':
        # Creamos objetos de tipo etiqueta con lo siguente
        etiquetas.append(Etiqueta(instrucciones[c][1], c))

# Funcion para obtener la direccion de una etiqueta   
def get_dir_etiqueta(etq):
    # Creamos una variable
    direccion = -1
    # reccorremos nuestro array con las etiquetas
    for e in etiquetas:
        # Si el nombre de uno de nuestros recorridos es igual a etq
        if e.nombre == etq:
            # Regresamos la linea donde se ecuentra
            return e.linea
    # De no ser asi regresa -1
    return direccion

# imprimir todas las etiquetas
for e in etiquetas:
    print(e.nombre, e.linea)

# Mientras en la lista de instrucciones no sea 'END'
while instrucciones[pc][0] != 'END':
    # Almacenamos la fila actual en la variable inst
    inst = instrucciones[pc]
    # Imprimimos el contador de programa (pc), el contenido del registro 2 y la instruccion actual
    print(pc, registros[2], inst)
    # Si la primera parte de la instruccion es 'ADDI'
    if inst[0] == 'ADDI':
        # Extraemos los valores necesarios de la instruccion para realizar una suma
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5]) # valor numerico del 6to elemento
        # Realizamos la suma y actualizamos el registro destino
        registros[destino] = registros[reg1] + numero
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    # Si la instruccion comienza con '%' avanzamos e incrementamos PC
    elif inst[0] == '%':
        pc = pc + 1
    # Jump salta a la direccion indicada)
    elif inst[0] == 'J':
        # Obtenemos la etiqueta a la que vamos a saltar
        etq = inst[1]
        # Buscamos la direccion correspondiente a esa etiqueta en la tabla de etiquetas
        pc = get_dir_etiqueta(etq)
        # Imprimimos un mensaje indicando que estamos saltando a esa direccion
        print('saltando a', pc)
    # Si la instruccion es una comparacion mayor o igual (BGE)
    elif inst[0] == 'BGE':
        # Extraemos los valores necesarios para la comparacion
        op1 = registros[int(inst[1][1:])]
        num = int(inst[3])
        etq = inst[5]
        # Imprimimos los valores que estamos comparando
        print('comparando ', op1, 'con', num)
        # Si la operacion es verdadera, saltamos a la etiqueta indicada
        if op1 >= num:
            pc = get_dir_etiqueta(etq)
        # Si la operacion es falsa, simplemente avanzamos al siguiente paso
        else:
            pc = pc + 1
    elif inst[0] == 'SUB':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5][1:]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] - registros[numero]
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'SUBI':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] - numero
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'MUL':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5][1:]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] * registros[numero]
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'MULI':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] * numero
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'ADD':
        # Extraemos los valores necesarios de la instruccion para realizar una suma
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5]) # valor numerico del 6to elemento
        # Realizamos la suma y actualizamos el registro destino
        registros[destino] = registros[reg1] + registros[numero]
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'DIV':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5][1:]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] / registros[numero]
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    elif inst[0] == 'DIVI':
        # Extraemos los valores necesarios de la instruccion para realizar una resta
        destino = int(inst[1][1:]) # valor numerico del 2do elemento
        reg1 = int(inst[3][1:]) # valor numerico del 4to elemento
        numero = int(inst[5]) # valor numerico del 6to elemento
        # Realizamos la resta y actualizamos el registro destino
        registros[destino] = registros[reg1] / numero
        # Incrementamos el contador de programa para pasar a la siguiente instruccion
        pc = pc + 1
    

# Ver los registros
print(registros)

