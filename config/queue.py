from pythoniq.framework.illuminate.support.env import Env
from pythoniq.framework.illuminate.support.facades.app import App


def config():
    return {
        # --------------------------------------------------------------------------
        # Default Queue Connection Name
        # --------------------------------------------------------------------------
        #
        # Laravel's queue API supports an assortment of back-ends via a single
        # API, giving you convenient access to each back-end using the same
        # syntax for every one. Here you may define a default connection.
        #
        'default': Env().get('QUEUE_CONNECTION', 'null'),

        # --------------------------------------------------------------------------
        # Queue Connections
        # --------------------------------------------------------------------------
        #
        # Here you may configure the connection information for each server that
        # is used by your application. A default configuration has been added
        # for each back-end shipped with Laravel. You are free to add more.
        #
        # Drivers: "array", "null"
        #
        'connections': {
            'array': {
                'driver': 'array',
            },

            'null': {
                'driver': 'null',
            },
        },

        # --------------------------------------------------------------------------
        # Job Batching
        # --------------------------------------------------------------------------
        #
        # The following options configure the database and table that store job
        # batching information. These options can be updated to any database
        # connection and table which has been defined by your application.
        #
        'batching': {
            'database': Env().get('DB_CONNECTION', 'mysql'),
            'table': 'job_batches',
        },

        # --------------------------------------------------------------------------
        # Failed Queue Jobs
        # --------------------------------------------------------------------------
        #
        # These options configure the behavior of failed queue job logging so you
        # can control which database and table are used to store the jobs that
        # have failed. You may change them to any database / table you wish.
        #
        'failed': {
            'driver': Env().get('QUEUE_FAILED_DRIVER', 'database-uuids'),
            'database': Env().get('DB_CONNECTION', 'mysql'),
            'table': 'failed_jobs',
        },
    }

