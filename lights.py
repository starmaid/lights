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
        data = list(sum(light_arr,()))
        print(data,end='\r')
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
    



if __name__ == "__main__":
    import random
    length = 100
    a = WledLightStrip(length)
    #print(a.getLightState())
    while True:
        a.setLights([(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for a in range(length)])
        time.sleep(0.01)