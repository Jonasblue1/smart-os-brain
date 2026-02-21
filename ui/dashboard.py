from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QTextEdit
)
from PySide6.QtCore import QTimer
import requests


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart OS Brain")
        self.resize(520, 600)

        layout = QVBoxLayout()

        self.stats = QLabel()
        layout.addWidget(self.stats)

        self.cmd = QLineEdit()
        self.cmd.setPlaceholderText("Run command")
        layout.addWidget(self.cmd)

        btn = QPushButton("Run")
        btn.clicked.connect(self.run_cmd)
        layout.addWidget(btn)

        row = QHBoxLayout()

        self.s_cmd = QLineEdit()
        self.s_cmd.setPlaceholderText("Schedule command")

        self.s_int = QLineEdit()
        self.s_int.setPlaceholderText("Minutes")

        row.addWidget(self.s_cmd)
        row.addWidget(self.s_int)

        layout.addLayout(row)

        s_btn = QPushButton("Add Schedule")
        s_btn.clicked.connect(self.schedule_cmd)
        layout.addWidget(s_btn)

        layout.addWidget(QLabel("Threats"))
        self.threat_box = QTextEdit()
        self.threat_box.setReadOnly(True)
        layout.addWidget(self.threat_box)

        layout.addWidget(QLabel("AI Anomalies"))
        self.anomaly_box = QTextEdit()
        self.anomaly_box.setReadOnly(True)
        layout.addWidget(self.anomaly_box)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(3000)

    def refresh(self):
        stats = requests.get("http://127.0.0.1:8010/stats").json()
        self.stats.setText(
            f"CPU {stats['cpu']}% | RAM {stats['ram']}% | Disk {stats['disk']}%"
        )

        threats = requests.get("http://127.0.0.1:8010/threats").json()
        self.threat_box.setText("\n".join([str(t) for t in threats]))

        anoms = requests.get("http://127.0.0.1:8010/anomalies").json()
        self.anomaly_box.setText("\n".join([str(a) for a in anoms]))

    def run_cmd(self):
        requests.post(f"http://127.0.0.1:8010/run?command={self.cmd.text()}")

    def schedule_cmd(self):
        requests.post(
            f"http://127.0.0.1:8010/schedule?command={self.s_cmd.text()}&interval={self.s_int.text()}"
        )
