import threading
import time
from typing import Sequence

import cv2
import numpy as np
from mss import mss
from pyautogui import Point, position
from pyglet import media

from .settings import Config, set_config_file


class OverviewCommand:
    def __init__(self, config: Config) -> None:
        self.thread: threading.Thread | None = None
        self.config = config

    def run(self) -> None:
        monitor = self._get_monitor_positions()
        self._run_watcher(monitor)

    def _get_monitor_positions(self) -> tuple[int]:
        if (
            not self.config.upper_left_position
            and not self.config.lower_right_position
        ):
            positions = self._get_overview_position()
            set_config_file(
                [
                    [
                        'upper_left_position',
                        f'{positions[0].x},{positions[0].y}',
                    ],
                    [
                        'lower_right_position',
                        f'{positions[1].x},{positions[1].y}',
                    ],
                ]
            )
            monitor = (
                positions[0].x,
                positions[0].y,
                positions[1].x,
                positions[1].y,
            )
        else:
            upper_left = tuple(
                map(int, self.config.upper_left_position.split(','))
            )
            lower_right = tuple(
                map(int, self.config.lower_right_position.split(','))
            )
            monitor = upper_left + lower_right  # type: ignore[assignment]
        return monitor  # type: ignore[return-value]

    @staticmethod
    def _get_overview_position() -> Sequence[Point]:
        overview_position = []
        for side in ['верхний левый', 'нижний правый']:
            input(
                f'Прицельтесь на {side} угол овервью '
                'и после нажмите в самом приложении Enter'
            )
            overview_position.append(position())
        return overview_position

    def _run_watcher(self, monitor: tuple[int]) -> None:
        while True:
            with mss() as sct:
                image = np.array(sct.grab(monitor))
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower_color = np.array([0, 50, 50])
            upper_color = np.array([10, 255, 255])
            mask = cv2.inRange(hsv_image, lower_color, upper_color)

            moments = cv2.moments(mask, True)
            if moments['m00']:
                self._alert_signal()

            cv2.imshow('Debug-Mode', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def _alert_signal(self) -> None:
        if not self.thread:
            self.thread = threading.Thread(target=self._run_media)
            self.thread.start()

    def _run_media(self) -> None:
        print('Обнаружен корабль!')
        sound = media.load(self.config.alert_sound, streaming=False)
        sound.play()
        time.sleep(5)
        self.thread = None
