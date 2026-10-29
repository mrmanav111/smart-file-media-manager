import sys
from PyQt6.QtWidgets import QApplication
from controller import AppController


def main():
    app = QApplication(sys.argv)
    window = AppController()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
