class PID():
    def __init__(self, timestamp, kp, ki, kd, name):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_err = 0
        self.err = 0
        self.I = 0 
        self.timestamp = timestamp # 100 mileseconds
        print("Create PID: " + name)
        self.printParameters()

    def printParameters(self):
        print('err: ' + str(self.err))
        print('Kp: ' + str(self.kp))
        print('Ki: ' + str(self.ki))
        print('Kd: ' + str(self.kd))
        print('ts: ' + str(self.timestamp))
        

    def get_vel(self):
        P = self.kp * self.err
        self.I += self.ki * self.err * self.timestamp
        D = (self.kd * (self.err - self.last_err))/self.timestamp
        return P + self.I + D
        