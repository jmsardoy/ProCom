import numpy as np 
import matplotlib.pyplot as plt


def figplot(x, y, rows, cols, numplot, plot_type, xlim, ylim, xlabels, 
            ylabels, join_vec=None, show=False):
    
    if not join_vec: join_vec = range(1, rows*cols+1)

    #Vectors dimension check
    if not (len(x)==len(y)==len(plot_type)==len(xlim)==len(ylim)):
        raise ValueError('Vectors Dims doesn\'t match')
    
    #Join Vec check
    for t in join_vec:
        if isinstance(t, tuple):
            if len(t) > 2: 
                raise ValueError('Join Vector Value Error')
            init_row = (t[0]-1)/cols
            fin_row = (t[1]-1)/cols
            if init_row != fin_row:
                if ((t[0]-1)%cols != 0) or (t[1]%cols != 0):
                    raise ValueError('Join Vector Value Error')
                    


    xlbl_count = ylbl_count = 0
    plt.figure(numplot)
    for xx, yy, ptype, xxlim, yylim, join in zip(x, y, plot_type, xlim, ylim, 
                                                 join_vec):
        plt.subplot(rows,cols, join)
        ptype(xx,yy)
        plt.xlim(xxlim)
        plt.ylim(yylim)
        plt.grid()

        if isinstance(join, tuple): index = join[0]
        else: index = join
        if index%cols == 1:
            plt.ylabel(ylabels[ylbl_count]); ylbl_count += 1
        if  index>(rows*cols-cols):
            plt.xlabel(xlabels[xlbl_count]); xlbl_count += 1
    if show:
        plt.show()

x = []
y = []
xlim = []
ylim = []
plot_type = []
xlabels = ['xlabel1', 'xlabel2', 'xlabel3']
ylabels = ['ylabel1', 'ylabel2', 'ylabel3']
for i in range(8):
    x.append(range(10))
    y.append(range(10))
    xlim.append((-2,10))
    ylim.append((-2,10))
    if i%2==0: plot_type.append(plt.plot)
    else: plot_type.append(plt.stem)
rows = 3
cols = 3
join_vec = [(1,2), 3, 4, 5, 6, 7, 8, 9]
numplot = 1
figplot(x, y, rows, cols, numplot, plot_type, xlim, ylim, xlabels, ylabels,
        join_vec=join_vec, show=False)

x = []
y = []
xlim = []
ylim = []
plot_type = []
xlabels = ['xlabel1', 'xlabel2', 'xlabel3']
ylabels = ['ylabel1', 'ylabel2', 'ylabel3']
for i in range(5):
    x.append(range(10))
    y.append(range(10))
    xlim.append((-2,10))
    ylim.append((-2,10))
    if i%2==0: plot_type.append(plt.plot)
    else: plot_type.append(plt.stem)
rows = 2
cols = 3
join_vec = [1, (2, 3), 4, 5, 6]
numplot = 2
figplot(x, y, rows, cols, numplot, plot_type, xlim, ylim, xlabels, ylabels,
        join_vec=join_vec, show=False)

x = []
y = []
xlim = []
ylim = []
plot_type = []
xlabels = ['xlabel1', 'xlabel2', 'xlabel3']
ylabels = ['ylabel1', 'ylabel2', 'ylabel3']
for i in range(4):
    x.append(range(10))
    y.append(range(10))
    xlim.append((-2,10))
    ylim.append((-2,10))
    if i%2==0: plot_type.append(plt.plot)
    else: plot_type.append(plt.stem)
rows = 3
cols = 3
join_vec = [(1,6), 7,8,9]
numplot = 3
figplot(x, y, rows, cols, numplot, plot_type, xlim, ylim, xlabels, ylabels,
        join_vec=join_vec, show=True)
