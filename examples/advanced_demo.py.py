"""
Advanced demo with real-time data and dashboard
"""

from layered_earth import quick_start
import time
import threading

def delayed_data_add(app):
    time.sleep(3)
    app.add_earthquake_data(None)
    time.sleep(2)
    app.add_weather_data(None)
    time.sleep(2)
    app.toggle_dashboard(None)

if __name__ == "__main__":
    print("🚀 Launching Layered-Earth Advanced Demo")
    app = quick_start()

    thread = threading.Thread(target=delayed_data_add, args=(app,), daemon=True)
    thread.start()

    app.show()