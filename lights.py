import socket
import requests
import time

class LightStrip():
    def __init__(self,num_leds):
        self.num_leds = num_leds
        pass

    def powerOn(self):
        pass

    def powerOff(self):
        pass

    def setLights(self,light_arr):
        """
        Light array is a list of 3-tuples, RGB order
        """
        if len(light_arr) > self.num_leds:
            print(f'length of array {len(light_arr)} > length of current strip = {self.num_leds}')
            raise ValueError()
        if not isinstance(light_arr[0],tuple):
            print(f'you didnt pass tuples to the setLights')
            raise TypeError()
        if max(max(light_arr)) > 255:
            print(f'max value higher than 255')
            raise ValueError()
        if min(min(light_arr)) < 0:
            print(f'min value below 0')
            raise ValueError()
        pass


class PrintTestLightStrip(LightStrip):
    def setLights(self, light_arr):
        super().setLights(light_arr)
        # This is apparently the magic to flatten tuples
        #data = list(sum(light_arr,()))

        # this is the method from DSN
        allL = [int(sum(a)/3/25.6) for a in light_arr]
        allLString = ''
        for l in allL:
            allLString += str(l)
        print(allLString + '\r',end='')
        return  

class WledLightStrip(LightStrip):
    def __init__(self, num_leds, ip_addr="192.168.0.20"):
        super().__init__(num_leds)
        self.light_address = ip_addr
        self.light_baseurl = f"http://{self.light_address}"
        self.light_udp_port = 21324
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def powerOn(self):
        super().powerOn()
    
    def setLights(self, light_arr):
        super().setLights(light_arr)
        
        # This is apparently the magic to flatten tuples
        data = [2,5] + list(sum(light_arr,()))
        self.s.sendto(bytes(data), (self.light_address, self.light_udp_port))
        return  
    
    def getLightState(self):
        r = requests.get(self.light_address + "/json")
        return(r.content)



class NeopixelRPILightStrip(LightStrip):
    def __init__(self, num_leds, gpio_pin=18,pixel_order="GRB", brightness=50):
        super().__init__(num_leds)
        if gpio_pin not in [18,19,20,21]:
            raise Exception('Selected pin does not support PCM. See pinout and modify config.')

        import board
        import neopixel

        if pixel_order == "GRB":
            order = neopixel.GRB
        elif pixel_order == "GRBW":
            order = neopixel.GRBW
        else:
            order = neopixel.GRB
        
        pinname = getattr(board,'D'+str(gpio_pin))

        self.lights_strip = neopixel.NeoPixel(pinname, num_leds, 
                brightness=brightness, auto_write=False, 
                pixel_order=order)

    def setLights(self, light_arr):
        super().setLights(light_arr)

        for i,t in enumerate(light_arr):
            self.lights_strip[i] = t
            
        self.lights_strip.show()
        return 



if __name__ == "__main__":
    import random
    length = 100
    a = WledLightStrip(length)
    #print(a.getLightState())
    while True:
        a.setLights([(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for a in range(length)])
        time.sleep(0.01)