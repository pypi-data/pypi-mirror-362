import logging
import datetime
import time
import threading

import suntimes


class SunshineTrigger(threading.Thread):

    def __init__(self, lattitude, longitude):
        
        super().__init__()

        self.logger = logging.getLogger("SunshineTrigger")
        self.calendar = suntimes.SunTimes(longitude, lattitude)

        self.do_run = True
        self.sunshine = True
        
        now = datetime.datetime.now(datetime.timezone.utc)
        self.logger.debug("Now : %s" % now)

        self.next_sunrise = self.calendar.riseutc(now.date()).replace(tzinfo=datetime.timezone.utc)
        self.logger.debug("Next self.next_sunrise : %s" % self.next_sunrise)
        
        self.next_sunset = self.calendar.setutc(now.date()).replace(tzinfo=datetime.timezone.utc)
        self.logger.debug("Next self.next_sunset : %s" % self.next_sunset)

        if now > self.next_sunrise and now < self.next_sunset:
            self.sunshine = True
            self.logger.debug("Day")
        else:
            self.sunshine = False
            self.logger.debug("Night")


    def run(self):

        self.logger.debug("run")
            
        while self.do_run:

            now = datetime.datetime.now(datetime.timezone.utc)

            if self.sunshine:

                if now > self.next_sunset:
                    self.logger.debug("Night has fallen")                    
                    self.sunshine = False
                    self.next_sunrise = self.calendar.riseutc(now.date() + datetime.timedelta(days=1)).replace(tzinfo=datetime.timezone.utc)
                    self.logger.debug("Next self.next_sunrise : %s" % self.next_sunrise)
                    self.on_self.next_sunset()

            else:

                if now > self.next_sunrise:
                    self.logger.debug("Day has raised")                    
                    self.sunshine = True
                    self.next_sunset = self.calendar.setutc(now.date()).replace(tzinfo=datetime.timezone.utc)
                    self.logger.debug("Next self.next_sunset : %s" % self.next_sunset)
                    self.on_self.next_sunrise()

            time.sleep(1)

    def on_sunrise(self):
        self.logger.debug("on_self.next_sunrise")

    def on_sunset(self):
        self.logger.debug("on_self.next_sunset")

    def join(self):
        self.do_run = False
        super().join()
