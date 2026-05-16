class WeatherDisplay:
    def __init__(self):
        self.enabled = False
        self.api_key = None
        self.location = None
        self.refresh_interval = 300

    def enable(self, api_key, location, refresh_interval=300):
        self.api_key = api_key
        self.location = location
        self.refresh_interval = refresh_interval
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_current(self):
        if not self.enabled:
            return {
                "temperature": "--",
                "condition": "Not configured",
                "icon": None,
                "location": None
            }

        return {
            "temperature": "--",
            "condition": "Coming soon",
            "icon": None,
            "location": self.location
        }

    def update(self):
        pass

    def is_enabled(self):
        return self.enabled