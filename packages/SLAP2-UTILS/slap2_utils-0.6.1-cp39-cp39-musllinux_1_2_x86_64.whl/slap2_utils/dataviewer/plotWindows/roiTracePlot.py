from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyneurotrace.gpu.filters as filters
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.cm as cm
import sys

from slap2_utils.functions.tracefunctions  import returnAllTrace, returnVolumeTrace


def plotROITrace(ax, dffData, hz, start, end, stim_times):#, y_min, y_max):
    ax.clear()
 
    time = np.arange(0, int(end - start) / hz, 1 / hz) + (start / hz)

    y_min, y_max = -.05, 1

    data_slice = dffData[start:end]
    if len(time) != len(data_slice):
            time = np.linspace(start / hz, end / hz, len(data_slice))

    _traceColor = mpl.colors.rgb2hex(cm.Spectral(1))

    if data_slice.size > 0:
        line, = ax.plot(time, data_slice, color=_traceColor, alpha=.8)

        y_max_slice = (data_slice + (.15)).max()
        if not np.isnan(y_max_slice) and not np.isinf(y_max_slice):
            y_max = max(y_max, y_max_slice)


    if y_min == float('inf') or y_max == float('-inf') or np.isnan(y_min) or np.isinf(y_min) or np.isnan(y_max) or np.isinf(y_max):
        y_min, y_max = -0.05, 1  # Default values if no valid data
    if stim_times is not None:        
        # Plot vertical lines for stim times
        for stim_time in stim_times[0]:
            if start / hz <= stim_time <= end / hz:  # Only plot if within the time window
                ax.axvline(x=stim_time, color='black', alpha=.5, linestyle='--', linewidth=1)
        for stim_time in stim_times[1]:
            if start / hz <= stim_time <= end / hz:  # Only plot if within the time window
                ax.axvline(x=stim_time, color='black', alpha=.5,linestyle='dotted', linewidth=1)
    ax.set_xlim(time[0], time[-1])
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Seconds")
    ax.set_ylabel("dF/F")
    ax.figure.canvas.draw()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)
        self.initialized = False

    def plot(self, dffData, hz, start, end, stim_time):
        if not self.initialized:
            self.initialize_plot(dffData, hz, start, end, stim_time)
        else:
            plotROITrace(self.ax, dffData, hz, start, end, stim_time)

    def initialize_plot(self, dffData, hz, start, end, stim_times):
        time = np.arange(0, int(end - start) / hz, 1 / hz) + (start+1 / hz)
        self.ax.clear()
        y_min, y_max = -0.05, 1
        
        data_slice = dffData[start:end]
        if len(time) != len(data_slice):
            time = np.linspace(start / hz, end / hz, len(data_slice))

        _traceColor = mpl.colors.rgb2hex(cm.Spectral(1))

        if data_slice.size > 0:
            line, = self.ax.plot(time, data_slice, color=_traceColor, alpha=.8)
            y_min_slice = (data_slice-.05).min()
            y_max_slice = (data_slice + (.15)).max()
            if not np.isnan(y_min_slice) and not np.isinf(y_min_slice):
                y_min = min(y_min, y_min_slice)
            if not np.isnan(y_max_slice) and not np.isinf(y_max_slice):
                y_max = max(y_max, y_max_slice)
        else:
            # Handle case where the slice is empty
            line, = self.ax.plot([], [], color=_traceColor, alpha=.8)
        self.ax.add_line(line)
        if y_min == float('inf') or y_max == float('-inf') or np.isnan(y_min) or np.isinf(y_min) or np.isnan(y_max) or np.isinf(y_max):
            y_min, y_max = -0.05, 1  # Default values if no valid data
        
        if stim_times is not None:        
            # Plot vertical lines for stim times
            for stim_time in stim_times[0]:
                if start / hz <= stim_time <= end / hz:  # Only plot if within the time window
                    self.ax.axvline(x=stim_time, color='black', alpha=.5, linestyle='--', linewidth=1)
            for stim_time in stim_times[1]:
                if start / hz <= stim_time <= end / hz:  # Only plot if within the time window
                    self.ax.axvline(x=stim_time, color='black', alpha=.35,linestyle='dotted', linewidth=1)

        self.ax.set_xlim(time[0], time[-1])
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlabel("Seconds")
        self.ax.set_ylabel("dF/F")
        self.initialized = True
        self.ax.figure.canvas.draw()

    def update_plot(self, dffData, hz, ix, window_size, stim_times):
        plotROITrace(self.ax, dffData, hz, ix, ix + window_size, stim_times)

class roiPlot(QMainWindow):
    def __init__(self, roi_index, channel, hdatafile, stimTimes):
        super().__init__()

        self.setWindowTitle(f"Plot for ROI {roi_index}")

        layout = QVBoxLayout()

        # Create a PlotCanvas instance
        self.canvas = PlotCanvas(self, width=24, height=16)
        layout.addWidget(self.canvas)

        self.z = hdatafile.fastZs.index(hdatafile.metaData.AcquisitionContainer.ROIs[roi_index].z)
        _, self.roiTrace = returnVolumeTrace(hdatafile, roi_index, channel)
        hz = self.roiTrace.shape[0] / hdatafile.metaData.acqDuration_s

        dffTraces = filters.deltaFOverF0(self.roiTrace, hz, .2, .10, 3)
        self.hz = hz
        self.dffTraces = dffTraces
        self.window_size = 500
        self.stimTimes = stimTimes
        self.canvas.plot(dffTraces, hz, 0, self.window_size, self.stimTimes)

        # Create a QSlider for updating frames
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setMaximum(dffTraces.shape[0] - self.window_size)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.update_frame)
        
        layout.addWidget(self.slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_frame(self, ix):
        self.canvas.update_plot(self.dffTraces, self.hz, ix, self.window_size, self.stimTimes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = roiPlot(roi_index=0, channel=1, hdatafile=None, stim_times=None)
    window.show()
    sys.exit(app.exec())
