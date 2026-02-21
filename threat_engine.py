class ThreatEngine:
    def __init__(self):
        self.score = 0
        self.events = []

    def add_event(self, source, severity, description):
        self.score += severity
        event = {
            "source": source,
            "severity": severity,
            "description": description
        }
        self.events.append(event)

    def get_score(self):
        return self.score

    def get_events(self):
        return self.events[-20:]


threat_engine = ThreatEngine()
