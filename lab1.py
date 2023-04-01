CONVERSOR = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14,
    'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
    'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24,
    'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
    'U': 30, 'V': 31,
}


def leer_archivo(file):
    '''
    Esta función lee un archivo de texto y lo convierte en una lista de tuplas.
    Cada tupla contiene su base numerica y el numero.

    Parametros:
        file (str): nombre del archivo a leer.

    Retorno:
        lista_numeros (list): Lista de tuplas que contiene la base numerica de un numero y posiblemente el número en dicha base.
    '''
    with open(file, "r") as f:
        txt = f.read()

    txt = txt.strip()
    lista_info = (txt.replace("\n", "-")).split("-")
    lista_numeros = []
    for info in lista_info:
        base, numero = info.split(";")
        # Se hace esto para evitar usar el metodo int()
        base = num_decimal(10, base)
        lista_numeros.append((base, numero))
    return lista_numeros


def leer_errores(file, size_n):
    '''
    Esta función lee un archivo de texto y verifica si el tamaño de los números almacenados es mayor a size_n.

    Parametros:
        file (str): nombre del archivo a leer.
        size_n (int): número que se compara con el tamaño de los números almacenados en el archivo.

    Retorno:
        (bool): True si la suma de los números almacenados en el archivo es mayor o igual a size_n. False en caso contrario.
    '''
    with open(file, 'r') as f:
        txt = f.readlines()
    suma = 0
    for i in txt:
        error = i.replace('\n', "").split(", ")
        for j in error[1:]:
            suma += num_decimal(10, j)
    return (suma > size_n)


def escribir_archivo(file, result):
    '''
    Esta función escribe sobre un archivo de texto.

    Parametros:
        file (str): nombre del archivo en el que se escribirá texto result.
        result (str): cadena de texto que se escribirá en el archivo.

    Retorno:
        (void)
    '''
    with open(file, "a") as f:
        f.write(result + "\n")


def calcular_rango(lista_numeros, num_representables):
    '''
    Esta función recorre una lista de tuplas y verifica si el número es representable en la base de su misma tupla.
    En caso de ser representable se agrega la base y el numero a una lista vacia, si no es representable se agrega 0 y el numero.
    Por cada numero no representable se suma 1 al error_numerico.

    Parametros:
        lista_numeros (list): lista de tuplas con los elementos.
        num_representables (list): lista vacía en la que se almacenarán las tuplas de los números representables.

    Retorno:
        error_numerico (int): número de tuplas las cuales no son representables de acuerdo a su base.
    '''
    error_numerico = 0
    for base, numero in lista_numeros:
        representable = True
        for digito in numero:
            if CONVERSOR[digito] >= base:
                error_numerico += 1
                representable = False
                num_representables.append((0, numero))
                break
        if representable:
            num_representables.append((base, numero))

    return error_numerico


def calcular_valores(lista_numeros: list, rango: int):
    '''
    Esta función calcula, la cantidad de numeros de lista_numeros, los errores numericos, los errores en tamaño,
    y la cantidad de sumas que provocan overflow en complemento a 2.
    Esto lo hace con la ayuda de diversas funciones las cuales permiten realizar este procedimiento.
    Ciertos numeros se agregan con -1 unicamente para saber que están mal y poder ocuparlos para no alterar el orden la suma_overflow.

    Parametros:
        lista_numeros (list): lista de tuplas con los elementos.
        rango (int): cantidad de bits totales que se permiten.

    Retorno:
        (string): Devuelve un string el cual contiene lo siguiente:
            size_n (int): cantidad de tuplas en la lista lista_numeros.
            error_numerico (int): cantidad de dígitos no representables.
            error_size (int): cantidad de números que superan la cantidad de bits permitidos.
            error_overflow (int): cantidad de sumas que provocan overflow.
    '''
    size_n = len(lista_numeros)
    num_representables = []
    error_numerico = calcular_rango(lista_numeros, num_representables)

    num_representables = base_to_binario(num_representables, rango)
    print(num_representables)
    error_size = 0
    error_overflow = 0
    sum_values = []

    for num_binario in num_representables:
        if len(num_binario) > rango and num_binario != "-1":
            error_size += 1
            sum_values.append("-1")
        else:
            sum_values.append(num_binario)
        if (len(sum_values) == 2):
            error_overflow += suma_overflow(sum_values)
            sum_values = []

    return f"{size_n}, {error_numerico}, {error_size}, {error_overflow}"


def suma_overflow(num_representables):
    '''
    Esta función recibe una lista de dos números binarios.
    Devuelve 1 si la suma de estos números en complemento a 2 provoca un overflow, en caso contrario devuelve 0.

    Parametros:
        num_representables (list): lista de dos números binarios.

    Retorno:
        (int): retorna 1 si provoca overflow, 0 en caso de que no lo haga.
    '''
    if "-1" in num_representables:
        return 0
    else:
        resultado = ""
        num1 = num_representables[0]
        num1 = num1[::-1]
        num2 = num_representables[1]
        num2 = num2[::-1]

        carry_salida = 0
        carry_entrada = 0
        for i in range(0, len(num1)):
            sum = CONVERSOR[num1[i]] + CONVERSOR[num2[i]]
            carry_entrada = carry_salida
            resultado = f"{(sum+carry_entrada)%2}" + resultado
            carry_salida = (sum + carry_entrada)// 2

        resultado = resultado[len(resultado) - len(num1):]
        if carry_salida != carry_entrada:
            return 1
        else:
            return 0



def base_to_binario(num_representables, rango):
    '''
    Convierte un número en una base determinada a binario.
    Esto lo hace con la ayuda de la funcion num_decimal, la cual permite obtener el valor decimal de ese numero.
    Mediante el numero decimal se obtiene el numero binario con una extension de signo.

    Parametros:
        num_representables (list): lista de tuplas las cuales se quiere convertir el valor del numero a binario.
        rango (int): Rango de bits maximo permitido.

    Retorno:
        lista_num_binario (list): Lista de todos los numeros convertidos a binarios
    '''
    lista_num_binario = []
    for base, numero in num_representables:
        if base != 0:
            num = num_decimal(base, numero)

            num_binario = ""
            while num != 0:
                num_binario = str(num % 2) + num_binario
                num = num // 2

            if len(num_binario) < rango:
                num_binario = (
                    f"{num_binario[0]}" *
                    (rango - len(num_binario)) + num_binario
                )
            lista_num_binario.append(num_binario)
        else:
            lista_num_binario.append("-1")

    return lista_num_binario


def num_decimal(base, numero):
    '''
    Convierte un número en una base determinada a decimal.

    Parametros:
        base (int): La base en la que se encuentra el número.
        numero (str): El número en la base dada.

    Retorno:
        num (int): El número convertido a base decimal.
    '''
    num = 0
    digitos = list(numero)
    digitos.reverse()
    for i, digito in enumerate(digitos):
        num += (base**i) * CONVERSOR[digito]
    return num


def main():
    '''
    Funcion main encargada de ejecutar de forma correcta el programa.
    Se encarga de llamar a las distintas funciones del programa.
    Mediante un ciclo while va recibiendo un input por parte del usuario, si el usuario ingresa 0
    y la cantidad de errores es mayor al numero de tuplas, el programa se detiene.

    Parametros:
        No posee parametros

    Retorno:
        (void)
    '''
    rango = 1
    numeros = leer_archivo("numeros.txt")
    while rango != 0:
        rango = num_decimal(10, input("Ingresa el tamaño del registro: "))

        if rango == 0:
            if leer_errores("resultado.txt", len(numeros)):
                break
            else:
                rango = 1
                continue

        resultado = calcular_valores(numeros, rango)
        escribir_archivo("resultado.txt", resultado)


main()
