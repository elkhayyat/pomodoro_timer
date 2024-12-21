import json
import os
import threading
import time

import pygame
import rumps
from PyQt5.QtWidgets import QApplication

from src.settings import SettingsWindow


class PomodoroTimerStatusBarApp(rumps.App):
    def __init__(self):
        super(PomodoroTimerStatusBarApp, self).__init__("PomodoroTimer App", icon="assets/icon.png")
        self.work_time = 1500  # 25 minutes
        self.rest_time = 300  # 5 minutes
        self.sound_file = "assets/alarm.mp3"
        self.load_settings()
        self.timer_thread = None
        self.remaining_time = self.work_time
        self.is_working = True
        self.is_running = False
        self.is_playing_sound = False
        self.sound_thread = None
        pygame.mixer.init()
        self.menu.add(rumps.MenuItem("Start", callback=self.start))
        self.menu.add(rumps.MenuItem("Pause", callback=self.pause))
        self.menu.add(rumps.MenuItem("Reset", callback=self.reset))
        self.menu.add(rumps.MenuItem("Rest", callback=self.rest))
        self.menu.add(None)  # Separator
        self.menu.add(rumps.MenuItem("Settings", callback=self._handle_settings))

    def on_tick(self):
        while self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.title = self.format_time(self.remaining_time)
            time.sleep(1)
        if self.remaining_time <= 0:
            self.is_running = False
            rumps.notification(
                "Pomodoro Timer", "Time's up!", "Take a break!" if self.is_working else "Back to work!"
            )
            self.is_working = not self.is_working
            self.remaining_time = self.rest_time if not self.is_working else self.work_time
            self.start_sound()

    def start_sound(self):
        if not self.is_playing_sound:
            self.is_playing_sound = True
            self.sound_thread = threading.Thread(target=self.play_sound)
            self.sound_thread.start()

    def play_sound(self):
        while self.is_playing_sound:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if not self.is_playing_sound:
                    pygame.mixer.music.stop()
                    break

    def stop_sound(self):
        self.is_playing_sound = False
        if self.sound_thread:
            self.sound_thread.join()

    @rumps.clicked("Start")
    def start(self, _):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.on_tick)
            self.timer_thread.start()
            self.menu["Start"].set_callback(None)
            self.menu["Pause"].set_callback(self.pause)

    @rumps.clicked("Pause")
    def pause(self, _):
        if self.is_running:
            self.is_running = False
            if self.timer_thread:
                self.timer_thread.join()
            self.menu["Start"].set_callback(self.start)
            self.menu["Pause"].set_callback(None)

    @rumps.clicked("Reset")
    def reset(self, _):
        self.stop_sound()
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join()
        self.remaining_time = self.work_time
        self.title = self.format_time(self.remaining_time)
        self.menu["Start"].set_callback(self.start)
        self.menu["Pause"].set_callback(None)

    @rumps.clicked("Rest")
    def rest(self, _):
        self.stop_sound()
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join()
        self.is_working = False
        self.remaining_time = self.rest_time
        self.title = self.format_time(self.remaining_time)
        self.menu["Start"].set_callback(self.start)
        self.menu["Pause"].set_callback(None)

    def save_settings(self):
        settings = {
            "work_time": self.work_time,
            "rest_time": self.rest_time,
            "sound_file": self.sound_file
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        default_settings = {
            "work_time": 1500,
            "rest_time": 300,
            "sound_file": "assets/alarm.mp3"
        }
        if not os.path.exists("settings.json"):
            with open("settings.json", "w") as f:
                json.dump(default_settings, f)
            self.work_time = default_settings["work_time"]
            self.rest_time = default_settings["rest_time"]
            self.sound_file = default_settings["sound_file"]
        else:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.work_time = settings.get("work_time", 1500)
                self.rest_time = settings.get("rest_time", 300)
                self.sound_file = settings.get("sound_file", "assets/alarm.mp3")

    def _handle_settings(self, _):
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        window = SettingsWindow()
        window.show()
        app.exec_()
        self.load_settings()
        self.remaining_time = self.work_time if self.is_working else self.rest_time
        self.title = self.format_time(self.remaining_time)

    def format_time(self, seconds):
        if seconds < 3600:
            minutes, seconds = divmod(seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"
        else:
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def parse_time(self, time_str):
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
        elif len(parts) == 2:
            hours = 0
            minutes, seconds = map(int, parts)
        elif len(parts) == 1:
            hours = 0
            minutes = 0
            seconds = int(parts[0])
        else:
            raise ValueError("Invalid time format")
        return hours * 3600 + minutes * 60 + seconds


if __name__ == "__main__":
    PomodoroTimerStatusBarApp().run()
