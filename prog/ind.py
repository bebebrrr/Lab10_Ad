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

def calc_chis(x, q):
    chis_value = -x
    q.put(chis_value)  # результат в очередь

def calc_znam(q1, q2, event):
    chis_value = q1.get()  # результат из первой очереди
    znam_value = chis_value / (q2.get() + 1)  # Поделить чис на знам 
    q1.task_done()
    q2.task_done()
    event.set()  # Сигнализировать, что вычисление завершено
    return znam_value

def main():
    x = 1
    i = 0
    chis_queue = queue.Queue()
    znam_queue = queue.Queue()
    calc_event = threading.Event()

    while math.fabs(results[-1]) > E:
        # Создание и запуск потоков для вычисления числ и знам
        th1 = threading.Thread(target=calc_chis, args=(x, chis_queue))
        th1.start()

        # очередь для знам
        znam_queue.put(i)

        th2 = threading.Thread(target=lambda q1, q2, e: results.append(calc_znam(q1, q2, e) * results[-1]), args=(chis_queue, znam_queue, calc_event))
        th2.start()

        th1.join()
        th2.join()
        calc_event.wait()

        calc_event.clear()
        i += 1

    y = calc_sum(x)
    calculated_sum = sum(results)
    print(f"x = {x}")
    print(f"Ожидаемое значение y = {y}")
    print(f"Подсчитанное значение суммы ряда = {calculated_sum}")

if __name__ == "__main__":
    main()
