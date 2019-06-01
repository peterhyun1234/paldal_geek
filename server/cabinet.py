import datetime

class cabinet:
    def __init__(self, sid, pwd, num, isUse):
        self.id = sid
        self.pwd = pwd
        self.num = num
        self.isUse = isUse
        self.enrollt = datetime.datetime.now()

    def checkTimeout(self):
        now = datetime.datetime.now()
        # 3 miniutes
        if (now - self.enrollt).seconds >= 180:
            return true
        else:
            return false

