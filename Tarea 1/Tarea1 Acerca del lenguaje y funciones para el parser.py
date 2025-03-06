"""
Esta funcion sirve para ver los separadores de un texto, nos servirá para
separa en tokens nuestro codigo
"""
def esSeparador(c):
    separadores = "\n\t " #salto de linea, tabulaciones y espacio
    return c in separadores

"""
Esta funcion detectará algun simbolo especial, de esta manera será mas sencillo
asignarle esa etiqueta a los tokens
"""
def esSimboloEsp(c):
    especiales = "¡#$%&/*+-=:;[]{}(),"
    return c in especiales

"""
Esta función es algo extensa, será la primera que usemos y nos sevirá para
quitar los comentarios de nuestro codigo, de esta manera, sin comentarios,
posteriomente podremos empezar a separar en tokens
"""
def quitaComentarios(cad):
    # estados: A, B, C, Z.
    """Segun lo visto en clase, aprovechamos el uso de las maquinas de estado
    para saber en que punto estamos, a continuacion se explicara como funciona"""
    estado ="Z"    #representa el estado inicial
    #cad = "a=b/c;"
    cad2 =""        #creamos una cadena temporal donde almacenaremos el codigo
    for c in cad:
        if (estado=="Z"): #revisamos si estamos en el estado incial
            if (c=="/"): #si encontramos un / puede comenzar un cometario
                estado = "A" #cambiamos a estado A donde PODRIA ser un comentario
            else:
                cad2 = cad2 + c # si no comienza comentario metemos en cad2
        elif (estado=="A"): # estamos en el estado donde PODRIA se un comentario
            if (c=="*"): # sigue un *, estamos seguros que es un comentario
                estado="B" #cambiamos a estado B donde estamos ya en comentario
            else: # si no recibimos un * puede que sea una divicion 
                estado = "Z" #volvemos al estado de inicio
                cad2=cad2+"/"+c # agregamos el / que nos saltamos en el tado A
        elif (estado=="B"): #sabemos que estamos en el estado con comentarios
            if (c=="*"): # hasta que no encontremos un * no meteremos nada a cad2
                estado = "C" #encontramos el * PUEDE que termine el comentario
        elif(estado=="C"): #Estado donde PUEDE terminar elcometario
            if (c=="/"): # si encontramos / ha terminado el comentario
                estado="Z" #volvemos al estado de incio, Z
            else: # de no ser asi el comentario continua 
                estado="B" #volvemos al estado B donde sigue siendo un comentario
    return cad2

"""
Esta función servirá para empezar a separar por tokens nuestro codigo ya sin
comentarios
"""
def tokeniza(cad):
    tokens = [] #Creamos un array donde metermos nuestros tokens
    dentro = False #variable que usaremos en caso que no sean un simEspecial
                    #es posible que sea un id, palabra reservada o un tipo
    token = "" #variable donde guardaremos los casos anteriormente mencionados
    for c in cad: 
        if dentro:  # es un caso de los anteriores mencionados
            """
            Esta funcion es en caso que no sea un simbolo especial, significa
            que puede ser o un id, palabra reservada o un tipo, sabemos que
            estos tokens acaban cuando hay un espacio, el primer if se encarga
            de ello, cuando encuentre un espacio meteremos nuestra variable
            temporal y meteremos lo que almacenos ahi en el array, de igual
            manera pasará si encontramos un caracter especial, mientras no pase
            eso, todo lo que encontremos irá a la variable temporal
            """
            if esSeparador(c): 
                tokens.append(token)
                token = ""
                dentro = False
            elif esSimboloEsp(c):
                tokens.append(token)
                tokens.append(c)
                token = ""
                dentro = False
            else:
                token = token + c
        else: #Iniciamos con este, ya que dentro por defecto es falso
            if esSimboloEsp(c): #si es un simbolo especial lo mete al Array
                tokens.append(c)
            elif esSeparador(c): # si es un separador no hace nada
                a=0
            else:
                dentro = True # de no ser alguna de las anteriores lo manda
                            # a la funcion para meter el conjuto en un token
                token = c
    return tokens

"""
Esta funcion nos servirá para saber si es un ID
"""
def esId(cad):
    return (cad[0] in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

"""
Esta funcion nos servirá para saber si es una palabra reservada
"""
def esPalReservada(cad):
    reservadas = ["main","char", "int","float","double","if","else","do",
                  "while","for","switch","short","long","extern", "static",
                  "default","continue","break","register","sizeof","typedef"]
    return cad in reservadas

"""
Esta funcion nos servirá para ver si es un tipo de cadena
"""
def esTipo(cad):
    tipos=["int", "char", "float", "double"]
    return cad in tipos







# Programa para probar las funciones
codigo_prueba = """
/* Este es un comentario */

int main() {
    /* Declaración de variables */
    float var1 = 3.14;
    char char1 = 'a';
    
    /* Estructuras de control */
    if (var1 > 0) {
        print("La variable 'var1' es mayor que 0\n");
        return 1;
    } else {
        print("La variable 'var1' no es mayor que 0\n");
        return 0;
    }
}
"""

# Prueba de las funciones
print("Código prueba:")
print(codigo_prueba)

print("Resultado después de quitar comentarios:")
codigo_sin_comentarios = quitaComentarios(codigo_prueba)
print(codigo_sin_comentarios)

print("Tokens resultantes:")
tokens_resultantes = tokeniza(codigo_sin_comentarios)
print(tokens_resultantes)

print("Pruebas de identificadores, palabras reservadas y tipos:")
for token in tokens_resultantes:
    if esPalReservada(token):
        print(token + " es una palabra reservada.")
    elif esTipo(token):
        print(token + " es un tipo de dato.")
    elif esSimboloEsp(token):
        print(token + " es un simbolo especial.") 
    else:
        print(token + " es un identificador.")

