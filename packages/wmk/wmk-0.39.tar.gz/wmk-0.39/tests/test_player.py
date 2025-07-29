import unittest
from unittest.mock import Mock, patch

import numpy as np
import pyglet

from wmk.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.frame_generator = Mock(return_value=self.mock_frame)
        self.player = Player(frame_generator=self.frame_generator, width=800, height=600)

    def test_player_initialization(self) -> None:
        self.assertEqual(self.player.width, 800)
        self.assertEqual(self.player.height, 600)
        self.assertEqual(self.player.fps_max, 30)
        self.assertEqual(self.player.mouse_sensitivity, 1.0)
        self.assertIsInstance(self.player.keyboard_state, pyglet.window.key.KeyStateHandler)
        self.assertIsInstance(self.player.mouse_state, pyglet.window.mouse.MouseStateHandler)
        self.assertEqual(self.player.mouse_movement, {"dx": 0.0, "dy": 0.0})

    def test_player_initialization_with_custom_params(self) -> None:
        player = Player(
            frame_generator=self.frame_generator,
            width=1024,
            height=768,
            fps_max=60,
            mouse_sensitivity=2.0,
        )
        self.assertEqual(player.fps_max, 60)
        self.assertEqual(player.mouse_sensitivity, 2.0)
        player.close()

    def test_update(self) -> None:
        self.player.play()
        self.player.update(1 / 30)
        self.frame_generator.assert_called_once_with(self.player, 1 / 30)
        self.assertIsNotNone(self.player.img)

    @patch("pyglet.app.exit")
    def test_update_exits_on_none_frame(self, mock_exit: Mock) -> None:
        self.player.play()
        self.frame_generator.return_value = None
        self.player.update(1 / 30)
        mock_exit.assert_called_once()

    def test_handle_mouse_motion(self) -> None:
        self.player._handle_mouse_motion(10, 20, 30, 40)
        self.assertEqual(self.player.mouse_movement, {"dx": 30.0, "dy": 40.0})

    @patch("pyglet.app.run")
    def test_run(self, mock_run: Mock) -> None:
        result = self.player.run()
        mock_run.assert_called_once()
        self.assertFalse(result)

    @patch("pyglet.app.run")
    def test_run_paused(self, mock_run: Mock) -> None:
        result = self.player.run(is_paused=True)
        mock_run.assert_called_once()
        self.assertFalse(result)
        self.assertFalse(self.player.is_playing)

    def test_handle_key_press(self) -> None:
        self.player._handle_key_press(pyglet.window.key.A, 0)
        self.assertIn(pyglet.window.key.A, self.player.keys_pressed)

    def test_handle_mouse_press(self) -> None:
        self.player._handle_mouse_press(100, 100, pyglet.window.mouse.LEFT, 0)
        self.assertIn(pyglet.window.mouse.LEFT, self.player.keys_pressed)

    def test_update_removes_released_keys(self) -> None:
        self.player.keys_pressed.add(pyglet.window.key.A)
        self.player.play()
        self.player.update(1 / 30)
        self.assertNotIn(pyglet.window.key.A, self.player.keys_pressed)

    def test_update_resets_mouse_movement(self) -> None:
        self.player.play()
        self.player.mouse_movement = {"dx": 10.0, "dy": 20.0}
        self.player.update(1 / 30)
        self.assertEqual(self.player.mouse_movement, {"dx": 0.0, "dy": 0.0})

    def test_play_pause(self) -> None:
        self.assertFalse(self.player.is_playing)
        self.player.play()
        self.assertTrue(self.player.is_playing)
        self.player.pause()
        self.assertFalse(self.player.is_playing)

    def test_fps_display(self) -> None:
        player = Player(frame_generator=self.frame_generator, fps_display=True)
        self.assertIsNotNone(player.fps_display)
        player.close()

        player = Player(frame_generator=self.frame_generator, fps_display=False)
        self.assertIsNone(player.fps_display)
        player.close()

    def test_close_cleanup(self) -> None:
        # Setup initial state
        self.player.play()
        self.player.update(1 / 30)  # Create img
        self.assertIsNotNone(self.player.img)

        # Close and verify cleanup
        self.player.close()
        self.assertIsNone(self.player.img)
        self.assertIsNone(self.player.fps_display)

    def test_update_paused(self) -> None:
        self.player.pause()
        initial_img = self.player.img
        self.player.update(1 / 30)
        self.assertEqual(self.frame_generator.call_count, 0)
        self.assertEqual(self.player.img, initial_img)

    def tearDown(self) -> None:
        self.player.close()

    def test_update_sets_image_data(self):
        # Create a test frame
        test_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.frame_generator.return_value = test_frame

        # Update the player
        self.player.play()
        self.player.update(1 / 30.0)

        # Check that img was created
        self.assertIsNotNone(self.player.img)
        self.assertEqual(self.player.img.width, 100)
        self.assertEqual(self.player.img.height, 100)

    def test_update_none_frame_exits(self):
        # Setup frame generator to return None
        self.frame_generator.return_value = None

        with patch("pyglet.app.exit") as mock_exit:
            self.player.play()
            self.player.update(1 / 30.0)
            mock_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
