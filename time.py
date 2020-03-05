import re
import numpy as np
import matplotlib.pyplot as plt
#cmap = 'Blues'
#
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
        h2 = int(h2) if h2!='' else 0
        m2 = int(m2) if m2!='' else 0
        #interval=f'{h1:.0f}:{m1:.0f} até {h2:.0f}:{m2:.0f}'
        t1 = 60*h1+m1
        t2 = 60*h2+m2-1
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
    print(formated_daytimes)
    return(formated_daytimes)


#times = "1h... 2-3 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3) (seg + thu)"
times = "1h... '' 13:30-15h (7:50-8 16-17h2 ) seg (-2 ...3)"

days = conv_text(times)

grid = np.zeros((24*60,7))



for d, day in enumerate(days):
    for times in day:
        grid[times[0]:times[1], d] += 1


plt.imshow(grid, aspect='auto')
plt.show()
