import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
cmap = 'Greens'

days = np.array(['seg', 'ter', 'qua', 'qui', 'sex','sab'])
starting_time = 7
final_time = 22
period = final_time-starting_time
h_div = 60
time_num = period*h_div
times = np.array([starting_time + i/h_div for i in range(0,time_num+1)])

grid = pd.DataFrame(index=times, columns=days)
grid.fillna(0, inplace=True)
#sns.heatmap(grid)

days = np.array(['seg', 'ter', 'qua', 'qui', 'sex','sab'])
starting_time = 7
final_time = 20
period = final_time-starting_time
h_div = 6
time_num = period*h_div
times = np.array([starting_time + i/h_div for i in range(0,time_num+1)])

grid = pd.DataFrame(index=times, columns=days)
grid.fillna(0, inplace=True)

morning = [(8, 11.5)]
afternoon = [(13.5, 17)]
none = [(-1,-1)]
all_day = [(starting_time,final_time)]


people_times = {
"Nilo": [
		[[0, 0]],
		[[15.0, 23.983333333333334]],
		[[0, 0]],
		[[13.0, 23.983333333333334]]
	],
"Rada": [
		[[13.0, 17.983333333333334]],
		[[0.0, 10.666666666666666]],
		[[0, 0]],
		[[0.0, 10.666666666666666]],
		[[0.0, 12.983333333333333]]
	],
"Maria": [
		[[13.0, 17.983333333333334]],
		[[13.0, 17.983333333333334]],
		[[13.0, 17.983333333333334]],
		[[13.0, 17.983333333333334]],
		[[13.0, 17.983333333333334]],
		[[13.0, 17.983333333333334]],
	],
"André": [
		[[0, 0]],
		[[0, 0]],
		[[0, 0]],
		[[0, 0]],
		[[13.0, 17.983333333333334]]
	],
"Lorena": [
		[[13.0, 14.833333333333334]],
		[[0.0, 10.666666666666666]],
		[[13.0, 14.833333333333334]]
	],
"Laian": [
		[[0, 0]],
		[[0, 0]],
		[[0, 0]],
		[[16.0, 16.666666666666668]]
	],
"Anderson": [
		[[0, 0]],
		[[0, 0]],
		[[0, 0]],
		[[5, 17]]
	],
"Vinicius": [
		[[13.0, 23.983333333333334]],
		[[0, 0]],
		[[13.0, 23.983333333333334]],
		[[0.0, 14.983333333333333],
		[16.0, 23.983333333333334]]
	],
"Mari": [
		[[10.666666666666666, 23.983333333333334]],
		[[7.0, 14.983333333333333]],
		[[10.666666666666666, 23.983333333333334]],
		[[7.0, 14.983333333333333]], [[0.0, 16.666666666666668]]
	],
"Leticia": [
		[[12.0, 16.666666666666668]],
		[[0, 0]],
		[[12.0, 16.666666666666668]],
		[[14.833333333333334, 23.983333333333334]],
		[[12.0, 16.666666666666668]]
	],
"Gutembergue": [
		[[14.833333333333334, 17.0]],
		[[0, 0]],
		[[14.833333333333334, 17.0]],
		[[0, 0]],
		[[14.833333333333334, 17.0]]
	],
"Alber": [
		[[13.0, 16.666666666666668]],
		[[0, 0]],
		[[13.0, 16.666666666666668]],
		[[14.833333333333334, 23.983333333333334]],
		[[13.0, 16.666666666666668]]
	],
"Isaac": [
		[[10.666666666666666, 23.983333333333334]],
		[[10.666666666666666, 23.983333333333334]],
		[[10.666666666666666, 23.983333333333334]],
		[[10.666666666666666, 23.983333333333334]],
		[[10.666666666666666, 23.983333333333334]]
	],
"Rômulo": [
		[[13.0, 16.666666666666668]],
		[[0, 0]],
		[[13.0, 16.666666666666668]],
		[[14.833333333333334, 23.983333333333334]],
		[[13.0, 16.666666666666668]]
	],
"Annie": [
		[[16.666666666666668, 23.983333333333334]],
		[[0, 0]],
		[[0, 0]],
		[[10.666666666666666, 23.983333333333334]]
	],
"Maria M": [
		[[0, 0]],
		[[15.0, 16.5]],
		[[0, 0]],
		[[10.666666666666666, 16.5]]
	],
"Vasco": [
		[[0.0, 14.833333333333334]],
		[[0, 0]],
		[[0.0, 14.833333333333334]],
		[[10.666666666666666, 23.983333333333334]],
		[[0.0, 14.833333333333334]]
	],
"Milton": [
		[[9.75, 12.5]],
		[[0, 0]],
		[[0.0, 9.75]],
		[[10.666666666666666, 12.5]]
		],
}


for k in people_times.keys():
    for (d, j) in zip(days, people_times[k]):
        for (m,n) in j:
            for t in list(times):
                if t>=m and t<=n:
                    grid.loc[t][d] += 1

grid.fillna(value=0, inplace=True)
n_max = grid.max().max()
print(n_max)
boundaries = [ int(i) for i in range(0,n_max+1)]
values = [ i for i in range(1,n_max+1)]
sns.set_context('talk')
#fig = plt.figure(figsize=(8,8))
#ax = fig.add_axes([.1,.1,.8,.8])
fig, ax = plt.subplots(figsize=(8,8))
ax = sns.heatmap(grid, yticklabels=h_div, cmap=cmap, cbar_kws={
    'boundaries': boundaries,
    'extend':     'both',
    'extendrect': True,
    'extendfrac': .1,
#    'values': values,
    })#'drawedges':True})
#ax.set_title('Número de NEXters disponíveis por horário')
#ax.set_title('Roda com Ciência: pessoas disponíveis por horário')
ax.set_title('EAGE Student Chapter:\nN. Pessoas disponíveis por horário')
ax.set_ylabel('Horário')
ax.set_xlabel('Dia da semana')

colorbar = ax.collections[0].colorbar

fig.savefig('h.png')
plt.tight_layout()
plt.show()



def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """

    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = concatenate((linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in xrange(N+1) ]
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
