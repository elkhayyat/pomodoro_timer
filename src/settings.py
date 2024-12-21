import json
import os

import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.settings_file = "settings.json"
        self.load_settings()
        pygame.mixer.init()
        self.is_playing = False

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout()

        self.work_time_label = QLabel("Work Time (hh:mm:ss):")
        self.work_time_input = QLineEdit()
        self.layout.addWidget(self.work_time_label)
        self.layout.addWidget(self.work_time_input)

        self.rest_time_label = QLabel("Rest Time (hh:mm:ss):")
        self.rest_time_input = QLineEdit()
        self.layout.addWidget(self.rest_time_label)
        self.layout.addWidget(self.rest_time_input)

        self.sound_file_label = QLabel("Sound File:")
        self.sound_file_input = QLineEdit()
        self.sound_file_button = QPushButton("Select Sound File")
        self.sound_file_button.clicked.connect(self.select_sound_file)
        self.layout.addWidget(self.sound_file_label)
        self.layout.addWidget(self.sound_file_input)
        self.layout.addWidget(self.sound_file_button)

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.clicked.connect(self.play_pause_sound)
        self.layout.addWidget(self.play_pause_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def select_sound_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sound File", "", "Audio Files (*.mp3 *.wav)",
                                                   options=options)
        if file_path:
            self.sound_file_input.setText(file_path)

    def play_pause_sound(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.play_pause_button.setText("Play")
        else:
            sound_file = self.sound_file_input.text()
            if os.path.exists(sound_file):
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                self.play_pause_button.setText("Pause")
        self.is_playing = not self.is_playing

    def save_settings(self):
        settings = {
            "work_time": self.time_to_seconds(self.work_time_input.text()),
            "rest_time": self.time_to_seconds(self.rest_time_input.text()),
            "sound_file": self.sound_file_input.text()
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)
        QMessageBox.information(self, "Settings", "Settings saved successfully!")
        self.close()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                self.work_time_input.setText(self.seconds_to_time(int(settings.get("work_time", 0))))
                self.rest_time_input.setText(self.seconds_to_time(int(settings.get("rest_time", 0))))
                self.sound_file_input.setText(settings.get("sound_file", ""))

    def time_to_seconds(self, time_str):
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

    def seconds_to_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    app = QApplication([])
    window = SettingsWindow()
    window.show()
    app.exec_()
