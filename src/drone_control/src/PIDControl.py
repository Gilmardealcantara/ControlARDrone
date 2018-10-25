class PIDControl():
    def __init__(self, timestamp, kp, ki, kd, name):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_err = 0
        self.err = 0
        self.I = 0 
        self.timestamp = timestamp # 100 mileseconds
        self.point = 1.0
        print("Create PID: " + name)
        # self.printParameters(0,0,0)

    def printParameters(self, P, I, D, val):
        print('Kp : ' + str(self.kp))
        print('Ki : ' + str(self.ki))
        print('Kd : ' + str(self.kd))
        print('ts : ' + str(self.timestamp))
        print('ref: ' + str(self.point))
        print('val: ' + str(val))
        print('err: ' + str(self.err))
        print('P  : ' + str(P))
        print('I  : ' + str(I))
        print('D  : ' + str(D))
        print('vel: ' + str(P + I + D))
        
    def update_params(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_point(self, p):
        self.point = p
    
    def get_vel(self, current_p):
        self.err = self.point - current_p
        
        P = self.kp * self.err
        self.I += self.ki * self.err * self.timestamp
        D = (self.kd * (self.err - self.last_err))/self.timestamp
        # self.printParameters(P, self.I, D, current_p)
        self.last_err = self.err
        return P + self.I + D
        