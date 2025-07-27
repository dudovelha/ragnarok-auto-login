from windowcapture import WindowCapture
from vision import Vision
from time import sleep
import interception
import pyotp
import json

import cv2 as cv

with open("conf.json", "r") as file:
    config = json.load(file)
totp = pyotp.TOTP(config.get('otp'))
wincap = WindowCapture('Ragnarok')

threshold = 0.8

disconnect_button_offset = [100, 40]
connect_button_offset = [70, 58]
otp_button_offset = [70, 40]
server_button_offset = [40, 90]
pin_button_offset = [190, 20]
terms_button_offset = [110, 140]
game_button_offset = [60, 85]
play_button_offset = [0, 0]
first_character_button_offset = [230, 155]

game_field_offset = [0, -70]
email_field_offset = [0, -15]
password_field_offset = [0, 20]
otp_field_offset = [0, 0]

pin_outside_offset = [-100, 0]

server_offset = ([0, -70], [0, -55], [0, -30])

class Bot:

    vision_action_tuple = ()
    pin_visions = []

    def __init__(self):
        self.vision_action_tuple = (
            (Vision('images/terms_window.jpg'), self.acceptTerms),
            (Vision('images/game_window.jpg'), self.selectGame),
            (Vision('images/login_window.jpg'), self.connect),
            (Vision('images/disconected_window.jpg'), self.disconnect),
            (Vision('images/last_login_window.jpg'), self.disconnect),
            (Vision('images/unable_window.jpg'), self.disconnect),
            (Vision('images/otp_window.jpg'), self.otp),
            (Vision('images/server_window.jpg'), self.selectServer),
            (Vision('images/pin_window.jpg'), self.pin),
            (Vision('images/play_button.jpg'), self.selectCharacter)
        )
        
        for number in config.get('pin'):
            self.pin_visions.append(Vision('images/pin_{}.jpg'.format(number)))

    def update(self):
        screenshot = wincap.get_screenshot()
        
        for vision_action in self.vision_action_tuple:
            vision = vision_action[0]
            action = vision_action[1]
            
            points = vision.find(screenshot, threshold)
            
            if len(points) > 0:
                wincap.focus()
                action(points[0])
                break
        

    def disconnect(self, window_position):
        print('disconected')
        self.click(window_position, disconnect_button_offset)
        
    def acceptTerms(self, window_position):
        print('accept terms and conditions')
        self.click(window_position, terms_button_offset)
    
    def selectGame(self, window_position):
        print('select game')
        self.click(window_position, game_field_offset)
        sleep(0.5)
        self.click(window_position, game_button_offset)
        
    def connect(self, window_position):
        print('loggin in')
        self.click(window_position, email_field_offset)
        interception.write(config.get('email'))
        self.click(window_position, password_field_offset)
        interception.write(config.get('password'))
        self.click(window_position, connect_button_offset)
        
    def otp(self, window_position):
        otp = totp.now()
        print('typing otp {}'.format(otp))
        self.click(window_position, otp_field_offset)
        interception.write(otp)
        self.click(window_position, otp_button_offset)
        
    def selectServer(self, window_position):
        server_position = config.get('server')
        print('select server at position {}'.format(server_position))
        self.click(window_position, server_offset[server_position])
        sleep(0.5)
        self.click(window_position, server_button_offset)
    
    def pin(self, window_position):
        print('typing pin {}'.format(config.get('pin')))
        self.click(window_position, pin_outside_offset)
        sleep(1)
        for pin_vision in self.pin_visions:
            screenshot = wincap.get_screenshot()
            pin_point = pin_vision.find(screenshot, 0.9)
            self.click(pin_point[0], [0, 0])
            sleep(0.5)
            self.click(window_position, pin_outside_offset)
            
        self.click(window_position, pin_button_offset)
    
    def selectCharacter(self, window_position):
        character_position = config.get('character')
        print('selecting character in position {}'.format(character_position))
        self.click([0, 0], first_character_button_offset)
        for i in range(character_position):
            interception.key_down('right')
            sleep(0.5)
        self.click(window_position, play_button_offset) 

    def click(self, win_position, offset):
        click_position = self.getPosition(win_position, offset)
        interception.click(x=click_position[0], y=click_position[1])

    def getPosition(self, position, offset):
        pos = [position[0] + offset[0], position[1] + offset[1]]
        return wincap.get_screen_position(pos)