#!/usr/bin/env python3

from easymeet import plot_free_schedule

# interpret these days as possible daynamees in people_free_schedule
possiveis_nomes_dias = [['seg', 'segunda', 'segunda-feira',],
                        ['ter', 'terça', 'terça-feira',],
                        ['qua', 'quarta', 'quarta-feira',],
                        ['qui', 'quinta', 'quinta-feira',],
                        ['sex', 'sexta', 'sexta-feira',],
                        ['sáb', 'sábado', 'sab',],
                        ['dom', 'sunday', 'domingo',]]
labels_para_dias = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom']

horarios = {
    "Nilo":        "nenhum 15... nenhum 13...",
    "Rada":        "13-17 ...10h40 nenhum tue -12",
    "Maria":       "13-17 seg seg seg seg seg seg",
    "André":       "nenhum nenhum nenhum nenhum 13-17",
    "Lorena":      "13-14:50 -10:40 seg",
    "Laian":       "nenhum nenhum nenhum 16-16:40",
    "Anderson":    "nenhum nenhum nenhum 5-17",
    "Vinicius":    "13- nenhum seg (-14 16-)",
    "Mari":        "10:40- 7-14h seg ter -16h40",
    "Leticia":     "12-16:40 nenhum seg 14:50- seg",
    "Gutembergue": "14:50-17:00 nenhum seg nenhum seg",
    "Alber":       "13-16:40 nenhum seg 14:50- seg",
    "Isaac":       "10:40- seg seg seg seg",
    "Rômulo":      "13-16h40 nenhum seg 14:50- seg",
    "Annie":       "16:40- nenhum nenhum 10h40-",
    "Maria M":     "nenhum 15h-16:30 nenhum 10:40-16:30",
    "Vasco":       "-14:50 nenhum seg 10h40- seg",
    "Milton":      "9:45-12:30 nenhum -9:45 10h40-12:30",
    }

plot_free_schedule(horarios,
            possible_daynames=possiveis_nomes_dias,
            disp_daynames=labels_para_dias,
            also_possibly_en_daynames=True,
            first_day='seg', last_day='sex',
            header="EAGE Student Chapter - UFBa (2020.1)",
            start_time='6:30', end_time=20.5,
            cmap='Greens',
            format24=True,
            hourhlines=True,
            filename='example/eagescufba.png')
