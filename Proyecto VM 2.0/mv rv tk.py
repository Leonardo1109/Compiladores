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
    cadena = cadena.replace(',', ' ,') # Reemplaza las comas por un espacio seguido de una coma
    tokens = cadena.split() # Divide la cadena por espacios y devuelve la lista de tokens
    return tokens

# Lista que se utiliza para almacenar las instrucciones del programa
instrucciones = []
varPC = [0] # Lista para obtener en donde nos encontramos

# Definir la interfaz gráfica principal de la aplicación.
class Interfaz:
    def __init__(self, master):
        self.master = master
        self.master.title("Interprete de Ensamblador RISC-V")

        # Botón para cargar el programa
        self.boton_cargar = tk.Button(master, text="Cargar Programa", command=self.cargar_programa)
        self.boton_cargar.pack()

        # Botón para correr el programa
        self.boton_correr = tk.Button(master, text="Correr Programa", command=self.correr_programa)
        self.boton_correr.pack()

        # Botón para ejecutar paso a paso
        self.boton_paso_a_paso = tk.Button(master, text="Ejecutar Paso a Paso", command=self.ejecutar_paso_a_paso)
        self.boton_paso_a_paso.pack()

        # Botón para ejecutar paso a paso
        self.reinicio = tk.Button(master, text="Reinicio", command=self.reinicio)
        self.reinicio.pack()

        # Contador de programa
        self.contador_programa = tk.Label(master, text="Contador de Programa: 0")
        self.contador_programa.pack()

        # Registros
        self.valores_registros = [0 for _ in range(32)]
        self.registros = [tk.Label(master, text=f"Registro {i}: {self.valores_registros[i]}") for i in range(32)]
        for registro in self.registros:
            registro.pack()

    
    # Funcion que se encarga de cargar un programa desde un archivo seleccionado por el usuario
    def cargar_programa(self):
        filename = filedialog.askopenfilename() # Abre un cuadro de diálogo para que el usuario seleccione un archivo
        print(f'Programa cargado: {filename}') # Imprime un mensaje indicando que el programa ha sido cargado con éxito
        arch = open(filename, 'r')
        for ren in arch:
            if len(ren)>2: # Verifica si la longitud de la línea es mayor a 2 para asegurarse de que no esté vacía o sea un comentario
                datos = tokenizar(ren) # Tokeniza la línea y agrega los tokens a la lista de instrucciones
                instrucciones.append(datos)
        arch.close() # Cierra el archivo después de leerlo
        self.etiquetas = [] # Inicializa una lista vacía para almacenar etiquetas
        for c in range(len(instrucciones)): # Itera sobre el número de instrucciones en la lista de instrucciones
            if instrucciones[c][0] == '%': # Verifica si la primera parte de la instrucción es una etiqueta
                self.etiquetas.append(Etiqueta(instrucciones[c][1], c))

    #  Esta funcion recibe el nombre de una etiqueta como argumento y devuelve la línea correspondiente donde se encuentra esa etiqueta en el programa
    def get_dir_etiqueta(self, etq):
        direccion = -1
        for e in self.etiquetas: # Itera sobre cada etiqueta en la lista de etiquetas
            if e.nombre == etq: # Verifica si el nombre de la etiqueta coincide con la etiqueta proporcionada
                return e.linea # Retorna el número de línea asociado a la etiqueta
        return direccion # Retorna -1 si la etiqueta no se encuentra

    # Funcion para correr el programa
    def correr_programa(self):
        pc = 0 # Inicializa el contador de programa en 0
        print('Corriendo programa...')
        while instrucciones[pc][0]!='END': # Mientras no se encuentre la instrucción 'END'
            inst = instrucciones[pc] # Obtiene la instrucción actual
            print(pc, self.valores_registros[2], inst) # Imprime información de depuración
            # Si es una instrucción de suma inmediata
            if inst[0]=='ADDI':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5])
                self.valores_registros[destino] = self.valores_registros[reg1] + numero
                pc = pc + 1
            # Si es una etiqueta, avanza al siguiente paso
            elif inst[0] == '%':
                pc = pc + 1
            # Si es una instrucción de salto
            elif inst[0] == 'J':
                etq = inst[1]
                pc = self.get_dir_etiqueta(etq)
                print('saltando a', pc)
            # Si es una instrucción de comparación mayor o igual
            elif inst[0] == 'BGE':
                op1 = self.valores_registros[int(inst[1][1:])]
                num = int(inst[3])
                etq = inst[5]
                print('comparando ' , op1, 'con', num)
                if op1 >= num:
                    pc = self.get_dir_etiqueta(etq)
                else:
                    pc = pc + 1
            # Si es una instrucción de suma
            elif inst[0] == 'ADD':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5][1:])
                self.valores_registros[destino] = self.valores_registros[reg1] + self.valores_registros[numero]
                pc = pc + 1
            # Si es una instrucción de resta
            elif inst[0] == 'SUB':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5][1:])
                self.valores_registros[destino] = self.valores_registros[reg1] - self.valores_registros[numero]
                pc = pc + 1
            # Si es una instrucción de resta inmediata
            elif inst[0] == 'SUBI':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5])
                self.valores_registros[destino] = self.valores_registros[reg1] - numero
                pc = pc + 1
            # Si es una instrucción de multiplicación
            elif inst[0] == 'MUL':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5][1:])
                self.valores_registros[destino] = self.valores_registros[reg1] * self.valores_registros[numero]
                pc = pc + 1
            # Si es una instrucción de multiplicación inmediata
            elif inst[0] == 'MULI':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5])
                self.valores_registros[destino] = self.valores_registros[reg1] * numero
                pc = pc + 1
            # Si es una instrucción de división
            elif inst[0] == 'DIV':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5][1:])
                self.valores_registros[destino] = int(self.valores_registros[reg1] / self.valores_registros[numero])
                pc = pc + 1
            # Si es una instrucción de división inmediata
            elif inst[0] == 'DIVI':
                destino = int(inst[1][1:])
                reg1 = int(inst[3][1:])
                numero = int(inst[5])
                self.valores_registros[destino] = int(self.valores_registros[reg1] / numero)
                pc = pc + 1
            # Almacenar valores en un registro
            elif inst[0] == 'LI':
                destino = int(inst[1][1:])
                numero = int(inst[3])
                self.valores_registros[destino] = numero
                pc = pc + 1
            self.actualizar_registros(pc)
            varPC[0] = pc # almacenando pc para saber donde nos encontramos
            print(varPC)
            

    # Método para ejecutar el programa paso a paso
    def ejecutar_paso_a_paso(self):
        print('Ejecutando paso a paso...')
        
        self.actualizar_registros()

    # Método para reiniciar
    def reinicio(self):
        global instrucciones
        instrucciones = []
        self.valores_registros = [0 for _ in range(32)]
        self.actualizar_registros(0)
        print("Programa reiniciado")

    # Método para actualizar la interfaz con los valores de los registros
    def actualizar_registros(self, pc):
        self.contador_programa.config(text="Contador de Programa: " + str(pc)) # Cambia el valor de Pc en donde se esta quedando (acutalizando pc)
        for i in range(32): # Itera sobre los registros y actualiza el texto de los labels con los nuevos valores
            self.registros[i].config(text=f"Registro {i}: {self.valores_registros[i]}")

# Inicialización de la ventana principal de la interfaz gráfica
root = tk.Tk()
# Crea una instancia de la clase Interfaz pasando la ventana principal como argumento
root.geometry("300x900")
app = Interfaz(root)
# Inicia el bucle principal de eventos de la interfaz gráfica
root.mainloop()
