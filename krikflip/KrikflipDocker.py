import os
from pathlib import Path

from krita import DockWidget
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

DOCKER_TITLE = "Krikflip"

LN_TMIN = 0.0
LN_TMAX = 5.19295685089021
TIME_TICKS = [1, 2, 5, 10, 15, 30, 45, 60, 120, 180]
SLIDER_MAX = 99.0
BASE_E = 2.71828
INITIAL_SLIDER_VALUE = 49


class KrikflipDocker(DockWidget):
    """A Krita docker widget that provides canvas flipping functionality.

    This docker provides controls for automatically flipping the canvas at timed
    intervals, as well as manual flipping. It includes a slider for interval
    adjustment and audio feedback.

    Attributes:
        _running (bool): Flag indicating if auto-flip timer is active
        _count (int): Current countdown value in seconds
        _interval (int): Time between flips in minutes
    """

    _running = False
    _count = 0
    _interval = 60 * 15

    def __init__(self):
        """Initialize the docker widget with controls and timer."""
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        # Layout elements
        ourwidget = QWidget()
        box_buttons = QHBoxLayout()
        box_layout = QVBoxLayout()
        box_slider = QHBoxLayout()
        # Buttons
        button_flip = QPushButton("Flip now", self)
        button_flip.clicked.connect(self.flip)
        button_running = QPushButton("Stopped", self)
        button_running.setCheckable(True)
        button_running.clicked.connect(self.toggleRunning)
        # Slider component
        label_slider = QLabel("Test")
        slider_time = QSlider(orientation=QtCore.Qt.Horizontal)
        slider_time.valueChanged.connect(self.updateTime)
        # Layout
        box_buttons.addWidget(button_running)
        box_buttons.addWidget(button_flip)
        box_slider.addWidget(slider_time)
        box_slider.addWidget(label_slider)
        box_layout.addLayout(box_buttons)
        box_layout.addLayout(box_slider)
        ourwidget.setLayout(box_layout)
        self.label_slider = label_slider
        self.button_running = button_running
        self.button_flip = button_flip
        self.slider_time = slider_time
        # self.checkbox_chime = checkbox_chime
        self.setWidget(ourwidget)

        slider_time.setValue(INITIAL_SLIDER_VALUE)
        self.ourtimer = QTimer(interval=1000)
        self.ourtimer.timeout.connect(self.tick)
        self.resetCount()

    def toggleRunning(self) -> None:
        """Toggle the auto-flip timer between running and stopped states."""
        self._running = not self._running
        if self._running:
            self.button_running.setText("Running")
            self.ourtimer.start()
        else:
            self.button_running.setText("Stopped")
            self.button_flip.setText("Flip now")
            self.ourtimer.stop()
            self.resetCount()

    def resetCount(self) -> None:
        """Reset the countdown timer to the current interval value."""
        self._count = self._interval * 60

    def updateTime(self, value: int) -> None:
        """Update the flip interval based on slider value.

        Args:
            value: The raw slider value (0-99)
        """
        self._interval = self.scaleTime(value=value)
        self.label_slider.setText(f"{self._interval} {self.pluralise_time(v=self._interval)}")
        self.resetCount()

    @property
    def percentage_to_flip(self):
        return int(round(self._count / (self._interval * 60) * 100, 0))

    def tick(self) -> None:
        """Handle timer tick events, updating countdown and triggering flips."""
        self._count -= 1
        self.button_flip.setText(str(self._count))
        if self._count <= 5:
            self.button_flip.setText(str(self._count))
        else:
            self.button_flip.setText(f"{self.percentage_to_flip}%")
        if self._count == 0:
            self.flip()
            self.resetCount()

    def canvasChanged(self, canvas):
        pass

    @staticmethod
    def pluralise_time(v: int) -> str:
        """Return the plural or singular form of 'minute' based on value.

        Args:
            v: The number of minutes

        Returns:
            str: Either 'minute' or 'minutes'
        """
        if v == 0:
            return "minutes"
        elif v == 1:
            return "minute"
        else:
            return "minutes"

    @staticmethod
    def scaleTime(value: int) -> int:
        """Convert slider value to actual minutes using exponential scaling.

        Args:
            value: Raw slider value (0-99)

        Returns:
            int: Number of minutes for the interval
        """
        v = BASE_E ** ((value / SLIDER_MAX) * LN_TMAX)
        errors = {_: abs(v - _) for _ in TIME_TICKS}
        return sorted(errors.items(), key=lambda x: x[1])[0][0]

    def flip(self):
        """Toggle the canvas mirror state."""
        Krita.instance().views()[0].canvas().setMirror(not self.mirror)

    @property
    def mirror(self):
        """Get current mirror state of the canvas.

        Returns:
            bool: True if canvas is currently mirrored
        """
        return Krita.instance().views()[0].canvas().mirror()
