def config():
    return {
        'default': 'AES-CBC',
        
        'drivers': {
            'AES-ECB': {
                'driver': 'aesEcb',
                'size': 32,
            },

            'AES-CBC': {
                'driver': 'aesCbc',
                'size': 16,
            },
        }
    }

