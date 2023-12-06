def config():
    return {
        'default': 'sha256',

        'drivers': {
            'sha256': {
                'driver': 'sha256',
            },

            'sha1': {
                'driver': 'sha1',
            },

            'md5': {
                'driver': 'md5',
            },
        }
    }

