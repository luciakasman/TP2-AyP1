import csv
import random
import argparse

def leer_linea_de_comandos ():
	'''Lee los parámetros de la linea de comandos y devuelve True si se escribió "-s", False de lo contrario''' 

	parser = argparse.ArgumentParser(description = 'Generador de crucigramas')

	parser.add_argument('-s', '--solucion', action = 'store_true', help = 'imprimir la solución')
	
	args = parser.parse_args()

	return args.solucion 		# es True si el usuario incluyó la opción -s


def filas_desde_horizontal (palabras_verticales):
	'''Cuenta la cantidad de filas desde la palabra horizontal hasta el fin del crucigrama'''

	cant_filas = 0

	for palabra in palabras_verticales:

		if len(palabra[0]) - palabra[2] > cant_filas:

			cant_filas = len(palabra[0]) - palabra[2]

	return cant_filas


def filas_hasta_horizontal (palabras_verticales):
	'''Cuenta la cantidad de filas que hay hasta la palabra horizontal'''

	numero_mas_alto = 0

	for palabra in palabras_verticales:

		if palabra[2] > numero_mas_alto:

			numero_mas_alto = palabra[2]

	return numero_mas_alto


def armar_crucigrama (horizontal, palabras_verticales, imprimir_solucion):
	'''Arma el crucigrama sin ocultar las letras, es decir, la solución del mismo'''

	numero_de_fila_crucigrama = 0

	nro_filas_arriba = filas_hasta_horizontal (palabras_verticales)

	nro_filas_abajo = filas_desde_horizontal (palabras_verticales)

	numero_de_linea = nro_filas_arriba

	crucigrama = []

	linea_de_crucigrama = []

	while numero_de_fila_crucigrama < nro_filas_abajo + nro_filas_arriba:

		numero_de_columna_crucigrama = 0

		while numero_de_columna_crucigrama < len(horizontal[0]):

			if numero_de_linea == 0:

						linea_de_crucigrama.append(horizontal[0][numero_de_columna_crucigrama])
			else: 

				if numero_de_columna_crucigrama % 2 == 0:

					nro_linea_donde_cruza_palabra = palabras_verticales[int(numero_de_columna_crucigrama / 2)][2]
						
					numero_fila = nro_linea_donde_cruza_palabra - numero_de_linea

					if numero_fila < 0:

						linea_de_crucigrama.append(" ")

					elif numero_fila >= len(palabras_verticales[int(numero_de_columna_crucigrama / 2)][0]):

						linea_de_crucigrama.append(" ")

					else: 

						linea_de_crucigrama.append(palabras_verticales[int(numero_de_columna_crucigrama / 2)][0][numero_fila])

				else:

					linea_de_crucigrama.append(" ")

			numero_de_columna_crucigrama += 1

		numero_de_linea -= 1

		numero_de_fila_crucigrama += 1

		crucigrama.append(linea_de_crucigrama)

		linea_de_crucigrama = []


	crucigrama_sin_sol = armar_crucigrama_sin_sol (crucigrama)

	if imprimir_solucion:
		
		imprimir_crucigrama (crucigrama_sin_sol, nro_filas_arriba)

		print()
	
		imprimir_definiciones (horizontal, palabras_verticales)

		print()

		print("SOLUCION")

		print()

		imprimir_crucigrama (crucigrama, nro_filas_arriba)

	else:

		imprimir_crucigrama (crucigrama_sin_sol, nro_filas_arriba)

		print()
	
		imprimir_definiciones (horizontal, palabras_verticales)



def armar_crucigrama_sin_sol (crucigrama):
	'''Arma el crucigrama ocultando las letras'''

	crucigrama_sin_sol = []
	fila_crucigrama_sin_sol = []

	for fila in crucigrama:

		for elemento in fila: 

			if elemento.isalpha():

				fila_crucigrama_sin_sol.append(".")

			else:

				fila_crucigrama_sin_sol.append(elemento)

		crucigrama_sin_sol.append(fila_crucigrama_sin_sol)

		fila_crucigrama_sin_sol = []

	return crucigrama_sin_sol


def imprimir_crucigrama (crucigrama, nro_filas_arriba):
	'''Imprime el crucigrama'''

	print("    ", end = "")

	for cant_palabras in range(len(crucigrama[0])):

		if cant_palabras % 2 == 0:

			print(cant_palabras//2, end = "   ")

	print()

	print()

	for cant_filas, fila in enumerate(crucigrama):

		if  cant_filas == nro_filas_arriba:

			print("H",end = "   ")
		else:
			print(" ", end = "   ")

		for elemento in fila:		
		
			print(elemento, end=" ")
		
		print()


def imprimir_definiciones (horizontal, palabras_verticales):
	'''Imprime las definiciones de las palabras utilizadas en el crucigrama'''

	print("DEFINICIONES")

	print()

	print("H. {}".format(horizontal[1]))

	for cant_palabras, palabra in enumerate(palabras_verticales):

		print("{}. {}".format(cant_palabras, palabra[1]))


def crear_matriz (cant_cols, cant_fils):
	'''Crea matriz de tamaño cant_fils por cant_cols y la llena con ceros'''

	matriz = []

	for i in range(cant_fils):

		matriz.append([0]*cant_cols)

	return matriz


def nro_letra_donde_cruzan (horizontal, palabras_verticales):

	for i, palabra_vert in enumerate(palabras_verticales):

		letra = horizontal[0][2*i]

		for j, letra_palabra_vert in enumerate(palabra_vert[0]):

			if letra == letra_palabra_vert:

				palabras_verticales[i]=(palabra_vert[0], palabra_vert[1], j)

				break

	return palabras_verticales


def linea_aleatoria (lector, archivo):
	'''Lee una linea aleatoria del archivo'''

	num_random = random.randrange(0, 17959)

	for i in range(num_random+1):

		linea_random = next(lector)

	archivo.seek(1)

	return linea_random

def leer_archivo (ruta):
	'''Lee el archivo y encuentra la palabra horizontal y todas las palabras verticales para armar el crucigrama'''

	palabras_verticales = []

	with open(ruta) as archivo:		

		lector = csv.reader(archivo, delimiter="|")
		
		horizontal = linea_aleatoria(lector,archivo)

		while len(horizontal[0]) < 8:

			horizontal = linea_aleatoria(lector,archivo) 

		for i in range(0,len(horizontal[0]),2):

			letra = horizontal[0][i] 

			linea = linea_aleatoria(lector, archivo)

			while not letra in linea[0] or linea[0] in palabras_verticales or linea[0] == horizontal:

				linea = linea_aleatoria(lector, archivo)

			palabras_verticales.append((linea[0], linea[1]))

	return horizontal, palabras_verticales


def main():

	horizontal, palabras_verticales = leer_archivo ("/home/luciakasman/Documentos/Algoritmos y Programación 1/TP2/palabras.csv")

	nro_letra_donde_cruzan(horizontal, palabras_verticales)

	imprimir_solucion = leer_linea_de_comandos()

	armar_crucigrama(horizontal, palabras_verticales, imprimir_solucion)

main ()
