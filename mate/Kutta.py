import numpy as np
import matplotlib.pyplot as plt

class MetodoRungeKutta:
    def resolver(self, f, x0, y0, h, intervalo):
        series = []

        x = x0
        y = y0

        print("Método de Runge-Kutta")
        print("x\t\ty\t\tk1\t\tk2\t\tk3\t\tk4")

        epsilon = 1e-10

        # Imprimir los valores iniciales
        print(f"{x:.4f}\t\t{y:.4f}")

        while x + epsilon < intervalo:
            series.append((x, y))

            k1 = h * f(x, y)
            k2 = h * f(x + h / 2.0, y + k1 / 2.0)
            k3 = h * f(x + h / 2.0, y + k2 / 2.0)
            k4 = h * f(x + h, y + k3)

            y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            x = x + h

            # Imprimir los valores formateados en la consola
            print(f"{x:.4f}\t\t{y:.4f}\t\t{k1:.4f}\t\t{k2:.4f}\t\t{k3:.4f}\t\t{k4:.4f}")

        # Agregar el último valor del intervalo a la serie
        series.append((intervalo, y))

        return series

def ejemplo_funcion(x, y):
    return x * y  # Cambia esta función por la que necesitas resolver

if __name__ == "__main__":
    runge_kutta = MetodoRungeKutta()
    intervalo = 2.0  # Cambia el intervalo según tus necesidades
    h = 0.1  # Cambia el tamaño del paso h según tus necesidades

    series = runge_kutta.resolver(ejemplo_funcion, 0.0, 1.0, h, intervalo)

    x_values, y_values = zip(*series)
    plt.plot(x_values, y_values, label="Solución numérica (Runge-Kutta)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()