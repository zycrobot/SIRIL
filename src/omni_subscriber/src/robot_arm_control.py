#!/usr/bin/env python
# Python 3.9.12 (main, Apr  5 2022, 06:56:58)
import time
import serial
import sys

class RobotSDK:
    def __init__(self,port):
        self.port=port
        self.serial_port = serial.Serial(
            port=port,
            baudrate=57600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        time.sleep(1)
        print("serial connect!")

    def swichToRemoteControl(self):
        try:
            print("command = C004")
            self.serial_port.write("C004\r\n".encode('ASCII'))
            response = self.serial_port.readline().decode().strip()
            print("answer  = ",response)
            print('swich To Remote Control!')

        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
        finally:
            pass
        

    def switchToMannualControl(self):
        try:
            print("command = C005")

            self.serial_port.write("C005\r\n".encode('ASCII'))
            response = self.serial_port.readline().decode().strip()
            print("answer  = ",response)
            print('switch To Mannual Control!')

        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
        finally:
            print()


    def positionQueryInMicrometers(self):
        try:
            print("command = C010")
            self.serial_port.write("C010\r\n".encode('ASCII'))
            ans = self.serial_port.readline().decode().strip()
            # print(ans)
            rxyc0=ans.split(' ')
            res=[int(rxyc0[1]),int(rxyc0[2]),int(rxyc0[3])]
            return res

        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
        finally:
            pass

    def gotoPositionInmicrometers_(self,px,py,pz,vx=1000,vy=1000,vz=1000):
        command="C007"+" "+str(px)+" "+str(py)+" "+str(pz)+" "+str(vx)+" "+str(vy)+" "+str(vz)+"\r\n"
        try:
            self.serial_port.write(command.encode('ASCII'))
            response = self.serial_port.readline().decode().strip()
            print("answer  = ",response)

        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
            
        finally:
            pass


    
    def gotoPositionInmicrometers(self,px,py,pz,vx=5000,vy=5000,vz=3000):
        '''
        To fast track trajectory
        TODO fix robot arm jerks
        '''
        command=f"C012 {px} {py} {pz} {vx} {vy} {vz}\r\n"
        self.serial_port.write(command.encode('ASCII'))
        self.serial_port.readline()


    def gotoPositionInmicrometers_V(self,px,py,pz,vx=3000,vy=3000,vz=2000):
        '''
        To fast track trajectory
        TODO fix robot arm jerks
        '''
        command=f"C012 {px} {py} {pz} {vx} {vy} {vz}\r\n"
        self.serial_port.write(command.encode('ASCII'))
        self.serial_port.readline()


    def gotoPositionInmicrometers_C011(self,px,py,pz,vx=5000,vy=5000,vz=3000):
        
        command="C011"+" "+str(px)+" "+str(py)+" "+str(pz)+" "+str(vx)+" "+str(vy)+" "+str(vz)+"\r\n"
        try:
            self.serial_port.write(command.encode('ASCII'))
            self.serial_port.readline()
        except Exception as exception_error:
            print("Error occurred. Exiting Program")
            print("Error: " + str(exception_error))
        finally:
            pass

    def __del__(self):
        self.switchToMannualControl()
        print('Close '+self.port)
        self.serial_port.close()
        time.sleep(0.1)


def main():

    # assert len(sys.argv)==3
    sdk=RobotSDK('/dev/ttyUSB0') #leftarm
    # sdk=RobotSDK('/dev/ttyUSB0') #rightarm
    sdk.swichToRemoteControl()
    
    x,y,z=sdk.positionQueryInMicrometers()
    sdk.gotoPositionInmicrometers_(x+int(sys.argv[1]),y+int(sys.argv[2]),z+int(sys.argv[3]))


if __name__ == '__main__':
    main()
    pass

