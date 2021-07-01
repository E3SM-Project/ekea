"""Kernel Timing Plotting


top: type of plotting
y axis: mpi-openmp group
x axis: invocation group
"""

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, MultiSelect, Select, Div
from bokeh.plotting import figure

import os, json
import numpy as np
import pandas as pd

with open("model.json") as f:
    jmodel = json.load(f)

source = ColumnDataSource(data=dict(top=[], left=[], right=[]))

kplot = figure()
kplot.y_range.start = 0
kplot.quad(top="top", bottom=0, left="left", right="right", source=source)

procs = ["All"]
invokes = ["All"]
plots = ["Elapsed Times", "Alignment"]

labels = {
    "xlabel" : {
        plots[0] : "elapsed time (sec)",
        plots[1] : "Time deviation from the average (sec)"
    },

    "ylabel" : {
        plots[0] : "frequency",
        plots[1] : "frequency"
    }
}

for mpi, d1 in jmodel["etime"].items():
    if not mpi.isnumeric():
        continue

    for omp, d2 in d1.items():
        ylabel = mpi+"."+omp

        if ylabel not in procs:
            procs.append(ylabel)

        for invoke in d2.keys():
            if invoke not in invokes:
                invokes.append(invoke)

sel_procs = MultiSelect(title="Select MPI.OpenMP", options=procs, value=["All"])
sel_plots = Select(title="Select Plot Type", options=plots, value=plots[0])
sel_invokes = MultiSelect(title="Select invokes", options=invokes, value=["All"])

src = pd.read_json("model.json")

summary = src.loc["_summary_"]
src = src.drop(labels=["_summary_"])


def select_timings():

    sel_plot = sel_plots.value
    sel_proc = sel_procs.value
    sel_invoke = sel_invokes.value

    min_etime = 10E10
    max_etime = 0.0
    resolution = None

    vals = []
    vallist = []
    valdict = {}

    for mpi, d1 in jmodel["etime"].items():
        if not mpi.isnumeric():
            continue

        for omp, d2 in d1.items():

            ylabel = mpi+"."+omp

            if "All" not in sel_proc and ylabel not in sel_proc:
                continue

            for invoke in sorted(d2.keys(), key=int):

                if "All" not in sel_invoke and invoke not in sel_invoke:
                    continue

                interval = tuple(float(v) for v in d2[invoke])

                if interval[0] < min_etime:
                    min_etime = interval[0]

                if interval[1] < max_etime:
                    max_etime = interval[1]

                if sel_plot == plots[0]:
                    vallist.append(abs(interval[0] - interval[1]))

                elif sel_plot == plots[1]:
                    if invoke not in valdict:
                        valdict[invoke] = []
                    
                    valdict[invoke].append(interval[0])

    if sel_plot == plots[0]:
        vals = vallist

    elif sel_plot == plots[1]:
        for invoke, stimes in valdict.items():
            valavg = sum(stimes) / float(len(stimes))
            vals.extend([s - valavg for s in stimes])
            
    x_name = labels["xlabel"][sel_plot]
    y_name = labels["ylabel"][sel_plot]

    return vals, x_name, y_name


def update():

    vals, x_name, y_name = select_timings()

    top, edges = np.histogram(vals, density=True, bins=min(100, len(vals)))
    #x_name = "elapsed time(sec)"
    #y_name = "frequency"

    kplot.xaxis.axis_label = x_name
    kplot.yaxis.axis_label = y_name
    kplot.title.text = ""

    source.data = dict(
        top= top,
        left= edges[:-1],
        right= edges[1:]
    )

desc = Div(text=open(os.path.join(os.path.dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

controls = [sel_procs, sel_invokes, sel_plots]

for control in controls:
    control.on_change("value", lambda attr, old, new: update())

root = column(desc, row(sel_procs, column(sel_plots, kplot, sel_invokes)))

update()

curdoc().add_root(root)
curdoc().title = "Kernel Timing"
