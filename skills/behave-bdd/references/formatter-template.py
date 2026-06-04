"""
Custom Formatter Template for Behave

Usage:
    behave --format=features.formatters.custom_formatter:MyFormatter

Or register in behave.ini:
    [behave]
    format = features.formatters.custom_formatter:MyFormatter
"""

from behave.formatter.base import Formatter


class MyFormatter(Formatter):
    name = 'myformatter'
    description = 'Template custom formatter. Replace with your implementation.'

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)
        self.results = []

    def feature(self, feature):
        """Called when a feature starts."""
        pass

    def scenario(self, scenario):
        """Called when a scenario starts."""
        pass

    def step(self, step):
        """Called when a step starts."""
        pass

    def result(self, step):
        """Called when a step finishes."""
        self.results.append({
            'name': step.name,
            'status': step.status,
            'duration': step.duration,
            'error_message': step.error_message,
        })

    def eof(self):
        """Called at end of feature file. Post results here."""
        # Example: send to Slack, write to DB, generate custom report
        pass

    def close(self):
        """Called when formatter is closed."""
        pass
