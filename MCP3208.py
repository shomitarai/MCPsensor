import spidev
import time
import math

class MCP3208:
        def __init__(self, spi_channel=0):
                self.spi_channel = spi_channel
                self.conn = spidev.SpiDev(0, spi_channel)
                self.conn.max_speed_hz = 1000000 # 1MHz

        def __del__( self ):
                self.close

        def close(self):
                if self.conn != None:
                        self.conn.close
                        self.conn = None

        def bitstring(self, n):
                s = bin(n)[2:]
                return '0'*(8-len(s)) + s

        def read(self, adc_channel=0):
                # build command
                cmd  = 128 # start bit
                cmd +=  64 # single end / diff
                if adc_channel % 2 == 1:
                        cmd += 8
                if (adc_channel/2) % 2 == 1:
                        cmd += 16
                if (adc_channel/4) % 2 == 1:
                        cmd += 32

                # send & receive data
                reply_bytes = self.conn.xfer2([cmd, 0, 0, 0])

                #
                reply_bitstring = ''.join(self.bitstring(n) for n in reply_bytes)
                # print reply_bitstring

                # see also... http://akizukidenshi.com/download/MCP3204.pdf (page.20)
                reply = reply_bitstring[5:19]
                return int(reply, 2)
        # specify reading frequency(Hz)
        def read_4ch(self, frequency=20):
            countSummationNumber =0
            startSummationTime = time.time()
            ch1=0
            ch2=0
            ch3=0
            ch4=0
            ch5=0
            while time.time()-startSummationTime <= 1.0/float(frequency):
                ch1 += self.read(0)
                ch2 += self.read(1)
                ch3 += self.read(2)
                ch4 += self.read(3)
                ch5 += self.read(4)
                countSummationNumber += 1
            return [ch1/countSummationNumber, ch2/countSummationNumber, ch3/countSummationNumber, ch4/countSummationNumber, ch5/countSummationNumber]

if __name__ == '__main__':
    spi = MCP3208(0)
    count = 0


    while count<100:
        print spi.read(0)
        count +=1
