import re
import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt
cmap = 'Greens'

daynames = [['mon', 'monday'],
        ['tue', 'tuesday'],
        ['wed', 'wednesday'],
        ['thu', 'thursday'],
        ['fri', 'friday'],
        ['sat', 'saturday'],
        ['sun', 'sunday']]
daynamespt = [['segunda', 'segunda-feira', 'seg'],
          ['terça', 'terça-feira', 'ter'],
          [ 'quarta', 'quarta-feira', 'qua'],
          [ 'quinta', 'quinta-feira', 'qui'],
          [ 'sexta', 'sexta-feira', 'sex'],
          [ 'sábado', 'sab', 'sáb'],
          ['sunday', 'domingo', 'dom']]
daynames = [ daynames[d]+daynamespt[d] for d in range(7) ]

def format_interval(interval):
    interval = re.findall('(\d*)[h:]*(\d*)[-\.]+(\d*)[h:]*(\d*)', interval)
    if interval:
        h1, m1, h2, m2 = interval[0]
        h1 = int(h1) if h1 else 0
        m1 = int(m1) if m1 else 0
        h2 = int(h2) if h2 else 23
        m2 = int(m2) if m2 else 60
        t1 = 60*h1+m1
        t2 = 60*h2+m2
    else:
        t1, t2 = 0,0
    return(t1,t2)


def conv_text(times):
    daytimes = re.findall(r'\(([^\)]+)\)|(\S+)', times)
    for dt,_ in enumerate(daytimes):
        daytimes[dt] = [intervals for intervals in daytimes[dt] if intervals][0]
        daytimes[dt] = re.findall(r'(\S+)', daytimes[dt].replace('+', ''))

    # copying list
    edited_daytimes = [ intervals[:] for intervals in daytimes ]

    for intervals_iter, intervals in enumerate(daytimes):
        for interval_iter, interval in enumerate(intervals):
            for day_iter, day_names in enumerate(daynames):
                if interval in day_names:
                    edited_daytimes[intervals_iter].remove(interval)
                    for edited_interval in daytimes[day_iter]:
                        edited_daytimes[intervals_iter].append(edited_interval)

    for intervals_iter, intervals in enumerate(edited_daytimes):
        for interval_iter, interval in enumerate(intervals):
            edited_daytimes[intervals_iter][interval_iter] = format_interval(interval)
    return(edited_daytimes)


#times = "1h... 2-3 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3) (seg + thu)"
#times = "1h... '' 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3)"
#days = conv_text(times)

# bota manhã e tarde, bro
horarios = {
	"a": "13...15 seg",
	"b": "14-16h40 nope seg",
        "c": "(13h30-14:20 15...16) nope nope seg thu",
	#"Nilo": "nope 15... nope 13...",
	#"Rada": "13-17 ...10h40 nope tue -12",
	#"Maria": "13-17 seg seg seg seg seg seg",
	#"André": "nope nope nope nope 13-17",
	#"Lorena": "13-14:50 -10:40 seg",
	#"Laian": "nope nope nope 16-16:40",
	#"Anderson": "nope nope nope 5-17",
	#"Vinicius": "13- nope seg (-14 16-)",
	#"Mari": "10:40- 7-14h seg ter -16h40",
	#"Leticia": "12-16:40 nope seg 14:50- seg",
	#"Gutembergue": "14:50-17:00 nope seg nope seg",
	#"Alber": "13-16:40 nope seg 14:50- seg",
	#"Isaac": "10:40- seg seg seg seg",
	#"Rômulo": "13-16h40 nope seg 14:50- seg",
	#"Annie": "16:40- nope nope 10h40-",
	#"Maria M": "nope 15h-16:30 nope 10:40-16:30",
	#"Vasco": "-14:50 nope seg 10h40- seg",
	#"Milton": "9:45-12:30 nope -9:45 10h40-12:30",
}



grid = np.zeros((24*60,7))
for horario in horarios.values():
    hdays = conv_text(horario)
    for d, day in enumerate(hdays):
        for times in day:
            grid[times[0]:times[1], d] += 1


start=7
end=20
last_day='fri'
#daynames=[ days[i][0] for i in range(6) ]
daynames=['mon' ,'tue','wed','thu','fri','sat','sun']

days_to_show = daynames.index(last_day)
data=grid[start*60:end*60,:days_to_show+1]
col_labels = []
row_labels = []
fig, ax = plt.subplots(figsize=(4,6))
fig.suptitle("EAGE Student Chapter - UFBA (2020.1)")
# plot grid heatmap
im = ax.imshow(data, aspect='auto', interpolation='nearest', cmap=cmap)
# days axis
ax.set_xticks(np.arange(data.shape[1]))
ax.set_xticklabels(daynames)
ax.yaxis.set_ticks(np.arange(0, data.shape[0]+1, 60))
ax.set_yticklabels([ f'{hour}h' for hour in range(start,end+1,1) ])
# Let the horizontal axes labeling appear on top.
ax.tick_params(top=True, bottom=False,
                labeltop=True, labelbottom=False)
# Turn spines off and create white grid.
for edge, spine in ax.spines.items():
    spine.set_visible(False)
# create colorbar
cmap = plt.get_cmap(cmap)
bounds=np.arange(grid.min(),data.max()+2, dtype=int)
vals=bounds[:-1]
norm = clr.BoundaryNorm(bounds, cmap.N)
cbar = ax.figure.colorbar(im,
                        cmap=cmap,
                        norm=norm,
                        boundaries=bounds,
                        orientation='horizontal',
                        values=vals,
                        ticks=bounds)
cbar.set_ticks(vals + .5)
cbar.set_ticklabels(vals)
cbar.ax.set_xlabel('Number of people able for a meeting', rotation=0)
cbar.outline.set_linewidth(0)

plt.show()
