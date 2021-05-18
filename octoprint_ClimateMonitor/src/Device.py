import adafruit_dht
import board

import logging

logging.basicConfig("./logs/device_loging.log")

class Device:

    def __init__(self, data_pin:int, type:str, use_celsius:bool=False, *args, **kwargs) :
        self.data_pin = data_pin
        assert type in ['ambient', 'enclosure'] , f"type must be either 'enclosure' or 'ambient', {type} provided."
        self.type = type
        self.use_celsius = use_celsius
        


    def _init_device(self): 
        ''' Sets up the device with pin values, returns true if successful '''
        # TODO: Do not know the board module well enough. Can look into more effective means for this later
        pin_num_convert = {
            "1": board.D1, 
            "2": board.D2, 
            "3": board.D3, 
            "4": board.D4, 
            "5": board.D5, 
            "6": board.D6, 
            "7": board.D7, 
            "8": board.D8, 
            "9": board.D9, 
            "10": board.D10, 
            "11": board.D11, 
            "12": board.D12, 
            "13": board.D13, 
            "14": board.D14, 
            "15": board.D15, 
            "16": board.D16, 
            "17": board.D17, 
            "18": board.D18, 
            "19": board.D19, 
            "20": board.D20, 
            "21": board.D21, 
            "22": board.D22, 
            "23": board.D23, 
            "24": board.D24, 
            "25": board.D25, 
            "26": board.D26, 
            "27": board.D27, 
        }
        try:
            self.device = adafruit_dht.DHT22(pin_num_convert.get(str(self.data_pin), None))
            return True
        except Exception as e:
            raise Exception("Error initializing the device. ")

    def get_temperature(self) -> float:
        try:
            t = float(self.device.temperature)
            t = t if self.use_celsius else t * (9/5) + 32
            return 
        
        except Exception as e:
            logging.error(f"Read error on device {self.type} for temperature.")
            return None

    def get_humidity(self) -> float:
        tryL
        return float(self.device.humidity)
