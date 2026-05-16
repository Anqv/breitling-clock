import sys
import platform


def main():
    print(f"Breitling AeroSpace Evo Desktop Watch")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print()

    from PyQt5.QtWidgets import QApplication
    from watch.main_window import WatchWindow

    app = QApplication(sys.argv)
    app.setApplicationName("Breitling Clock")
    app.setApplicationVersion("1.0.0")

    if platform.system() == "Linux":
        app.setDesktopFileName("breitling-clock")

    window = WatchWindow()
    window.show()

    print("Watch is running. Right-click for settings.")
    print("Press Ctrl+C to exit in terminal mode.")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()