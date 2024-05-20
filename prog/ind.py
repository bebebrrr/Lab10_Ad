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
results = [1]


def calc_sum(x):
    return math.exp(-(x**2))


def calc_chis(x, chis_queue):
    chis_value = -x
    chis_queue.put(chis_value)  # Положить результат в очередь


def calc_znam(n, chis_queue, results_queue, event):
    chis_value = chis_queue.get()  # Получить результат из первой очереди
    chis_queue.task_done()
    znam_value = n + 1
    cur = chis_value / znam_value
    results_queue.put(cur)
    event.set()  # Сигнализировать, что вычисление завершено


def main():
    x = 1
    i = 0
    chis_queue = queue.Queue()
    results_queue = queue.Queue()
    calc_event = threading.Event()

    while True:
        # Создаем и запускаем поток для вычисления числителя
        th1 = threading.Thread(target=calc_chis, args=(x, chis_queue))
        th1.start()
        
        # Создаем и запускаем поток для вычисления знам
        th2 = threading.Thread(target=calc_znam, args=(i, chis_queue, results_queue, calc_event))
        th2.start()

        # Ждем завершения вычислений
        th1.join()
        th2.join()
        calc_event.wait()
        
        calc_event.clear()
        
        cur = results_queue.get()
        results_queue.task_done()
        
        results.append(cur * results[-1])
        
        if math.fabs(results[-1]) <= E:
            break

        i += 1

    y = calc_sum(x)
    calculated_sum = sum(results)
    print(f"x = {x}")
    print(f"Ожидаемое значение y = {y}")
    print(f"Подсчитанное значение суммы ряда = {calculated_sum}")

if __name__ == "__main__":
    main()
