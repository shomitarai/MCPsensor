import csv
import os

class FileSaveManager:

    def __init__(self, fileName='test'):
        self.saveCounter=0
        self.fileName = fileName
        self.savePath = './'+fileName+'/'
        if not os.path.exists(self.savePath):
            os.makedirs("./"+fileName)

    def loadCSV(self, filePath):
        dataSequence = []
        for itemList in open(filePath, 'r'):
            item = itemList.strip().split(',')
            dataSequence.append(item)
        return dataSequence

    def saveCSV(self, dataSequence):
        f = open(self.savePath+self.fileName+'_'+str(self.saveCounter)+'.csv', 'w')
        csv.writer(f).writerows(dataSequence)
        f.close()
        self.saveCounter += 1
        return self.saveCounter
    def save(self, name, dataSequence):
        f = open(name+'.csv', 'w')
        csv.writer(f).writerows(dataSequence)
        f.close()
        

# --------------Use for debug--------------
if __name__ == '__main__':
    fsm = FileSaveManager()

# test for saveCSV
    dataSeq = []
    for i in range(1,10):
        dataSeq.append([i, i])

    while True:
        if fsm.saveCSV(dataSeq) == 5:
            break

    # test for loadCSV
    print fsm.loadCSV("python_raspi/emg1-1.csv")
