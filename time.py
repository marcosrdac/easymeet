import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
cmap = 'Greens'

mon  = ['monday']   + [ 'segunda' + feira for feira in ['','-feira'] ]
mon += [ day[:3] for day in mon[:2]]
tue  = ['tuesday']  + [ 'terça' + feira for feira in ['','-feira'] ]
tue += [ day[:3] for day in tue[:2] ]
wed  = ['wednesday'] + [ 'quarta' + feira for feira in ['','-feira'] ]
wed += [ day[:3] for day in wed[:2] ]
thu  = ['thursday'] + [ 'quinta' + feira for feira in ['','-feira'] ]
thu += [ day[:3] for day in thu[:2] ]
fri  = ['friday'] + [ 'sexta' + feira for feira in ['','-feira'] ]
fri += [ day[:3] for day in fri[:2] ]
sat  = ['saturday'] + ['sábado']
sat += [ day[:3] for day in sat ]
sun  = ['sunday']   + ['domingo']
sun += [ day[:3] for day in sun ]
days = {'0': mon,
        '1': tue,
        '2': wed,
        '3': thu,
        '4': fri,
        '5': sat,
        '6': sun,}

def format_interval(interval):
    interval = re.findall('(\d*)[h:]*(\d*)[-\.]+(\d*)[h:]*(\d*)', interval)
    if len(interval)<1:
        t1, t2 = 0,0
    else:
        h1, m1, h2, m2 = interval[0]
        h1 = int(h1) if h1!='' else 0
        m1 = int(m1) if m1!='' else 0
        h2 = int(h2) if h2!='' else 23
        m2 = int(m2) if m2!='' else 59 # actually 60
        #interval=f'{h1:.0f}:{m1:.0f} até {h2:.0f}:{m2:.0f}'
        t1 = 60*h1+m1
        t2 = 60*h2+m2
    return([t1,t2])


def conv_text(times):
    daytimes = re.findall(r'\(([^\)]+)\)|(\S+)', times)
    for dt,_ in enumerate(daytimes):
        daytimes[dt] = daytimes[dt][0] if daytimes[dt][0]!='' else daytimes[dt][1]
        daytimes[dt] = daytimes[dt].replace('+', '')
        daytimes[dt] = re.findall(r'(\S+)', daytimes[dt])

    formated_daytimes = daytimes.copy()  # it only copies the major list
    for i,_ in enumerate(formated_daytimes):
        formated_daytimes[i] = daytimes[i].copy()

    for dt, intervals in enumerate(daytimes):
        for i, interval in enumerate(intervals):
            for d, (day, daynames) in enumerate(days.items()):
                if interval in daynames:
                    formated_daytimes[dt].remove(interval)
                    for intn, anotherinterval in enumerate(daytimes[d]):
                        formated_daytimes[dt].append(anotherinterval)
    for dt, intervals in enumerate(formated_daytimes):
        for i, interval in enumerate(intervals):
            formated_daytimes[dt][i] = format_interval(interval)
    return(formated_daytimes)


#times = "1h... 2-3 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3) (seg + thu)"
times = "1h... '' 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3)"

#days = conv_text(times)

grid = np.zeros((24*60,7))

# bota manhã e tarde, bro
horarios = {
	"Nilo": "nope 15... nope 13...",
	"Rada": "13-17 ...10h40 nope tue -12",
	"Maria": "13-17 seg seg seg seg seg seg",
	"André": "nope nope nope nope 13-17",
	"Lorena": "13-14:50 -10:40 seg",
	"Laian": "nope nope nope 16-16:40",
	"Anderson": "nope nope nope 5-17",
	"Vinicius": "13- nope seg (-14 16-)",
	"Mari": "10:40- 7-14h seg ter -16h40",
	"Leticia": "12-16:40 nope seg 14:50- seg",
	"Gutembergue": "14:50-17:00 nope seg nope seg",
	"Alber": "13-16:40 nope seg 14:50- seg",
	"Isaac": "10:40- seg seg seg seg",
	"Rômulo": "13-16h40 nope seg 14:50- seg",
	"Annie": "16:40- nope nope 10h40-",
	"Maria M": "nope 15h-16:30 nope 10:40-16:30",
	"Vasco": "-14:50 nope seg 10h40- seg",
	"Milton": "9:45-12:30 nope -9:45 10h40-12:30",
}



for horario in horarios.values():
    hdays = conv_text(horario)
    for d, day in enumerate(hdays):
        for times in day:
            grid[times[0]:times[1], d] += 1


start=7
end=20
last_day='fri'
daynames=['mon' ,'tue','wed','thu','fri','sat','sun']
days_to_show = daynames.index(last_day)
data=grid[start*60:end*60,:days_to_show+1]
col_labels = []
row_labels = []
fig, ax = plt.subplots(figsize=(4,6))
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
bounds=np.arange(grid.min(),grid.max()+2, dtype=int)
vals=bounds[:-1]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
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
# ... and label them with the respective list entries.
#ax.set_xticklabels([day for day, vals in days.items()[0]])

plt.show()
