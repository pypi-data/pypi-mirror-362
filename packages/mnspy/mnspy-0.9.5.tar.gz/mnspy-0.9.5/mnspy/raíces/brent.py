from mnspy.raíces import Raices
import numpy as np
import matplotlib.pyplot as plt
import sys
plt.rcParams.update(plt.rcParamsDefault)

class Brent(Raices):
    """Clase para la implementación del cálculo de raíces por el método cerrado de Brent.

        Attributes
        ----------
        f: callable
            Función a la que se le hallará la raíz.
        x_min: float
            Límite inferior del intervalo de búsqueda.
        x_max: float
            Límite superior del intervalo de búsqueda.
        tol: float | int
            Máxima tolerancia del error.
        max_iter: int
            Número máximo de iteraciones permitido.
        tipo_error: str
            Tipo de error a utilizar para la convergencia:
            - ``'%'``: Error relativo porcentual.
            - ``'/'``: Error relativo.
            - ``'n'``: Número de cifras significativas.

        Methods
        -------
        _calcular():
            Realiza los cálculos iterativos del método de Brent.
        graficar(mostrar_sol: bool, mostrar_iter: bool, mostrar_lin_iter: bool, n_puntos: int):
            Genera una gráfica del proceso de búsqueda de la raíz.

        Examples
        -------
        import numpy as np

        def f(x):
            return (x ** 3 + 7 * x ** 2 - 40 * x - 100) / 50

        br = Brent(f, 0.0, 8.0, 0.0001, tipo_error="%")
        br.generar_tabla()
        br.graficar()
        br.solucion()
        """
    def __init__(self, f: callable, x_min: float = 0.0, x_max: float = 0.0, tol: float | int = 1e-3, max_iter: int = 20,
                 tipo_error='%'):
        """
        Constructor de la clase Brent.

        Parameters
        ----------
        f: callable
            Función a la que se le hallará la raíz.
        x_min: float
            Límite inferior del intervalo de búsqueda.
        x_max: float
            Límite superior del intervalo de búsqueda.
        tol: float | int
            Máxima tolerancia del error.
        max_iter: int
            Número máximo de iteraciones permitido.
        tipo_error: str
            Tipo de error a utilizar: ``'%'``, ``'/'`` o ``'n'``.
        """
        # Inicialización de la clase padre
        super().__init__(f, x_min, x_max, tol, max_iter, tipo_error)
        self._val = list([x_min, x_max])
        self._val_f = [self._f(x_min), self._f(x_max)]
        if np.sign(self._val_f[0]) == np.sign(self._val_f[1]):
            print(
                "No hay cambio de signo entre los límites. El método de Brent requiere que los límites tengan "
                "signos diferentes")
            sys.exit()
        # Se asegura que |f(a)| > |f(b)|
        if abs(self._f(x_min)) < abs(self._f(x_max)):
            self._val.reverse()
            self._val_f.reverse()
        self._val.append(self._val[0])
        self._val_f.append(self._val_f[0])
        self._biseccion_usada = True
        self._calcular()

    def _calcular(self):
        """Realiza los cálculos iterativos del método de Brent.

        Combina la interpolación cuadrática inversa, el método de la secante
        y el método de bisección para encontrar la raíz de manera eficiente y robusta.

        Returns
        -------
        None
        """
        # Verificación inicial
        if np.sign(self._val_f[0]) == np.sign(self._val_f[1]):
            print(
                "No hay cambio de signo entre los límites. El método de Brent requiere que los límites tengan "
                "signos diferentes")
            sys.exit()

        # Bucle de iteración para evitar recursión profunda
        while True:
            x_a, x_b, x_c = self._val
            y_a, y_b, y_c = self._val_f
            x_d = 0  # No se usa en la lógica actual, pero se mantiene por si se reimplementa una condición

            self._x_min = min([x_a, x_b])
            self._x_max = max([x_a, x_b])

            if len(self._val_f) == len(set(self._val_f)):
                # Si los valores de y son distintos, se usa interpolación cuadrática inversa
                self.x = (x_a * y_b * y_c / ((y_a - y_b) * (y_a - y_c)) +
                          x_b * y_a * y_c / ((y_b - y_a) * (y_b - y_c)) +
                          x_c * y_a * y_b / ((y_c - y_a) * (y_c - y_b)))
            else:
                # Si hay valores de y repetidos, se usa el método de la secante (falsa posición)
                self.x = (y_a * x_b - y_b * x_a) / (y_a - y_b)

            # Se verifica si el paso de interpolación es aceptable, si no, se usa bisección
            cond1 = (self.x - (3 * x_a + x_b) / 4) * (self.x - x_b) >= 0
            cond2 = self._biseccion_usada and abs(self.x - x_b) >= abs(x_b - x_c) / 2
            cond3 = not self._biseccion_usada and abs(self.x - x_b) >= abs(x_c - x_d) / 2

            if cond1 or cond2 or cond3:
                self.x = (x_a + x_b) / 2
                self._biseccion_usada = True
            else:
                self._biseccion_usada = False

            if self._fin_iteracion():
                break

            y_x = self._f(self.x)
            x_c, y_c = x_b, y_b # Actualizar el punto previo

            if np.sign(y_a) == np.sign(y_x):
                x_a, y_a = self.x, y_x
            else:
                x_b, y_b = self.x, y_x

            # Se asegura de nuevo que |f(a)| > |f(b)| para la siguiente iteración
            if abs(y_a) < abs(y_b):
                x_a, x_b = x_b, x_a
                y_a, y_b = y_b, y_a

            self._val = x_a, x_b, x_c
            self._val_f = y_a, y_b, y_c

    def graficar(self, mostrar_sol: bool = True, mostrar_iter: bool = True, mostrar_lin_iter: bool = False,
                 n_puntos: int = 100):
        """
        Realiza la gráfica del cálculo de la raíz por el método de Brent.

        Parameters
        ----------
        mostrar_sol: bool
            si es verdadero muestra el punto donde se encontró la solución
            por defecto es True
        mostrar_iter: bool
            si es verdadero muestra los puntos obtenidos de cada iteración
            por defecto es True
        mostrar_lin_iter: bool, optional
            Este parámetro no está implementado para este método. Por defecto es ``False``.
        n_puntos: int, optional
            Número de puntos para dibujar la curva de la función. Por defecto es 100.

        Returns
        -------
        None
            Muestra una gráfica de Matplotlib.
        """
        plt.title(f'x = {self.x}')
        if self._error_porcentual:
            plt.suptitle('Método de Brent (tol= ' + str(self._tol) + '%)')
        else:
            plt.suptitle('Método de Brent (tol= ' + str(self._tol) + ')')
        super().graficar(mostrar_sol, mostrar_iter, mostrar_lin_iter, n_puntos)


def main():
    """Función principal para demostración."""
    def f(x):
        return (x ** 3 + 7 * x ** 2 - 40 * x - 100) / 50

    br = Brent(f, 0.0, 8.0, 0.0001, tipo_error="%")
    br.generar_tabla()
    br.graficar()
    br.solucion()


if __name__ == '__main__':
    main()
