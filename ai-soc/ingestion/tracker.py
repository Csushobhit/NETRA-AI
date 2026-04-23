class TimeTracker:
    def __init__(self):
        self.last_timestamp = "1970-01-01 00:00:00"

    def update(self, timestamp):
        self.last_timestamp = timestamp

    def get(self):
        return self.last_timestamp