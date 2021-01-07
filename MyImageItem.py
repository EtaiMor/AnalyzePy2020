import pyqtgraph as pg

class MyImageItem(pg.ImageItem):
    def __init__(self, image=None, **kargs):
        super().__init__(image, **kargs)
        self.signal_mouseClickEvent = None


    def attach_mouseClickEvent(self, event_func):
        self.signal_mouseClickEvent = event_func

    def mouseClickEvent(self, event):
        self.signal_mouseClickEvent(event)


        print(pos_str)

