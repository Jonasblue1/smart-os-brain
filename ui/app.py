import sys
from PySide6.QtWidgets import QApplication
from .dashboard import Dashboard   # <-- FIXED (notice the dot)

app = QApplication(sys.argv)
window = Dashboard()
window.show()
sys.exit(app.exec())
