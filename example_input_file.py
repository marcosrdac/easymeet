#!/usr/bin/env python3

from re import findall
from easymeet import plot_free_schedule, file2dict


input_file = 'example_input_file.txt'
people_free_schedule = file2dict(input_file)

plot_free_schedule(people_free_schedule,
                   also_possibly_en_daynames=True,
                   first_day=0, last_day=5,
                   header="EAGE Student Chapter - UFBa (2020.1)",
                   start_time='6:30', end_time=20.5,
                   cmap='Greens',
                   format24=True,
                   hourhlines=True,
                   filename='example/eagescufba.png')
