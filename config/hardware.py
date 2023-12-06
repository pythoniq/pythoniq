from pythoniq.framework.illuminate.support.env import Env


def config():
    return {
        'powerOutageWatcher': {
            'cycle': Env().get('HARDWARE_POWER_CONTROL_CYCLE', 10),
            'control': Env().get('HARDWARE_POWER_FAILURE_CONTROL'),
        },
        'protectionCover': {
            'dejectPin': Env().get('HARDWARE_PROTECTION_COVER_DEJECT_PIN'),
        },
        'i2c': {
            'clock': Env().get('HARDWARE_I2C_CLOCK'),
            'dataIo': Env().get('HARDWARE_I2C_DATA_IO'),
            'frequency': Env().get('HARDWARE_I2C_FREQUENCY', 100_000),
        },
        'ioExpander': {
            'led': {
                'deviceAddress': Env().get('HARDWARE_IO_EXPANDER_LED_DEVICE_ADDRESS', 32),
            }
        },
        'uart': {
            'meter': {
                'id': Env().get('HARDWARE_UART_METER_ID'),
                'baudRate': Env().get('HARDWARE_UART_METER_BAUD_RATE', 300),
                'rx': Env().get('HARDWARE_UART_METER_RX'),
                'tx': Env().get('HARDWARE_UART_METER_TX'),
                'rs485': {
                    'directionPin': Env().get('HARDWARE_UART_METER_RS485_DIRECTION_PIN'),
                }
            }
        }
    }
