import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt
from  re import findall


DAYNAMESEN = [['mon', 'monday'],
              ['tue', 'tuesday'],
              ['wed', 'wednesday'],
              ['thu', 'thursday'],
              ['fri', 'friday'],
              ['sat', 'saturday'],
              ['sun', 'sunday']]

def format_time(time):
    try:
        time = float(time)
        h = int(time)
        m = round(60*(time-h))
    except ValueError:
        time_found = findall('(\d+)[h:]*(\d*)|(\d)+\.?(\d)', time)
        h1, m1, h2, m2 = time_found[0]
        if h1 or m1:
            h = int(h1) if h1 else 0
            m = int(m1) if m1 else 0
        else:
            h = int(h2)        if h2 else 0
            m = round(60*(m2)) if m2 else 0
    return(h,m)

def format_interval(interval):
    interval = findall('(\d*)[h:]*(\d*)[-\.]+(\d*)[h:]*(\d*)', interval)
    if interval:
        h1, m1, h2, m2 = interval[0]
        h1 = int(h1) if h1 else 0
        m1 = int(m1) if m1 else 0
        if h2:
            h2 = int(h2)
            m2 = int(m2) if m2 else 0
        else:
            h2, m2 = 23, 60
        t1 = 60*h1+m1
        t2 = 60*h2+m2
    else:
        t1, t2 = 0,0
    return(t1,t2)


def file2dict(filename):
    dic = {}
    with open(filename) as f:
        for line in f.readlines():
            res = findall(r'([\s\w]*):?\s*(.+)', line)
            if len(res)>0:
                res = res[0]
                dic[res[0]] = res[1]
    return(dic)

# rename variables for more readability...
def edit_daytimes(daytimes, possible_daynames=DAYNAMESEN):
    daytimes = findall(r'\(([^\)]+)\)|(\S+)', daytimes)
    for dt,_ in enumerate(daytimes):
        daytimes[dt] = [intervals for intervals in daytimes[dt] if intervals][0]
        daytimes[dt] = findall(r'(\S+)', daytimes[dt].replace('+', ''))

    # copying list and sublists
    edited_daytimes = [ intervals[:] for intervals in daytimes ]

    for day_intervals_iter, day_intervals in enumerate(daytimes):
        for interval_iter,  interval in enumerate(day_intervals):
            for day_iter,   daynames in enumerate(possible_daynames):

                if interval in daynames:
                    edited_daytimes[day_intervals_iter].remove(interval)
                    equalsday = interval
                    notfound = True
                    while notfound:
                        for daynames_n,   daynames in enumerate(possible_daynames):
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
            edited_daytimes[day_intervals_iter][interval_iter] = \
                                                format_interval(interval)
    return(edited_daytimes)


def plot_free_schedule(intervals,
            possible_daynames=DAYNAMESEN, also_possibly_en_daynames=True,
            disp_daynames=None,
            header='', ax_title='', hourhlines=True,
            first_day=0, last_day=4,
            start_time=7, end_time=20,
            format24=False,
            cmap='Blues',
            show=True,
            filename=None):
    # setting possible_daynames
    if also_possibly_en_daynames:
        for d in range(7):
            if possible_daynames[d] != DAYNAMESEN[d]:
                possible_daynames[d] += DAYNAMESEN[d]
    if not disp_daynames:
        disp_daynames = [ dayname[0] for dayname in possible_daynames ]
    else:
        for d in range(7):
            if disp_daynames[d] not in possible_daynames[d]:
                possible_daynames[d] += [disp_daynames[d]]

    # creating grid for week times
    grid = np.zeros((24*60,7))  # 24 hours, 60 minutes/hour, 7 days
    # filling weektimes
    for person, person_schedule in intervals.items():
        day_intervals = edit_daytimes(person_schedule, possible_daynames)
        for d, day in enumerate(day_intervals):
            day_grid = np.zeros(24*60)
            for times in day:
                day_grid[times[0]:times[1]] = 1
            grid[:, d] += day_grid

    # translating days to numbers
    if not isinstance(first_day, int):
        for d in range(7):
            if first_day in possible_daynames[d]:
                first_day = d
                break
    if not isinstance(last_day, int):
        for d in range(7):
            if last_day in possible_daynames[d]:
                last_day = d
                break
    # if first day is sunday, roll list so that it is true
    if first_day == 6:
        disp_daynames.insert(0, disp_daynames.pop())
        grid = np.roll(grid, 1)
        first_day = 0
    if format24:
        hours = [f'{hour}h' for hour in range(0, 24+1, 1)]
    else:
        hours  = [f'{hour} AM' for hour in range(0, 12+1, 1)]
        hours += [f'{hour} PM' for hour in range(1, 12+1, 1)]
    # cmap input can be a cmap obbject or cmap name string
    cmap = plt.get_cmap(cmap)

    # day start and end times: (h1,m1) and (h2,m2)
    h1, m1 = format_time(start_time)
    h2, m2 = format_time(end_time)
    t1 = h1*60+m1
    t2 = (h2-1)*60+m2

    # creating canvas
    fig = plt.figure(figsize=(4, 6))
    # setting bigger title
    fig.suptitle(header, va='top')

    # creating axes
    if format24:
        ax_dims = [.1,0,.88,.85]
    else:
        ax_dims = [.15,0,.82,.85]
    ax = fig.add_axes(ax_dims)
    ax.set_title(ax_title, y=1.08)

    # plotting grid heatmap to axes
    img = ax.imshow(grid, aspect='auto', interpolation='none', cmap=cmap)
    # configuring axes
    ax.set_xticks(np.arange(grid.shape[1]))
    ax.set_xticklabels(disp_daynames)
    ax.yaxis.set_ticks(np.arange(0, grid.shape[0]+1, 60))
    #ax.set_yticklabels([ f'{hour}h' for hour in range(h1,h2+1,1) ])
    ax.set_yticklabels(hours)
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
    if show:
        plt.show()





if __name__ == '__main__':
    people_free_schedules = {
            "Person A": "13...15 mon",
            "Person B": "14-16h40 nope mon",
            "Person C": "(12h30-14:30 15:20...16) nope nope mon",
        }

    plot_free_schedule(people_free_schedules,
                header="Test" + '\n' +
                       "I Hope everything is alright!")
