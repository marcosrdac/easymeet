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
    "Alber":       "13-16:40 nenhum seg 14:50- seg",
    "Anderson":    "nenhum nenhum nenhum 5-17",
    "André":       "16:40... seg seg seg seg seg seg",
    "Annie":       "16:40- nenhum nenhum 10h40-",
    "Gutembergue": "14:50-17 nenhum seg 11-13 seg",
    "Isaac":       "10:40- seg seg seg seg",
    "Laian":       "nenhum nenhum nenhum 16-16:40",
    "Leticia":     "12-16:40 nenhum seg 16:40- seg",
    "Lorena":      "13-14:50 -10:40 seg",
    "Marcos":      "(9h10-10h20 13h30-18h10) (7-10:20 + 16h-) mon tue -12 - -",
    "Mari":        "10:40- 7-14h seg ter -16h40",
    "Maria M":     "nenhum 15h-16:30 nenhum 10:40-16:30",
    "Maria":       "13-17 seg seg seg seg seg seg",
    "Milton":      "9:45-12:30 nenhum -9:45 10h40-12:30",
    "Nilo":        "nenhum 15... nenhum 13...",
    "Rada":        "13-17 ...10h40 nenhum ter -12",
    "Rômulo":      "13-16h40 nenhum seg 14:50- seg",
    "Vasco":       "-14:50 nenhum seg 10h40- seg",
    "Vinicius":    "13- nenhum seg (-14 16-)",
    }

plot_free_schedule(horarios,
            possible_daynames=possiveis_nomes_dias,
            disp_daynames=labels_para_dias,
            also_possibly_en_daynames=True,
            first_day='seg', last_day='sex',
            start_time='6:30', end_time=20.5,
            header="EAGE Student Chapter - UFBa (2020.1)",
            cbar_label="Número de pessoas disponíveis para uma reunião",
            cmap='Greens',
            format24=True,
            hourhlines=True,
            filename='example/eagescufba.png')

# access matplotlib's site for more colormap (cmaps) names:
# https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
