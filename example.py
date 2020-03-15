#!/usr/bin/env python3

from easymeet import plot_free_schedule

people_free_schedules = {
        # person     mon     tue         wed             thu  fri
        "Person A": "13...15 (mon + 7-9) (tue + 19:..20) nope 10-18",
        # person     mon      tue  wed thu fri
        "Person B": "14-16h40 nope ... mon ...",
        # person     mon                      tue  wed  thu fri
        "Person C": "(12h30-14:30 15:20...16) nope nope mon (mon + thu)",
    }

plot_free_schedule(people_free_schedules,
                   header="Ease scheduling meetings for your team!" + '\n' +
                          "(Dark colors equals good)",
                   filename='example/example.png')
