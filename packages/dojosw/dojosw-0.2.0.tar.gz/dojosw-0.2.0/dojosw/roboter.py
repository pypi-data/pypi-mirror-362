from jupyturtle import Turtle

class Roboter:
    def __init__(self, *args, **kwargs):
        """Initialisiert den Roboter. """
        self.turtle = Turtle(*args, **kwargs)

    def vorwaerts(self, schritte):
        """Bewegt den Roboter vorwärts um die angegebene Anzahl von Schritten."""
        self.turtle.forward(schritte)

    def rueckwaerts(self, schritte):
        """Bewegt den Roboter rückwärts um die angegebene Anzahl von Schritten."""
        self.turtle.back(schritte)

    def links(self, winkel):
        """Dreht den Roboter nach links um den angegebenen Winkel."""
        self.turtle.left(winkel)

    def rechts(self, winkel):
        """Dreht den Roboter nach rechts um den angegebenen Winkel."""
        self.turtle.right(winkel)

    def gehe_zu(self, x, y):
        """Bewegt den Roboter zu den angegebenen Koordinaten (x, y)."""
        self.turtle.move_to(x, y)

    def sprung_zu(self, x, y):
        """Bewegt den Roboter zu den angegebenen Koordinaten (x, y) ohne eine Linie zu zeichnen."""
        self.turtle.jump_to(x, y)

    def stift_hoch(self):
        """Hebt den Stift an, sodass keine Linie gezeichnet wird."""
        self.turtle.pen_up()

    def stift_runter(self):
        """Senkt den Stift ab, sodass eine Linie gezeichnet wird."""
        self.turtle.pen_down()

    def zeichne(self):
        """Wird benötigt wenn Roboter mit Roboter(anmiate=False) initialisiert wird. Zeichnet die aktuelle Position des Roboters."""
        self.turtle.draw()

    @property
    def richtung(self):
        """Gibt die aktuelle Richtung des Roboters zurück."""
        return self.turtle.heading

    @property
    def x(self):
        """Gibt die aktuelle x-Position des Roboters zurück."""
        return self.turtle.x
    
    @property
    def y(self):
        """Gibt die aktuelle y-Position des Roboters zurück."""
        return self.turtle.y
    
    @property
    def position(self):
        """Gibt die aktuelle Position des Roboters als Tupel (x, y) zurück."""
        return self.turtle.x, self.turtle.y

