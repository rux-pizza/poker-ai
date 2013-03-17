from screencap_quartz import ScreenCapture
from scraper import Scraper

if __name__ == '__main__':
    sp = Scraper()
    sc = ScreenCapture()

    while True:
        raw_input("press enter for screen cap ")
        sc.capture()
        a = sc.tonumpy()
        c = sp.findPlayerCards(a, 'm1lo0u')
        print c
    
