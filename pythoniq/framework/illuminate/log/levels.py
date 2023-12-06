class Levels:
    # The Log levels.
    _levels: dict = {
        # Detailed debug information
        'debug': 100,

        # Interesting events
        # Examples: User logs in, SQL logs.
        'info': 200,

        # Uncommon events
        'notice': 250,

        # Exceptional occurrences that are not errors
        # Examples: Use of deprecated APIs, poor use of an API, undesirable things that are not necessarily wrong.
        'warning': 400,

        # Runtime errors
        'error': 400,

        # Critical conditions
        # Example: Application component unavailable, unexpected exception.
        'critical': 500,

        # Action must be taken immediately
        # Example: Entire website down, database unavailable, etc.
        # This should trigger the SMS alerts and wake you up.
        'alert': 550,

        #  Urgent alert.
        'emergency': 600
    }
