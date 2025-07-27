from time import sleep
from bot import Bot


bot = Bot()
sleep(1)

while(True):
    bot.update()
    sleep(10)