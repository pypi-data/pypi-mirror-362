from vispy import app
app.use_app('pyqt6')

import sys
import tifffile
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt6.QtCore import Qt
from vispy import scene
from vispy.color import Colormap
from vispy.scene import visuals
from matplotlib import cm
from slap2_utils.utils.roi_utils import roiLabels


class ROIViewer3D(QMainWindow):
    def __init__(self, img_path, hdatafile):
        super().__init__()

        self.setWindowTitle("3D ROI Viewer")
        print(img_path)
        # Load the image stack if provided
        self.img = tifffile.imread(img_path) if img_path !=None else None
        
        if self.img is not None:
            if self.img.ndim == 4:
                # Shape: (C, Z, Y, X) or (T, Z, Y, X) — select first channel/timepoint
                self.volume_data = self.img[0, :, :, :].astype('float32')
            elif self.img.ndim == 3:
                # Shape: (Z, Y, X)
                self.volume_data = self.img.astype('float32')
            else:
                raise ValueError(f"Unexpected image dimensions: {self.img.shape}")

        # Create a Vispy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()

        # Initial grayscale colormap
        self.gamma = 1.0  # Initial gamma value
        gamma_corrected = lambda x: x ** self.gamma
        self.grayscale_cmap = Colormap([(gamma_corrected(0), gamma_corrected(0), gamma_corrected(0)), 
                                        (gamma_corrected(1), gamma_corrected(1), gamma_corrected(1))])

        self.labels = roiLabels(hdatafile, img_path).astype('float32')
     
        label_min = np.min(self.labels[self.labels > 0]) 
        label_max = np.max(self.labels)
        normalized_labels = (self.labels - label_min) / (label_max - label_min)

        # Generate a colormap for the labels based on the spectral colormap
        spectral_cmap = cm.Spectral(np.linspace(0, 1, len(np.unique(normalized_labels))))
        label_cmap = Colormap([(0, 0, 0, 0)] + [tuple(c) for c in spectral_cmap])

        if self.img is not None:

            # Add the volume with the grayscale colormap
            self.volume = visuals.Volume(self.volume_data,
                                        parent=self.view.scene,
                                        threshold=0.225,
                                        gamma=.5,
                                        cmap=self.grayscale_cmap,
                                        clim=[np.min(self.volume_data), np.max(self.volume_data)],
                                        method='mip')

        # Render the ROIs using Volume with a custom colormap
        self.roi_volume = visuals.Volume(self.labels,
                                        parent=self.view.scene,
                                        threshold=0.5,
                                        cmap=label_cmap,
                                        clim=[0, 1], #clim=[np.min(unique_labels), np.max(unique_labels)],
                                        method='translucent')

        # Set the camera to view the volume
        self.view.camera = scene.cameras.TurntableCamera(fov=60, azimuth=180)

        # Embed the Vispy canvas into the Qt layout
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(self.canvas.native)
        if self.img is not None:
            # Add a gamma slider
            self.gamma_slider = QSlider(Qt.Orientation.Horizontal)
            self.gamma_slider.setMinimum(0)
            self.gamma_slider.setMaximum(200)
            self.gamma_slider.setValue(100)  # Initial value corresponds to gamma=1.0
            self.gamma_slider.valueChanged.connect(self.update_gamma)

            layout.addWidget(self.gamma_slider)
        self.setCentralWidget(widget)

 

    def update_gamma(self, value):
        """Update gamma value based on the slider position and re-render the volume."""
        self.gamma = value / 100.0  # Convert slider value to gamma (0.01 to 2.0 range)
        self.volume.gamma = self.gamma
        self.volume.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Provide the correct arguments to the ROIViewer3D
    img_path = "Haase_MRT_tfl3d1.tif"  # Replace with actual path
    hdatafile = "path_to_your_datafile"  # Replace with actual datafile object

    window = ROIViewer3D(img_path, hdatafile)
    window.show()

    # Start the Qt event loop
    sys.exit(app.exec())