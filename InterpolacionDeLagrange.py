# Jeferson Alexis Suchite Chávez 
# 0909-22-12681

import matplotlib.pyplot as plt
import numpy as np

# Función para expandir el numerador del polinomio L_i(x)
def expandir_numerador(puntos, i):
    n = len(puntos)
    coeficientes = np.zeros(n)
    coeficientes[0] = 1  # Inicia el primer coeficiente en 1

    # Construye el numerador expandiendo el producto (x - x_j)
    for j in range(n):
        if i != j:
            for k in range(n-1, 0, -1):
                coeficientes[k] = coeficientes[k] * -puntos[j][0] + (coeficientes[k-1] if k > 0 else 0)
            coeficientes[0] *= -puntos[j][0]

    # Crea una lista de términos no nulos del numerador
    expandido = []
    for k in range(n-1, -1, -1):
        if coeficientes[k] != 0:
            expandido.append(f"{coeficientes[k]:.1f}x^{k}")

    return " + ".join(expandido)  # Retorna el numerador como una cadena de texto

# Función para escalar el numerador del polinomio L_i(x) por el denominador
def escalar_numerador(numerador_expandido, denominador):
    terminos = numerador_expandido.split(" + ")  # Separa los términos del numerador
    escalado = []

    # Escala cada término del numerador por el denominador
    for termino in terminos:
        if "x^" in termino:
            coef = float(termino.split("x^")[0].strip())  # Extrae el coeficiente
            potencia = int(termino.split("x^")[1])  # Extrae la potencia de x
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}x^{potencia}")
        else:
            coef = float(termino.split("x")[0].strip())  # Extrae el coeficiente
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}")

    return " + ".join(escalado)  # Retorna el numerador escalado como una cadena de texto

# Función para realizar la interpolación de Lagrange
def interpolacion_lagrange(puntos_x, puntos_y):
    def L(k, x):
        termino = 1
        for i in range(len(puntos_x)):
            if i != k:
                termino *= (x - puntos_x[i]) / (puntos_x[k] - puntos_x[i])
        return termino

    def P(x):
        polinomio = 0
        for k in range(len(puntos_x)):
            polinomio += puntos_y[k] * L(k, x)
        return polinomio

    valores_x = np.linspace(min(puntos_x) - 1, max(puntos_x) + 1, 1000)  # Valores de x para graficar
    valores_y = [P(x) for x in valores_x]  # Evalúa P(x) para cada valor de x

    return P, valores_x, valores_y  # Retorna la función P(x) y los valores calculados

# Función para imprimir los polinomios individuales de Lagrange
def imprimir_polinomios_lagrange(puntos_x, puntos_y):
    n = len(puntos_x)
    puntos = list(zip(puntos_x, puntos_y))  # Crea una lista de puntos (x, y)

    P_str = "Polinomios individuales L_i(x):\n"
    for i in range(n):
        numerador, denominador = expandir_numerador(puntos, i), 1  # Expande el numerador y calcula el denominador
        for j in range(n):
            if j != i:
                denominador *= (puntos_x[i] - puntos_x[j])  # Calcula el denominador del polinomio L_i(x)
        numerador_escalado = escalar_numerador(numerador, denominador)  # Escala el numerador por el denominador

        if i > 0:
            P_str += "\n"
        P_str += f"L{i}(x):\n"
        P_str += f"L{i}(x) = ({numerador}) / ({denominador})\n"  # Muestra el polinomio L_i(x)
        P_str += f"L{i}(x) = {numerador_escalado}\n"  # Muestra el polinomio L_i(x) escalado

    print(P_str)  # Imprime todos los polinomios individuales L_i(x)

def main():
    num_puntos = int(input("Ingresa la cantidad de puntos (3 o 4): "))  # Ingresa la cantidad de puntos a interpolar
    puntos_x = []
    puntos_y = []

    print("Ingresa los puntos (x, y) uno por uno:")
    for i in range(num_puntos):
        x = float(input(f"Punto {i + 1} - x: "))  # Ingresa el valor de x
        y = float(input(f"Punto {i + 1} - y: "))  # Ingresa el valor de y
        puntos_x.append(x)  # Agrega x a la lista de puntos_x
        puntos_y.append(y)  # Agrega y a la lista de puntos_y

    print("\nPolinomios de Lagrange:")
    for i in range(num_puntos):
        print(f"I[{i}]: ({puntos_x[i]}, {puntos_y[i]})")  # Muestra los puntos ingresados

    # Interpolación de Lagrange
    P, valores_x, valores_y = interpolacion_lagrange(puntos_x, puntos_y)

    # Imprimir polinomios individuales de Lagrange
    imprimir_polinomios_lagrange(puntos_x, puntos_y)

    # Evaluación del polinomio en puntos específicos
    valores_x_evaluados = np.arange(-10, 10.5, 0.5)  # Valores de x para evaluar P(x)
    valores_y_evaluados = []

    print("\nValores de P(x) para los puntos evaluados:")
    for x in valores_x_evaluados:
        resultado = P(x)  # Evalúa P(x) en cada valor de x
        valores_y_evaluados.append(resultado)  # Agrega el resultado a la lista de valores y evaluados
        print(f"P({x:.1f}) = {resultado:.6f}")  # Imprime el resultado de P(x)

    # Graficar los resultados
    plt.plot(valores_x, valores_y, label='Polinomio Interpolante')  # Grafica el polinomio interpolante
    plt.scatter(puntos_x, puntos_y, color='red', s=100, label='Puntos de Datos')  # Grafica los puntos de datos

    # Agregar etiquetas de coordenadas a los puntos de datos
    for (x, y) in zip(puntos_x, puntos_y):
        plt.text(x, y, f'({x}, {y})', fontsize=15, ha='center', va='bottom')

    plt.scatter(valores_x_evaluados, valores_y_evaluados, color='green', label='Puntos Evaluados')  # Grafica los puntos evaluados
    plt.axhline(0, color='black', linewidth=1.5)  # Línea horizontal en y=0 más oscura
    plt.axvline(0, color='black', linewidth=1.5)  # Línea vertical en x=0 más oscura
    plt.xlabel('x')  # Etiqueta del eje x
    plt.ylabel('P(x)')  # Etiqueta del eje y
    plt.legend()  # Muestra la leyenda
    plt.title('Polinomio de Interpolación de Lagrange')  # Título del gráfico
    plt.grid(True)  # Activa la cuadrícula en el gráfico
    plt.show()  # Muestra el gráfico

if __name__ == "__main__":
    main()  # Llama a la función principal al ejecutar el script
