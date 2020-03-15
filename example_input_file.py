#!/usr/bin/env python3

from easymeet import plot_free_schedule, file2dict


input_file = 'example_input_file.txt'
people_free_schedule = file2dict(input_file)

plot_free_schedule(people_free_schedule,
                   first_day='sunday', last_day='saturday',
                   header="Ardur" + '\n' + \
                          "When to play RPG",
                   start_time='7:30', end_time='24',
                   cmap='PuRd',
                   format24=True,
                   hourhlines=True,
                   filename='example/ardur.png')
