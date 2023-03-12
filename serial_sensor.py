import serial

try:
    port = serial.Serial('COM3',57600)
    port_open = 1
except:
    #Serial port couldn't be opened / No arduino is connected
    port_open = 0

def get_measurement():
    if(port_open):
        port.reset_input_buffer()
        measurement = float(port.readline().decode().strip())
        #dealing with negative measurements
        if(measurement < 0):
            return 0
        else:
            return measurement
    else:
        #return sample measurement for demo purposes
        return 110

def tare():
    if(port_open):
        port.write(b't')
