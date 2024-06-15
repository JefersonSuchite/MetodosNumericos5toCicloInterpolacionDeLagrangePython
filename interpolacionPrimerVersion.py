import numpy as np
import matplotlib.pyplot as plt

def main():
    # Ingresar la cantidad de puntos
    print("Ingresa la cantidad de puntos (3 o 4): ")
    n = int(input())

    puntos = np.zeros((n, 2))

    # Ingresar los puntos
    print("Ingresa los puntos (x, y) uno por uno:")
    for i in range(n):
        print(f"Punto {i + 1} - x: ", end='')
        puntos[i][0] = float(input())
        print(f"Punto {i + 1} - y: ", end='')
        puntos[i][1] = float(input())

    # Mostrar los puntos ingresados
    print("\nPolinomios de Lagrange:\n")
    for i in range(n):
        print(f"I[{i}]: ({puntos[i][0]:.1f}, {puntos[i][1]:.1f})")

    # Valores de x donde se evaluará el polinomio
    valores_x = np.array([-10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5,
                         -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, 0, 1, 1.5,
                         2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])

    # Evaluar el polinomio en cada valor de x
    resultados = []
    for x in valores_x:
        print(f"\nx = {x:.1f}\n\n")
        print("Construcción del polinomio interpolado P(x):\n")

        polinomio = []
        for i in range(n):
            termino = puntos[i][1]
            terminos_builder = []
            
            for j in range(n):
                if i != j:
                    if puntos[j][0] < 0:
                        terminos_builder.append(f"(x + {-puntos[j][0]:.1f})")
                    else:
                        terminos_builder.append(f"(x - {puntos[j][0]:.1f})")
            
            polinomio.append(f"{termino:.1f} * ({' * '.join(terminos_builder)})")

        print("P(x) = " + " + ".join(polinomio))

        # Evaluación paso a paso
        print("\nPaso a paso:\n")
        for i in range(n):
            termino = puntos[i][1]
            terminos_builder = []

            for j in range(n):
                if i != j:
                    if puntos[j][0] < 0:
                        terminos_builder.append(f"(x + {-puntos[j][0]:.1f})")
                    else:
                        terminos_builder.append(f"(x - {puntos[j][0]:.1f})")
            
            print(f"f(x{i})L{i}(x):")
            print(f"{termino:.1f} * ({' * '.join(terminos_builder)})")

        # Mostrar polinomios individuales L_i(x)
        print("\nPolinomios individuales L_i(x):")
        for i in range(n):
            print(f"\nL{i}(x):")
            numerador = []
            denominador = 1
            
            for j in range(n):
                if i != j:
                    numerador.append(f"(x - {puntos[j][0]:.1f})")
                    denominador *= (puntos[i][0] - puntos[j][0])
            
            numerador_str = " * ".join(numerador)
            print(f"L{i}(x) = ({numerador_str}) / ({denominador:.1f})")
            
            numerador_expandido = expandir_numerador(puntos, i)
            print(f"L{i}(x) = {numerador_expandido}")

            numerador_escalado = escalar_numerador(numerador_expandido, denominador)
            print(f"L{i}(x) = {numerador_escalado}")

        # Evaluación en x
        resultado = evaluar_polinomio_lagrange(x, puntos)
        resultados.append(resultado)
        print(f"\nEvaluación en x = {x:.1f}:")
        print(f"P({x:.1f}) = {resultado:.6f}")

    # Mostrar gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(valores_x, resultados, label='Polinomio Interpolado')
    plt.scatter(puntos[:, 0], puntos[:, 1], color='red', s=100, label='Puntos de Datos')
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(0, color='black', linewidth=1.5)
    plt.xlabel('x')
    plt.ylabel('P(x)')
    plt.legend()
    plt.title('Polinomio de Interpolación de Lagrange')
    plt.grid(True)
    plt.show()

def evaluar_polinomio_lagrange(x, puntos):
    n = len(puntos)
    resultado = 0
    
    for i in range(n):
        termino = puntos[i][1]
        
        for j in range(n):
            if i != j:
                termino *= (x - puntos[j][0]) / (puntos[i][0] - puntos[j][0])
        
        resultado += termino
    
    return resultado

def expandir_numerador(puntos, i):
    n = len(puntos)
    coeficientes = np.zeros(n)
    coeficientes[0] = 1
    
    for j in range(n):
        if i != j:
            for k in range(n-1, 0, -1):
                coeficientes[k] = coeficientes[k] * -puntos[j][0] + (coeficientes[k-1] if k > 0 else 0)
            coeficientes[0] *= -puntos[j][0]
    
    expandido = []
    for k in range(n-1, -1, -1):
        if coeficientes[k] != 0:
            expandido.append(f"{coeficientes[k]:.1f}x^{k}")
    
    return " + ".join(expandido)

def escalar_numerador(numerador_expandido, denominador):
    terminos = numerador_expandido.split(" + ")
    escalado = []
    
    for termino in terminos:
        if "x^" in termino:
            coef = float(termino.split("x^")[0].strip())
            potencia = int(termino.split("x^")[1])
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}x^{potencia}")
        else:
            coef = float(termino.split("x")[0].strip())
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}")
    
    return " + ".join(escalado)

if __name__ == "__main__":
    main()
