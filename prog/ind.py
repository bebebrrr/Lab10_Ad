#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23 необходимо организовать
# конвейер, в котором сначала в отдельном потоке вычисляется значение первой функции,
# после чего результаты вычисления должны передаваться второй функции, вычисляемой в
# отдельном потоке. Потоки для вычисления значений двух функций должны запускаться
# одновременно.

import math
import threading
import queue

E = 10e-7


def calc_sum(x):
    return math.exp(-(x**2))


def calc_chis(x, n):
    return ((-1) ** n) * (x ** (2 * n))


def calc_znam(n):
    return math.factorial(n)


def calc_part(x, n, result_queue):
    chis = calc_chis(x, n)
    znam = calc_znam(n)
    result_queue.put((chis, znam))


def main():
    x = -0.7
    result_queue = queue.Queue()

    i = 1
    while True:
        # Создаем поток для вычисления части ряда
        part_thread = threading.Thread(
            target=calc_part, args=(x, i, result_queue)
        )
        part_thread.start()

        # Получаем результат вычисления
        chis, znam = result_queue.get()
        part_thread.join()

        # Проверяем условие остановки
        if abs(chis / znam) < E:
            break

        i += 1

    y = calc_sum(x)
    calculated_sum = chis / znam
    print(f"x = {x}")
    print(f"Ожидаемое значение y = {round(y,4)}")
    print(f"Подсчитанное значение суммы ряда = {round(calculated_sum, 7)}")


if __name__ == "__main__":
    main()
