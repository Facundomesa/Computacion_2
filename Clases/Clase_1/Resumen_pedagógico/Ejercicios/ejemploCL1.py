#import getopt
#import sys

#def main():
#    try:
        # Parsear los argumentos
 #       opts, args = getopt.getopt(sys.argv[1:], "i:v", ["input=", "verbose"])

  #      input_file = None
   #     verbose = False

    #    for opt, arg in opts:
    #        if opt in ("-i", "--input"):
    #            input_file = arg
    #        elif opt in ("-v", "--verbose"):
    #            verbose = True

        # Verificar que se haya pasado un archivo de entrada
    #    if not input_file:
    #        print("Error: Debes proporcionar un archivo de entrada.")
    #        sys.exit(1)

    #    print(f"Archivo de entrada: {input_file}")
    #    if verbose:
    #        print("Modo verbose activado.")

    #except getopt.GetoptError as err:
    #    print(str(err))
    #    sys.exit(2)

#if __name__ == "__main__":
#    main()


#import argparse

#def main():
#    # Crear el analizador de argumentos
#    parser = argparse.ArgumentParser(description="Un script para procesar archivos de entrada.")
    
    # Definir los argumentos
#    parser.add_argument("-i", "--input", required=True, help="Archivo de entrada")
#    parser.add_argument("-v", "--verbose", action="store_true", help="Activar el modo verbose")

    # Parsear los argumentos
#    args = parser.parse_args()

    # Mostrar los resultados
#    print(f"Archivo de entrada: {args.input}")
#    if args.verbose:
#        print("Modo verbose activado.")

#if __name__ == "__main__":
#    main()


#import argparse

#def main():
    # Crear el analizador de argumentos
#    parser = argparse.ArgumentParser(description="Un script para procesar archivos de entrada y salida.")

    # Definir los argumentos
#    parser.add_argument("--input", required=True, help="Archivo de entrada")  # Argumento obligatorio
#    parser.add_argument("--output", default="salida.txt", help="Archivo de salida (por defecto 'salida.txt')")  # Argumento opcional con valor por defecto
#    parser.add_argument("--verbose", action="store_true", help="Activar el modo verbose (opcional)")  # Argumento opcional de bandera

    # Parsear los argumentos
#    args = parser.parse_args()

    # Mostrar los resultados
#    print(f"Archivo de entrada: {args.input}")
#    print(f"Archivo de salida: {args.output}")
#    if args.verbose:
#        print("Modo verbose activado.")

#if __name__ == "__main__":
#    main()


import argparse

def main():
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description="Script que procesa diferentes tipos de datos.")

    # Argumento entero
    parser.add_argument("--num", type=int, help="Número entero (por defecto es 10)", default=10)

    # Argumento lista
    parser.add_argument("--list", type=int, nargs='+', help="Lista de números enteros")

    # Parsear los argumentos
    args = parser.parse_args()

    # Mostrar los resultados
    print(f"Número proporcionado: {args.num}")
    if args.list:
        print(f"Lista de números: {args.list}")

if __name__ == "__main__":
    main()
