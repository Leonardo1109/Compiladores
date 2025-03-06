# Creamos una clase variable para asignar nuevos objetos de tipo variable
# Asignamos el valor del atributo valor para que se haga refrencia al del objeto
class Variable:
    def __init__(self, nombre, tipo, valor):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor

# Esta funcion sirve para agregar laos objetos de tipo variable a un array
# Agregamos el atributo VALOR
def agrega_var(tabla_var, nombre, tipo, valor):
    tabla_var.append(Variable(nombre, tipo, valor))
    pass

# Funcion para verificar si existe ya existe una variable con el mismo nombre
def existe_var(tabla_var, nombre):
    # Creamos una bandera
    encontrado = False
    for v in tabla_var:
        # Buscamos el nombre de la variable en nuestro array
        if v.nombre == nombre:
            # Si la encontramos cambiamos la bandera a True
            encontrado = True
    return encontrado

# Funcion para reasignar un valor a una variable ya existente
def set_var(tabla_var, nombre, valor):
    # Buscamos si existe la variable
    if existe_var(tabla_var, nombre):
        for v in tabla_var:
            # Buscamos la variable con el nombre que queremos reasignar
            if v.nombre == nombre:
                # Cambiamos el valor
                v.valor = valor
    # Si no existe la variable
    else:
        # Retornamos un error
        print('variable ', nombre, 'no encontrada')
        return None

# Funcion para imrpimir todas las variables almacenadas
def imprime_tabla_var(tabla_var):
    print()
    print('   Tabla de variables')
    print('nombre\t\ttipo\t\tvalor')
    for v in tabla_var:
        # Imprime los campos de los objetos
        print(v.nombre,'\t\t', v.tipo,'\t\t', v.valor)
    return None

#                               SEPARA TOKENS

# Funcion para detectar si es un caracter especial
def es_simbolo_esp(caracter):
    return caracter in "+-*;,.:!#=%&/(){}[]<><=>=="

# Funcion para ver si es un separador
def es_separador(caracter):
    return caracter in " \n\t"

# Funcion para detectar si se trata de un id
def es_id(cad):
    return (cad[0] in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Funcion para detectar si se trata de una palabra reservada
def  es_pal_res(cad):
    palres = ["int","real","string", 'print', 'read', 'tabla']
    return (cad in palres)

# Funcion para ver si se trata de un tipo de dato
def  es_tipo(cad):
    tipos = ["int","real","string"]
    return (cad in tipos)

def esEntero(dato):
    if isinstance(dato, int):
        return True
    else:
        return False

# Funcion para separar en tokens nuestro codigo
def separa_tokens(linea):
    # Revisamos que el codigo que nos dieron no sea menor a 3 caracteres
    if len(linea) < 3:
        return []
    else: # Si es mayor a 3 caracteres     
        tokens = []
        tokens2 = []    
        dentro = False 
        # Revisamos caracter por caracter  
        for l in linea:
            # Si es simbolo especial
            if es_simbolo_esp(l) and not(dentro):
                # agregalo a la lista de tokens
                tokens.append(l)
            # si es simbolo especial o separador
            if (es_simbolo_esp(l) or es_separador(l)) and dentro:
                tokens.append(cad)
                dentro = False
                # Si es simbolo especial
                if es_simbolo_esp(l):
                    # Agregalo a la lista
                    tokens.append(l)
            # Si no es simbolo espcial y no es separador asumimos que es un id
            if not (es_simbolo_esp(l)) and not (es_separador(l)) and not(dentro):
                #cambiamos la bandera para guardar el id
                dentro = True
                cad=""
            # Si no es simbolo espcial y no es separador y la bandera esta activada
            if not (es_simbolo_esp(l)) and not (es_separador(l)) and dentro:
                    # Almacenamos el valor en una variable
                    cad = cad + l

        # Creamos una bandera
        compuesto = False
        # Recorremos nuestros tokens menos 1
        for c in range(len(tokens)-1):
            if compuesto:
                compuesto = False
                continue
            # Si en el token que leemos encontramos un operador y el siguente es un =
            if tokens[c] in "=<>!" and tokens[c+1]=="=":
                # agregamos a nuestro arreglo de tokens el token c mas =
                tokens2.append(tokens[c]+"=")
                compuesto = True
            # Si no, continuamos sin agregar el =
            else:
                tokens2.append(tokens[c])
        # Agrega el último token a la lista tokens2
        tokens2.append(tokens[-1])

        # Recorre la lista tokens2 para encontrar los decimales
        for c in range(1,len(tokens2)-1):
            # si el token es . busca si el anterior y consecuente es entero
            if tokens2[c]=="." and esEntero(tokens2[c-1]) and esEntero(tokens2[c+1]):
                # Si es asi, elimina el anterior y consecuente y los une con c
                tokens2[c]=tokens2[c-1]+tokens2[c]+tokens2[c+1]
                # Marcamos los tokens para borrarlos
                tokens2[c-1]="borrar"
                tokens2[c+1]="borrar"
        # Borramos los anteriores y consecuentes    
        porBorrar = tokens2.count("borrar")
        for c in range(porBorrar):
            tokens2.remove("borrar")
        # Limpiamos el array tokens
        tokens=[]
        # Creamos una bandera
        dentroCad = False
        # Creamos una cadena vacia
        cadena = ""
        # Recorremos tokens2
        for t in tokens2:
            # Si la bandera esta activa     
            if dentroCad:
                # Revisamos si termina en comillas
                if t[-1]=='"':
                    # Agrega el token a la cadena actual
                    cadena=cadena+" "+t
                    # Agrega la cadena actual, sin las comillas, a la lista de tokens
                    tokens.append(cadena[1:-1])
                    # Cambia bandera a False
                    dentroCad = False
                else:
                    # Agregar token a la cadena
                    cadena = cadena+" "+t
            # Si el token actual comienza con "
            elif ((t[0]=='"')):
                  # Guardamos el valor t en la cadena
                  cadena= t
                  # Actuvamos la bandera
                  dentroCad = True
            # Si no es una cadena
            else:
                  tokens.append(t)
    return tokens

# Creamos un array
tabla_var = []
# Creamos una cadena vacia
ren = ""
# Mientras la cadena no sea igual a end; el codigo continua
while (ren != 'end;'):
    # Solicitamos el ingreso de una línea de código
    ren = input('$:')
    # Separamos lo que ingresaron en tokens
    tokens = separa_tokens(ren)
    # Verificamos si el primer token es un ID
    if es_id(tokens[0]):
        # Verificamos si el primer token es una palabra reservada
        if es_pal_res(tokens[0]):
            # Verificamos si el primer token es un tipo
            if es_tipo(tokens[0]):
                # Verificamos si el segundo token es un ID
                if es_id(tokens[1]): 
                    # CODIGO PARA AGREGAR VALORES A LA TABLA
                    if(tokens[2] == '=' and tokens[4] == ';'):
                        agrega_var(tabla_var, tokens[1], tokens[0], tokens[3])   
                    else:
                    # Agregamos a nuestra tabla el nombre de nuestro variable y valor
                        agrega_var(tabla_var, tokens[1], tokens[0], None)
            # Si el token es read
            elif tokens[0] == 'read':
                # Si el siguente token es un ( y el siguente un Id y el siguente )
                if tokens[1] == '(' and es_id(tokens[2]) and tokens[3] == ')':
                    # Leer un valor del usuario e insertarlo en la variable correspondiente
                    leido = input()
                    set_var(tabla_var, tokens[2], leido)
            # Si el token es read
            elif tokens[0] == 'tabla':               
                # Imprimir la tabla de variables con los valores
                imprime_tabla_var(tabla_var)        

            # CODIGO PARA IMPRIMIR USANDO print();
            # Verificar si el token es la palabra reservada 'print'
            elif tokens[0] == 'print':
                if tokens[1] == '(' and es_id(tokens[2]) and tokens[3] == ')' and tokens[4] == ';':  
                    # Verificamos si la variable existe antes de imprimir
                    if existe_var(tabla_var, tokens[2]):
                        for v in tabla_var:
                            # Busca la variable
                            if v.nombre == tokens[2]:
                                print(v.valor)
                    else:
                        # Mostrar un mensaje de error si la variable no se encuentra
                        print('Error Variable', tokens[2], 'no encontrada')