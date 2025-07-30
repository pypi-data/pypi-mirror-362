import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

def plot_set(obj, vals, range, select = {}, title = "", hide_endpoints = False):
    '''
    visualize, change and select points for each plot defined by each dict (key, value) pair
    :param obj: dtw obj where results are stored dynamically
    :param vals: dict with data values. Each (key, value) pair represents one subplot. The keys are attribute names of obj.
    :param range: list of lists where each sublist holds the minimum and maximun range value for each subplot.
    :param select: dict with selected/flagged data points. The keys are attribute names of obj.
    :return:
    '''
    def button_press_callback(event):
        'whenever a mouse button is pressed'
        if event.inaxes is None: #mouse not over an axes
            return
        if event.button == 1 or event.button == 3: #left or right mouse button
            for i in np.arange(N_plots):
                idx[i] = get_idx_under_point(event, axes[i], vals[keys[i]])
            if event.button == 3:
                #color selected points red
                id_plot = np.argwhere(idx != None)
                if len(id_plot) != 0 and id_plot < len(select_keys):
                    id_plot = id_plot.flatten()[0]
                    idx_sel = idx[id_plot]
                    fc = plots_select[id_plot].get_facecolors()
                    fc[idx_sel,0] = 1-fc[idx_sel,0] #convert 1 to 0 and 0 to 1
                    plots_select[id_plot].set_facecolors(fc)
                    select_key = select_keys[id_plot]
                    select[select_key] = np.argwhere(fc[:,0] == 1).flatten() #update selection array
                    setattr(obj, select_key, select[select_key].copy())

    def button_release_callback(event):
        'whenever a mouse button is released'
        if event.button != 1:
            return
        
        for key in keys:
            setattr(obj, key, vals[key].copy())
            if hide_endpoints:
                obj.set_endpoints()

        for i in np.arange(N_plots):
            idx[i] = None

    def get_idx_under_point(event, ax, yvals):
        'get the index of the vertex under point if within epsilon tolerance'
        t = ax.transData.inverted()
        tinv = ax.transData
        xy = t.transform([event.x, event.y])
        xr = np.reshape(x, (np.shape(x)[0], 1))
        yr = np.reshape(yvals, (np.shape(yvals)[0], 1))
        xy_vals = np.append(xr, yr, 1)
        xyt = tinv.transform(xy_vals)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.hypot(xt - event.x, yt - event.y)
        idx_seq, = np.nonzero(d == d.min())
        idx = idx_seq[0]

        if d[idx] >= epsilon:
            idx = None

        return idx

    def motion_notify_callback(event):
        'on mouse movement'
        id_plot = np.argwhere(idx != None)
        if len(id_plot) == 0:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        id_plot = id_plot.flatten()[0]

        yvals = vals[keys[id_plot]]

        idx_sel = idx[id_plot]
        if yvals.dtype == int:
            yvals[idx_sel] = int(event.ydata)
        else:
            yvals[idx_sel] = event.ydata

        ymin = range[id_plot][0]
        ymax = range[id_plot][1]
        yvals = np.where(yvals > ymax, ymax, yvals)
        yvals = np.where(yvals < ymin, ymin, yvals)

        vals[keys[id_plot]] = yvals.copy()
        plots[id_plot].set_ydata(yvals)
        plots_select[id_plot].set_offsets(np.c_[np.arange(len(yvals)), yvals])
        fig.canvas.draw_idle()

    keys = list(vals.keys())
    select_keys = list(select.keys())
    N = len(vals[keys[0]])
    N_plots = len(vals)

    idx = np.array([None for i in np.arange(N_plots)]) #x-index corresponding with cursor for each plot.
    epsilon = 10  # max pixel distance

    # figure.subplot.right
    mpl.rcParams['figure.subplot.right'] = 0.9
    #set up a plot
    fig, axes = plt.subplots(N_plots, 1, figsize=(9.0, 8.0), sharex=True)
    fig.suptitle(title, fontsize=12,horizontalalignment='center')
    fig.subplots_adjust(top=0.88)
    #fig.tight_layout()
    plots = []
    plots_select = []

    x = np.arange(N)
    xmin = x[0] #x-axis min
    xmax = x[-1] #x-axis max

    if hide_endpoints == True:
        xmin = x[1] #x-axis min
        xmax = x[-2] #x-axis max
    xplus = 0.02 #x-axis margin
    yplus = 0.1 #y-axis margin

    for i,key in enumerate(keys):
        #set axes
        p1, = axes[i].plot(x, vals[key], color='black', linestyle='solid', marker='o', markersize=9, zorder = 1) #, color='k'
        color_select = np.zeros(N)
        if i < len(select_keys):
            select_key = select_keys[i]
            for el in select[select_key]: color_select[el] = 1
        colors = np.c_[color_select, np.zeros(N), np.zeros(N), np.ones(N)]
        p2 = axes[i].scatter(x,vals[key] ,edgecolors = None, facecolors = colors,zorder=2, s = 100)#,color = 'r', linestyle='', marker='o', markersize=10)
        plots.append(p1)
        plots_select.append(p2)
        #set bounds
        axes[i].set_yscale('linear')
        ymin = range[i][0]
        ymax = range[i][1]
        axes[i].set_ylim(ymin - yplus*(ymax-ymin), ymax + yplus*(ymax-ymin))
        axes[i].set_xlim(xmin - xplus*(xmax-xmin), xmax + xplus*(xmax-xmin))
        #set additional plot properties
        axes[i].set_ylabel(key)
        axes[i].grid(True)
        axes[i].yaxis.grid(True, which='minor', linestyle='--')

    #connect
    fig.canvas.mpl_connect('button_press_event', button_press_callback)
    fig.canvas.mpl_connect('button_release_event', button_release_callback)
    fig.canvas.mpl_connect('motion_notify_event', motion_notify_callback)

    #try:
    #    while fig.number in plt.get_fignums():
    #        plt.pause(2)
    #except:
    #    plt.close(fig.number)

    return vals, range, select

if __name__ == "__main__":
    None

