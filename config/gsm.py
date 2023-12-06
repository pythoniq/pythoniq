from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'default': 'simcom',

        'drivers': {
            'simcom': {
                'driver': 'simcom',
                'regulator': Env().get('HARDWARE_GSM_REGULATOR'),
                'powerKey': Env().get('HARDWARE_GSM_POWER_KEY'),
                'simDetect': Env().get('HARDWARE_GSM_SIM_DETECT'),
                'status': Env().get('HARDWARE_GSM_STATUS'),
                'ringIndicator': Env().get('HARDWARE_GSM_RING_INDICATOR'),
                'uart': {
                    'id': Env().get('HARDWARE_GSM_UART_ID'),
                    'defaultBaudRate': Env().get('HARDWARE_GSM_UART_DEFAULT_BAUD_RATE', 115200),
                    'baudRate': Env().get('HARDWARE_GSM_UART_BAUD_RATE', 921600),
                    'rx': Env().get('HARDWARE_GSM_UART_RX'),
                    'tx': Env().get('HARDWARE_GSM_UART_TX'),
                },
            },
        }
    }
