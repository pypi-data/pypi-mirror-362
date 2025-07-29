from os import remove,sep
from secrets import choice,randbits
from gmpy2 import is_prime as isprime
import sys
import cv2
from time import sleep

def captureImage(path,total_images=1,camera=0):
    image_names = []
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        raise Exception("Cannot open camera")

    ret,frame = cap.read()
    sleep((1 + 1/(randbits(6)+0.000001))) #Waits for the cam to open.
    for i in range(total_images):
        if not ret:
            raise Exception("Can't receive frame (stream end?). Exiting ...")
        else:
            ret,frame = cap.read()
            # Save the captured image
            image_name = path + sep + str(i) + ".jpg"
            image_names.append(image_name)
            cv2.imwrite(image_name, frame)
    cap.release()
    cv2.destroyAllWindows()
    return image_names


class NoiseRandom():
    
    def __init__(self,path:str,strength=1,cameras=[0]):
        self.path = path
        self.images = []
        self.cameras = cameras
        self.strength = strength
        if(self.strength<1):
            self.strength = 1
        
    def randomInt(self,getBytes=False)->int|bytes:
        self.__captureImages()
        with open(choice(self.images), "rb") as f:
            data = f.read()
            f.close()
        self.__deleteImages()
        starting_image_index = data.find(b"\xFF\xDA")
        ending_image_index = data.find(b"\xFF\xD9")
        data = self.__scramble(data[starting_image_index+1:ending_image_index])
        if(getBytes):
            return data
        sys.set_int_max_str_digits(len(data) * 3)
        return  int.from_bytes(data,"big",signed=False)
    
    def randomBytes(self,total_bytes:int) -> int:
        if(total_bytes<=0):
            raise ValueError("The value of total_bytes can't be 0 or less.")
        random_pool = self.randomInt(True)
        selected_bytes = [choice(random_pool) & 0xFF for _ in range(total_bytes)]
        selected_bytes[0] |= (1<<7)
        return int.from_bytes(selected_bytes,"big",signed=False)
    
    def randomPrime(self,total_bytes:int) -> int:
        if(total_bytes<=0):
            raise ValueError("The value of total_bytes can't be 0 or less.")
        random_pool = self.randomInt(True)
        selected_bytes = [choice(random_pool) & 0xFF for _ in range(total_bytes)]
        selected_bytes[0] |= (1<<7)
        prime_number = int.from_bytes(selected_bytes,"big",signed=False)
        while(not isprime(prime_number)):
            selected_bytes = [choice(random_pool) & 0xFF for _ in range(total_bytes)]
            selected_bytes[0] |= (1<<7)
            prime_number = int.from_bytes(selected_bytes,"big",signed=False)
        return prime_number

    def random1024(self)->int:
        return self.randomBytes(1024//8)
    
    def random2048(self)->int:
        return self.randomBytes(2048//8)

    def random4096(self)->int:
        return self.randomBytes(4096//8)
    
    def randomPrime1024(self):
        return self.randomPrime(1024//8)

    def randomPrime2048(self):
        return self.randomPrime(2048//8)
    
    def randomPrime4096(self):
        return self.randomPrime(4096//8)
              
    def __deleteImages(self) -> None:
        for image_path in self.images:
            remove(image_path)
        self.images.clear()

    def __captureImages(self) -> None:
        for camera in self.cameras:
            self.images = self.images + captureImage(self.path,self.strength,camera=camera)
        
    def __scramble(self,data):
        byte_list = list(data)
        data_size = len(byte_list)
        scrambled_data = b""
        for i in range(data_size*3):
            p1 = randbits(4*8) % data_size
            p2 = randbits(4*8) % data_size

            byte_list[p1], byte_list[p2] = byte_list[p2], byte_list[p1]

        for byte in byte_list:
            scrambled_data += byte.to_bytes()
        
        return scrambled_data