from kivy_garden.mapview import MapMarker
from kivy.animation import Animation

class GpsBlinker(MapMarker):
    """
    A class that represents a GPS marker on a map with a blinking animation.

    Attributes:
        default_blink_size (int): The default size of the blinking marker.
        outer_opacity (float): The opacity level of the outer part of the marker.
        blink_size (int): The current size of the blinking marker.
    """
    def blink(self):
        """
        Initiates a blinking animation for the GPS marker.

        The animation changes the marker's size and opacity over a duration of one second.
        Upon completion, it resets the animation and restarts it.
        """
        # Animation to change the blinker size and opacity
        anim = Animation(outer_opacity=0, blink_size=50, duration=1)
        # When the animation completes, reset the animation and call it again
        anim.bind(on_complete=self.reset)
        anim.start(self)

    def reset(self, *args):
        """
        Resets the GPS marker's properties to their default values and restarts the blink animation.

        Args:
            *args: Additional arguments passed by the animation's on_complete event.
        """
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()