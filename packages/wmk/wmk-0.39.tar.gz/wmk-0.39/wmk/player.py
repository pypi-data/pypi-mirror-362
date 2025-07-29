from collections.abc import Callable
from typing import Any

import pyglet


class Player(pyglet.window.Window):
    """A window class for displaying and controlling frame-based content using Pyglet.

    This class provides a window interface for rendering frames and handling user input,
    making it suitable for any application requiring frame-by-frame display with user interaction.

    The Player class manages:
        * Frame rendering with automatic scaling
        * Keyboard and mouse input handling
        * Window lifecycle management

    Example:
        Basic usage with a frame generator function::

            def generate_frames(player, dt):
                # Get current input state
                actions = create_actions_vector(player.keys_pressed, player.mouse_movement)

                # Create or return your frame using the actions vector
                frame = create_frame(actions)
                return frame

            # Create and run the player
            player = Player(
                frame_generator=generate_frames,
                fps_max=30,
                width=800,
                height=600,
                caption="My Player Window"
            )
            player.run()

    Args:
        frame_generator: Function that takes (player, dt) and returns a frame
        fps_max: Maximum frames per second (default: 30)
        fps_display: Whether to show FPS counter (default: False)
        mouse_sensitivity: Mouse movement multiplier (default: 1.0)
        **kwargs: Additional arguments passed to :class:`pyglet.window.Window`

    Note:
        The frame_generator function should return frames as numpy arrays in RGB format.
        Return None from the frame generator to gracefully exit the player.

    Attributes:
        keyboard_state (pyglet.window.key.KeyStateHandler): Key state handler for keyboard input
        mouse_state (pyglet.window.mouse.MouseStateHandler): Mouse state handler for mouse input
        keys_pressed (set): Set of keyboard and mouse keys pressed since the last update
        mouse_movement (dict): Dictionary of mouse movement deltas since the last update
        mouse_sensitivity (float): Mouse movement sensitivity multiplier
        is_playing (bool): Whether the player is currently running
    """

    def __init__(
        self,
        frame_generator: Callable[[Any, float], Any],
        fps_max: int = 30,
        fps_display: bool = False,
        mouse_sensitivity: float = 1.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        # Set background color to blue
        pyglet.gl.glClearColor(0, 0, 1, 1)

        self.frame_generator: Callable = frame_generator
        self.keyboard_state = pyglet.window.key.KeyStateHandler()
        self.mouse_state = pyglet.window.mouse.MouseStateHandler()
        self.keys_pressed = set()
        self.mouse_movement = {"dx": 0.0, "dy": 0.0}
        self.mouse_sensitivity: float = mouse_sensitivity
        self.is_playing: bool = False
        self.fps_max: float = fps_max
        if fps_display:
            self.fps_display = pyglet.window.FPSDisplay(window=self, samples=10)
        else:
            self.fps_display = None

        # Set up event handlers
        self.push_handlers(self.keyboard_state)
        self.push_handlers(self.mouse_state)
        self.set_handler("on_mouse_motion", self._handle_mouse_motion)
        self.set_handler("on_mouse_press", self._handle_mouse_press)
        self.set_handler("on_key_press", self._handle_key_press)
        self.set_handler("on_draw", self._handle_draw)

        # Set up the image data where our frame will be stored before drawing
        self.img: pyglet.image.ImageData | None = None

        # Store clock event for cleanup
        self._update_clock = pyglet.clock.schedule_interval(self.update, 1.0 / fps_max)

    def _handle_draw(self) -> None:
        """
        Handle window drawing events.
        """
        self.clear()

        # If we have an img it means we can draw it. We use the screen texture from pyglet directly https://pyglet.readthedocs.io/en/latest/modules/image/index.html#drawing-images
        if self.img:
            self.img.blit(0, 0, 0, self.width, self.height)

        if self.fps_display:
            self.fps_display.draw()

    def _handle_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """
        Handle mouse movement events.
        """
        self.mouse_movement["dx"] += dx * self.mouse_sensitivity
        self.mouse_movement["dy"] += dy * self.mouse_sensitivity

    def _handle_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        Handle mouse button press events.
        """
        self.keys_pressed.add(button)

    def _handle_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle keyboard key press events.
        """
        self.keys_pressed.add(symbol)

    def play(self) -> None:
        """
        Start the player and run the game loop.
        """
        self._reset_keys()
        self.is_playing = True

    def pause(self) -> None:
        """
        Pause the player and stop the game loop.
        """
        self.is_playing = False

    def _reset_keys(self) -> None:
        # Reset mouse movement
        self.mouse_movement["dx"] = 0
        self.mouse_movement["dy"] = 0

        # Reset keys pressed
        keys_pressed = self.keys_pressed
        self.keys_pressed = set()
        for key in keys_pressed:
            if self.keyboard_state[key] or self.mouse_state[key]:
                self.keys_pressed.add(key)
        del keys_pressed

    def update(self, dt: float) -> None:
        """
        Update the window state and content.

        Called periodically based on fps_max setting. Generates new frames
        and updates input states.

        Args:
            dt: Time elapsed since last update in seconds
        """
        if not self.is_playing:
            return

        frame = self.frame_generator(self, dt)
        if frame is None:
            pyglet.app.exit()
            return

        self._reset_keys()

        # Convert numpy array to pyglet image. We avoid using sprites since it was causing a gpu memory leak https://waltzbinaire.slack.com/archives/C07SZ7T7MQA/p1739889085928039?thread_ts=1739866903.620719&cid=C07SZ7T7MQA
        height, width = frame.shape[:2]
        self.img = pyglet.image.ImageData(width, height, "RGB", frame.tobytes())

    def close(self) -> None:
        """
        Clean up resources used by the player.

        This method should be called when the player is no longer needed.

        :inherited: from :class:`pyglet.window.Window`
        """
        if self._update_clock:
            pyglet.clock.unschedule(self._update_clock)

        if self.fps_display:
            self.fps_display = None

        # Remove event handlers
        self.img = None
        self.remove_handlers(self.keyboard_state)
        self.remove_handlers(self.mouse_state)

        super().close()

    def __del__(self) -> None:
        """Ensure resources are cleaned up when the object is deleted."""
        self.close()

    def run(self, is_paused: bool = False) -> bool:
        """
        Run the game window and start the game loop.
        Activates the window, sets exclusive mouse mode, and starts the game loop using
        pyglet's application runner.
        If pause is True, the player will be paused before
        starting the game loop.
        The window will be closed and False returned when
        the game loop ends or if an exception occurs.

        Args:
            pause: Whether to pause the player before starting the game loop (default: False)

        Returns:
            bool: False after the game loop ends.

        Note:
            Setting exclusive mouse mode captures the mouse pointer within the game window.

        :inherited: from :class:`pyglet.window.Window`
        """
        try:
            self.activate()
            self.set_exclusive_mouse(True)
            if not is_paused:
                self.play()
            pyglet.app.run()
        finally:
            self.close()
            return False
