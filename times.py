import re
import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt


DAYNAMESEN = [['mon', 'monday'],
              ['tue', 'tuesday'],
              ['wed', 'wednesday'],
              ['thu', 'thursday'],
              ['fri', 'friday'],
              ['sat', 'saturday'],
              ['sun', 'sunday']]
SHORTDAYNAMESEN = [ dayname[0] for dayname in DAYNAMESEN ]


def format_time(time):
    try:
        time = float(time)
        h = int(time)
        m = round(60*(time-h))
    except ValueError:
        time_found = re.findall('(\d+)[h:]*(\d*)|(\d)+\.?(\d)', time)
        h1, m1, h2, m2 = time_found[0]
        if h1 or m1:
            h = int(h1) if h1 else 0
            m = int(m1) if m1 else 0
        else:
            h = int(h2)        if h2 else 0
            m = round(60*(m2)) if m2 else 0
    return(h,m)

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

# rename variables for more readability...
def edit_daytimes(daytimes, DAYNAMES=DAYNAMESEN):
    daytimes = re.findall(r'\(([^\)]+)\)|(\S+)', daytimes)
    for dt,_ in enumerate(daytimes):
        daytimes[dt] = [intervals for intervals in daytimes[dt] if intervals][0]
        daytimes[dt] = re.findall(r'(\S+)', daytimes[dt].replace('+', ''))

    # copying list and sublists
    edited_daytimes = [ intervals[:] for intervals in daytimes ]

    for day_intervals_iter, day_intervals in enumerate(daytimes):
        for interval_iter,  interval in enumerate(day_intervals):
            for day_iter,   daynames in enumerate(DAYNAMES):

                if interval in daynames:
                    edited_daytimes[day_intervals_iter].remove(interval)
                    equalsday = interval
                    notfound = True
                    while notfound:
                        for daynames_n,   daynames in enumerate(DAYNAMES):
                            for dayname_n, dayname in enumerate(daynames):
                                if equalsday == dayname:
                                    equalsday = edited_daytimes[daynames_n]
                                    notfound = False
                                    break
                        else: break  # take a look at for / else sintax ;)
                    for edited_interval in equalsday:
                        edited_daytimes[day_intervals_iter].append(edited_interval)

    for day_intervals_iter, day_intervals in enumerate(edited_daytimes):
        for interval_iter, interval in enumerate(day_intervals):
            edited_daytimes[day_intervals_iter][interval_iter] = format_interval(interval)
    return(edited_daytimes)


def plot_times(intervals,
            possible_daynames=DAYNAMESEN, also_possibly_en_daynames=True,
            disp_daynames=None,
            header='', ax_title='', hourhlines=True,
            first_day=0, last_day=4,
            start_time=7, end_time=20,
            cmap='Blues',
            filename=None):
    # setting possible_daynames
    if also_possibly_en_daynames:
        for d in range(7):
            if possible_daynames[d] != DAYNAMESEN[d]:
                possible_daynames[d] += DAYNAMESEN[d]
    if not disp_daynames:
        disp_daynames = [ dayname[0] for dayname in possible_daynames ]

    # creating grid for week times
    grid = np.zeros((24*60,7))  # 24 hours, 60 minutes/hour, 7 days
    # filling weektimes
    for interval in intervals.values():
        hdays = edit_daytimes(interval, possible_daynames)
        for d, day in enumerate(hdays):
            daygrid = np.zeros(24*60)
            for times in day:
                daygrid[times[0]:times[1]] = 1
            grid[:, d] += daygrid

    # translating days to numbers
    if not isinstance(first_day, int):
        first_day = disp_daynames.index(first_day)
    if not isinstance(last_day, int):
        last_day = disp_daynames.index(last_day)
    # if first day is sunday, roll list so that it is true
    if first_day == 6:
        disp_daynames.insert(0, disp_daynames.pop())
        grid = np.roll(grid, 1)
        first_day = 0
    # cmap input can be a cmap obbject or cmap name string
    cmap = plt.get_cmap(cmap)

    # day start and end times: (h1,m1) and (h2,m2)
    h1, m1 = format_time(start_time)
    h2, m2 = format_time(end_time)
    t1 = h1*60+m1
    t2 = h2*60+m2

    # creating canvas
    fig = plt.figure(figsize=(4, 6))
    # setting bigger title
    fig.suptitle(header, va='top')

    # creating axes
    ax = fig.add_axes([.1,0,.88,.85])
    ax.set_title(ax_title, y=1.08)

    # plotting grid heatmap to axes
    img = ax.imshow(grid, aspect='auto', interpolation='nearest', cmap=cmap)
    # configuring axes
    ax.set_xticks(np.arange(grid.shape[1]))
    ax.set_xticklabels(disp_daynames)
    ax.yaxis.set_ticks(np.arange(0, grid.shape[0]+1, 60))
    #ax.set_yticklabels([ f'{hour}h' for hour in range(h1,h2+1,1) ])
    ax.set_yticklabels([f'{hour}h' for hour in range(0, 24+1, 1)])
    # limit plot of grid
    ax.set_ylim((t2, t1))
    ax.set_xlim((first_day-.5, last_day+.5))
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=False,
                   left=True, right=False,
                   labelleft=True, labelright=False,
                   labeltop=True, labelbottom=False)
    if hourhlines:
        for hour in range(0, 24+1):
            ax.axhline(60*hour, color="black", alpha=.05, ls='-')
    # Turn spines off and create
    for _, spine in ax.spines.items():  # edge, spine
        spine.set_visible(False)

    # create colorbar
    visiblegridmin = grid[t1:t2].min()
    visiblegridmax = grid[t1:t2].max()
    bounds = np.arange(visiblegridmin, visiblegridmax+2, dtype=int)
    vals = bounds[:-1]
    norm = clr.BoundaryNorm(bounds, cmap.N)
    cbar = ax.figure.colorbar(img,
                              fraction=.12,
                              pad=.05,
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

    # if filename set, save generated figure
    if filename:
        plt.savefig(filename)
    plt.show()





if __name__ == '__main__':

    # both portuguese and english
    possible_daynames_pt = [['seg', 'segunda', 'segunda-feira',],
                            ['ter', 'terça', 'terça-feira',],
                            ['qua', 'quarta', 'quarta-feira',],
                            ['qui', 'quinta', 'quinta-feira',],
                            ['sex', 'sexta', 'sexta-feira',],
                            ['sáb', 'sábado', 'sab',],
                            ['dom', 'sunday', 'domingo',]]
    disp_daynames_pt = [dayname[0] for dayname in possible_daynames_pt]

    #horarios = {
    #        "a": "13...15 (seg + seg + 7-9) (tue + 19:..20)",
    #        "b": "14-16h40 nope seg",
    #        "c": "(13h30-14:20 15...16) nope nope seg (seg + thu)",
    #    }
    # bota manhã e tarde, bro

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


    plot_times(horarios,
               possible_daynames=possible_daynames_pt,
               also_possibly_en_daynames=True,
               first_day='seg', last_day='sex',
               header="EAGE Student Chapter - UFBa (2020.1)",
               start_time='6:30', end_time=20.5,
               cmap='Greens',
               hourhlines=True,
               filename='times.png')
