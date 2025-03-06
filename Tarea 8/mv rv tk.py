# Importa la biblioteca tkinter para crear interfaces gráficas
# Importa el módulo filedialog de tkinter para manejar cuadros de diálogo de archivos
import tkinter as tk
from tkinter import filedialog

# Creamos la clase etiqueta para almacenar de mejor manera las etiquetas
class Etiqueta:
    def __init__(self, nombre, linea):
        self.nombre = nombre
        self.linea = linea

# Función para verificar si un caracter es un símbolo especial
def es_simbolo_esp(caracter):
    return caracter in "+-*;,.:!#=%&/(){}[]<><=>=="

# Función para verificar si un caracter es un separador
def es_separador(caracter):
    return caracter in " \n\t"

# Función para tokenizar una cadena y dividirla en tokens
def tokenizar(cadena):
    # Reemplaza las comas por un espacio seguido de una coma
    cadena = cadena.replace(',', ' ,')    
    # Divide la cadena por espacios y devuelve la lista de tokens
    tokens = cadena.split()
    return tokens

instrucciones = []


# Definición de la clase Interfaz para la GUI
class Interfaz:
    def __init__(self, master):
        self.master = master
        # Titulo del programa en la interfaz grafica
        self.master.title("Interprete de Ensamblador RISC-V")

        # Botón para cargar el programa usando la funcion "cargar_programa"
        self.boton_cargar = tk.Button(master, text="Cargar Programa", command=self.cargar_programa)
        self.boton_cargar.pack()

        # Botón para correr el programa usando la funcion "correr_programa"
        self.boton_correr = tk.Button(master, text="Correr Programa", command=self.correr_programa)
        self.boton_correr.pack()

        # Botón para ejecutar paso a paso usando la funcion "ejecutar_paso_a_paso"
        self.boton_paso_a_paso = tk.Button(master, text="Ejecutar Paso a Paso", command=self.ejecutar_paso_a_paso)
        self.boton_paso_a_paso.pack()

        # Contador de programa (PC) # REVISAR PUES NO FUNCIONA
        self.contador_programa = tk.Label(master, text="Contador de Programa: 0")
        self.contador_programa.pack()

        # Registros (mostrados en programa)
        self.valores_registros = [0 for _ in range(32)]
        self.registros = [tk.Label(master, text=f"Registro {i}: {self.valores_registros[i]}") for i in range(32)]
        for registro in self.registros:
            registro.pack()
    
    # Funcion para cargar un programa desde un archivo
    def cargar_programa(self):
        # Abre un cuadro de diálogo para que el usuario seleccione un archivo
        filename = filedialog.askopenfilename()
        # Imprime un mensaje indicando que el programa ha sido cargado con éxito
        print(f'Programa cargado: {filename}')
        # Abre el archivo en modo lectura
        arch = open(filename, 'r')
        # Recorre cada linea del archivo
        for ren in arch:
            # Verifica si la longitud es mayor a 2
            if len(ren)>2:
                # Tokeniza la línea y agrega los tokens a la lista de instrucciones
                datos = tokenizar(ren)
                instrucciones.append(datos)
        # Cierra el archivo después de leerlo
        arch.close()
        # Inicializa una lista vacía para almacenar etiquetas
        self.etiquetas = []
        # Itera sobre el número de instrucciones en la lista de instrucciones
        for c in range(len(instrucciones)):
            # Verifica si la primera parte de la instrucción es una etiqueta
            if instrucciones[c][0] == '%':
                # Agrega la etiqueta a la lista de etiquetas junto con su número de línea correspondiente
                self.etiquetas.append(Etiqueta(instrucciones[c][1], c))

    # Método para obtener la dirección de una etiqueta
    def get_dir_etiqueta(self, etq):
        # Inicializa la dirección como -1
        direccion = -1
        # Itera sobre cada etiqueta en la lista de etiquetas
        for e in self.etiquetas:
            # Verifica si el nombre de la etiqueta coincide con la etiqueta proporcionada
            if e.nombre == etq:
                # Retorna el número de línea asociado a la etiqueta
                return e.linea
        # Retorna -1 si la etiqueta no se encuentra
        return direccion

    # Método para correr el programa
    def correr_programa(self):
        # Inicializa el contador de programa en 0
        pc = 0
        print('Corriendo programa...')
        # Itera hasta encontrar la instrucción 'END'
        while instrucciones[pc][0]!='END':
            # Obtiene la fila actual
            inst = instrucciones[pc]
            # Imprime el arreglo en la posicion actual
            print(pc, self.valores_registros[2], inst)
            # Verifica si la primer instruccion es un ADDI
            if inst[0]=='ADDI':
                # Extraemos los valores necesarios de la instruccion para realizar una suma
                destino = int(inst[1][1:])# valor numerico del 2do elemento 
                reg1 = int(inst[3][1:] )# valor numerico del 4to elemento
                numero = int(inst[5])  # valor numerico del 6to elemento      
                # Realizamos la suma y actualizamos el registro destino
                self.valores_registros[destino] = self.valores_registros[reg1] + numero
                # incrementamos nuestro contador del programa
                pc = pc + 1
            # Si la instruccion comienza con '%' avanzamos e incrementamos PC
            elif inst[0] == '%':
                pc = pc + 1
            # Jump salta a la direccion indicada)            
            elif inst[0] == 'J': #Jump salta a la dirección indicada
                etq = inst[1]    # encontramos la etiqueta a donde saltar
                pc = self.get_dir_etiqueta(etq)  #buscamos la direccion en la tabla de etiquetas
                print('saltando a', pc)
            # Si la instruccion es una comparacion mayor o igual (BGE)
            elif inst[0] == 'BGE':
                # Extraemos los valores necesarios para la comparacion
                op1 = self.valores_registros[int(inst[1][1:])]
                num = int(inst[3])
                etq = inst[5]
                # Imprimimos los valores que estamos comparando
                print('comparando ' , op1, 'con', num)
                # Si la operacion es verdadera, saltamos a la etiqueta indicada
                if op1 >= num:
                    pc = self.get_dir_etiqueta(etq)
                # Si la operacion es falsa, simplemente avanzamos al siguiente paso
                else:
                    pc = pc + 1
            # Mandamos llamar a la funcion para que los registros se acutalicen, mandamos nuestro pc para solucionar el problema
            self.actualizar_registros(pc)

    # Método para ejecutar el programa paso a paso
    def ejecutar_paso_a_paso(self):
        print('Ejecutando paso a paso...')
        # Aquí puedes agregar el código para ejecutar tu programa paso a paso
        self.actualizar_registros()

    # Método para actualizar la interfaz con los valores de los registros
    def actualizar_registros(self, pc):
        # Cambia el valor de Pc en donde se esta quedando (acutalizando pc)
        self.contador_programa.config(text="Contador de Programa: " + str(pc))
        # Itera sobre los registros y actualiza el texto de los labels con los nuevos valores
        for i in range(32):
            self.registros[i].config(text=f"Registro {i}: {self.valores_registros[i]}")

# Inicialización de la ventana principal de la interfaz gráfica
root = tk.Tk()
# Crea una instancia de la clase Interfaz pasando la ventana principal como argumento
app = Interfaz(root)
# Inicia el bucle principal de eventos de la interfaz gráfica
root.mainloop()
