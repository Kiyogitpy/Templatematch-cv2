import cv2
import numpy as np
from mss import mss
import PyQt5 as qt
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import time

def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"{func.__name__} took {elapsed:.5f} seconds to run.")
        return result
    return wrapper

@elapsed_time
class overlay(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)
        self.rect_coords = None
        # Setting up a QTimer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_rectangle)
        self.timer.start(0) 

    def update_rectangle(self):
        print("Checking for template..."
        coords = find_template_on_screen("template.png")
        if coords:
            self.draw_red_rect(*coords)


    def draw_red_rect(self, x, y, w, h):
        self.rect_coords = (x, y, w, h)
        self.update()

    def paintEvent(self, event):
        if self.rect_coords:
            print("Drawing rectangle...")
            x, y, w, h = self.rect_coords
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 3))
            painter.drawRect(x, y, w, h)
            painter.end()
@elapsed_time
def fast_screenshot():
    """Capture the whole screen using mss and convert it to an array."""
    with mss() as sct:
        monitor = sct.monitors[2]  
        sct_img = sct.grab(monitor)
        return np.array(sct_img)

@elapsed_time
def find_template_on_screen(template, threshold=0.6):
    """
    Find a template on the screen and return the coordinates of the top left corner
    """
    img = fast_screenshot() 
    cv2.imwrite("captured_screenshot.png", img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    template = cv2.imread(template)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    if len(loc[0]) == 0:
        print("No match found.") 
        return None
    else:
        print(f"Found match at: {loc[1][0], loc[0][0], template.shape[1], template.shape[0]}")  
        return loc[1][0], loc[0][0], template.shape[1], template.shape[0]


        
if __name__ == "__main__":
    app = qtw.QApplication([])
    o = overlay()
    o.show() 
    app.exec_()
