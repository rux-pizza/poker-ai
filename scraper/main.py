from screencap_quartz import ScreenCapture
from scraper import Scraper

if __name__ == '__main__':
    sp = Scraper()
    sc = ScreenCapture()

    print 'capturing...'
    sc.capture()
    print 'converting...'
    a = sc.tonumpy()
    print 'search card...'
    c = sp.findPlayerCards(a, 'm1lo0u')
    print c
    
