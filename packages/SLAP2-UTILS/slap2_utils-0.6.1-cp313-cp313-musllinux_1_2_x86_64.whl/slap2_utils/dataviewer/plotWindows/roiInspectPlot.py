from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyneurotrace.gpu.filters as filters
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import sys
import json
from tifffile import imread, tiffcomment
from slap2_utils.utils.roi_utils import roiLabels


def plotROI(ax, labels, stack, z, z_positions):
    ax.clear()

    # Determine what to show as background
    if stack is not None:
        if stack.ndim == 4:  # (channel, z, y, x)
            frame = stack[0, z, :, :]
        elif stack.ndim == 3:  # (z, y, x)
            frame = stack[z, :, :]
        elif stack.ndim == 2:  # (y, x)
            frame = stack
        else:
            raise ValueError(f"Unsupported stack shape: {stack.shape}")
    else:
        frame = np.zeros(labels[z, :, :].shape)

    ax.imshow(frame, cmap='gray')
    # Create contours from ROI labels and plot them
    # Normalize the labels to create a color map
    norm = mpl.colors.Normalize(vmin=1, vmax=np.max(labels))
    cmap = cm.Spectral

    # Create contours from ROI labels and color them based on integer values
    unique_labels = np.unique(labels[z, :, :])
    for i in unique_labels:
        if i == 0:
            continue  # Skip background
        mask = labels[z, :, :] == i
        color = cmap(norm(i))
        ax.contour(mask, levels=[0.5], colors=[color], linewidths=1)

        # Find the centroid of the mask to place the label
        if np.any(mask):
            y, x = np.mean(np.argwhere(mask), axis=0)
            ax.text(x, y, str(i), color='white', fontsize=8, ha='center', va='center', weight='bold')

    # Add Z-position text in the lower-left corner
    if stack is not None:
        z_position_text = f"Z: {z_positions[z]:.2f} µm"  # Skip the first value in z_positions
    else:
        z_position_text = f"Z: {z_positions[z]:.2f} µm"  # Skip the first value in z_positions
    
    ax.text(0.02, 0.02, z_position_text, color='white', fontsize=10, ha='left', va='bottom', transform=ax.transAxes)


    ax.set_xticks([])
    ax.set_yticks([])
    ax.figure.canvas.draw()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)
        self.initialized = False

    def plot(self, labels, stack, z_positions):
        if not self.initialized:
            self.initialize_plot(labels, stack, z_positions)
        else:
            plotROI(self.ax, labels, stack, 0, z_positions)

    def initialize_plot(self, labels, stack, z_positions):
        _z =0
        plotROI(self.ax, labels, stack, _z, z_positions)
   
        self.ax.figure.canvas.draw()

    def update_plot(self, labels, stack, z, z_positions):
        plotROI(self.ax, labels, stack, z, z_positions)

class roiViewer(QMainWindow):
    def __init__(self, channel, hdatafile, imgPath):
        super().__init__()

        self.setWindowTitle(f"ROI Inspector")

        layout = QVBoxLayout()

        # Create a PlotCanvas instance
        self.canvas = PlotCanvas(self, width=24, height=16)
        layout.addWidget(self.canvas)
        if imgPath == None:
            self.img = None
        else:
            self.img = imread(imgPath)
        
        self.labels = roiLabels(hdatafile, imgPath)

        if imgPath == None:
            self.z_positions = hdatafile.fastZs[1:]
        else:
            _stackData = tiffcomment(imgPath)
            _stackInfo = json.loads(_stackData)
            self.z_positions = _stackInfo['zsAbsolute']
            
        self.canvas.plot(self.labels, self.img, self.z_positions)

        # Create a QSlider for updating frames
        if imgPath == None:
            if len(hdatafile.fastZs) > 2:
            
                self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
                self.slider.setMaximum(len(hdatafile.fastZs)-2)
                self.slider.setMinimum(0)
                self.slider.valueChanged.connect(self.update_frame)
                layout.addWidget(self.slider)

        else:
            z = self.img.shape[1]
            if z > 1:
                self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
                self.slider.setMaximum(z-1)
                self.slider.setMinimum(0)
                self.slider.valueChanged.connect(self.update_frame)
                layout.addWidget(self.slider)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def update_frame(self, z):
        self.canvas.update_plot(self.labels, self.img, z, self.z_positions)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = superPixelPlot(roi_index=0, channel=1, hdatafile=None, stim_times=None)
    window.show()
    sys.exit(app.exec())
