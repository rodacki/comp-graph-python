import logging
import os
import sys

from PyQt5.QtWidgets import QApplication

from .mainwindow import MainWindow


def setup_logging() -> None:
    # Ex.: LOG_LEVEL=DEBUG poetry run ex07-pyqt-opengl
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
