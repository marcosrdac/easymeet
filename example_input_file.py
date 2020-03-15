#!/usr/bin/env python3

from easymeet import plot_free_schedule, file2dict


input_file = 'example_input_file.txt'
people_free_schedule = file2dict(input_file)

plot_free_schedule(people_free_schedule,
                   header="Ardur" + '\n' + \
                          "When to play RPG",
                   cbar_label="Number of people able to play",
                   first_day='sunday', last_day='saturday',
                   start_time='7:30', end_time='24',
                   cmap='PuRd',
                   format24=True,
                   hourhlines=True,
                   filename='example/ardur.png')
