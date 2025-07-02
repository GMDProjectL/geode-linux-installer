from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QEvent, QPoint, QRect

from PySide6.QtCore import QElapsedTimer, QTimer, QObject, Signal, Slot, QThread

import random

class SwelvyBG(QWidget):
    layers: list[tuple[QPixmap, float, float]] = []

    def __init__ (self, parent=None):
        super().__init__(parent=parent)

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer3.png"), QColor(244, 212, 142)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer0.png"), QColor(245, 174, 125)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer1.png"), QColor(236, 137, 124)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer2.png"), QColor(213, 105, 133)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer1.png"), QColor(173, 84,  146)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))

        self.layers.append((
            self.colorizePixmap(QPixmap("assets/swelvy/swelve-layer0.png"), QColor(113, 74,  154)),
            random.choice([-1, 1]) * random.uniform(3, 9), 0
        ))
        
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        if parent:
            self.resize(parent.size())
            parent.installEventFilter(self)
        
        self.worker = SwelvyWorker()
        self.workerThread = QThread()
        self.workerThread.setObjectName("Swelvy Worker")
        self.worker.moveToThread(self.workerThread)
        self.worker.frame.connect(self.on_frame)
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.start()

    def eventFilter(self, obj: QObject, event: QEvent):
        # Resize background widget when parent resizes
        if obj == self.parent() and event.type() == QEvent.Type.Resize:
            self.resize(obj.size())
        return super().eventFilter(obj, event)
    
    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        for count, (layer, speed, x) in enumerate(self.layers):
            y = (self.height() / len(self.layers)) * count
            if count > 0:
                y -= layer.height() / 6

            w = layer.width()

            int_x = int(x)

            if speed > 0:
                painter.drawPixmap(QPoint(x, int(y)), layer)
                painter.drawPixmap(QPoint(int_x + w, int(y)), layer)
            else:
                painter.drawPixmap(QPoint(int_x - w, int(y)), layer)
                painter.drawPixmap(QPoint(x, int(y)), layer)

    @Slot(float)
    def on_frame(self, dt: float):
        for count, (layer, speed, x) in enumerate(self.layers):
            x -= speed * dt
            w = layer.width()
            
            if speed > 0 and x > w:
                x -= w
            elif speed < 0 and x < 0:
                x += w
            
            self.layers[count] = (layer, speed, x)
        self.update()

    @staticmethod
    def colorizePixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
        result = QPixmap(pixmap.size())
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(result.rect(), color)
        painter.end()

        return result


class SwelvyWorker(QObject):
    frame = Signal(float)

    def __init__(self):
        super().__init__()
        self._running = True


    def run(self):
        import time
        last = time.time()
        while self._running:
            now = time.time()
            dt = now - last
            last = now

            self.frame.emit(dt)
            time.sleep(1 / 60)
    
    def stop(self):
        self._running = False