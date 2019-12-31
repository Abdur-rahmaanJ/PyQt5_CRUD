import os
import sys

from PyQt5 import QtWidgets

def app_path(path):
    frozen = 'not'
    if getattr(sys, 'frozen', False):
            # we are running in executable mode
            frozen = 'ever so'
            app_dir = sys._MEIPASS
    else:
            # we are running in a normal Python environment
            app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, path)


def layout_addWidget(layout, widgets):
    '''adds widgets to layouts'''

    for widget in widgets:
        if isinstance(layout, QtWidgets.QGridLayout):
            layout.addWidget(widget[0], widget[1], widget[2])
        else:
            layout.addWidget(widget)