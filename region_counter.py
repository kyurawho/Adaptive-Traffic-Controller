from enum import Enum
from config import (
    GREEN_PER_VEHICLE,
    MIN_GREEN,
    MAX_GREEN,
    YELLOW_TIME,
    ALL_RED_TIME,
    JML_KELUAR_PERMENIT,
)
from datetime import datetime
import math
import threading

class statusLampu(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class dataLampu:
    def __init__(self, name):
        self.status = statusLampu.RED
        self.jmlQueue = 0
        self.keluarBuffer = 0.0
        self.theId = []
        self.startRed = datetime.now()
        self.nama = name

class trafficController :
    def __init__(self):
        self.utara = dataLampu("Utara")
        self.timur = dataLampu("Timur")
        self.selatan = dataLampu("Selatan")
        self.barat = dataLampu("Barat")
        self.statLampu = [self.utara, self.timur, self.selatan, self.barat]
        self.LampTimer = 0

    def _setStatusLampu_(self, newstatus : statusLampu, camNumber):
        if (self.statLampu[camNumber].status != newstatus) :
            selArah : dataLampu = self.statLampu[camNumber]
            selArah.status = newstatus
            if newstatus == statusLampu.GREEN :
                self.LampTimer = MAX_GREEN
            elif newstatus == statusLampu.YELLOW :
                self.LampTimer = YELLOW_TIME
            else : #RED
                selArah.theId.clear()
                selArah.keluarBuffer = 0.0
                selArah.startRed = datetime.now()
                if camNumber == 3:
                    self._setStatusLampu_(statusLampu.GREEN, 0)
                else :
                    self._setStatusLampu_(statusLampu.GREEN, camNumber+1)

    def _timerEnd_(self):
        for index, lampu in self.statLampu :
            if lampu.status != statusLampu.RED :
                if lampu.status == statusLampu.GREEN:
                    self._setStatusLampu_(statusLampu.YELLOW, index)
                else :
                    self._setStatusLampu_(statusLampu.RED, index)

    def update(self, detections, camNumber):
        selArah : dataLampu = self.statLampu[camNumber]
        newId = [] 
        if selArah.status == statusLampu.RED :
            for detection in detections:
                inside_region = detection["inside_region"]
                if (inside_region) :
                    theid = detection["id"]
                    if theid not in selArah.theId:
                        selArah.theId.append(theid)
                        selArah.jmlQueue += 1
                        newId.append(theid)
        return newId
            
    def setStatus(self, status, camNumber):
        self.statLampu[camNumber].status = status

    def getJumlahQueue(self, camNumber):
        selArah : dataLampu = self.statLampu[camNumber]
        return selArah.jmlQueue
    
    def getLampu(self, camNumber):
        selArah : dataLampu = self.statLampu[camNumber]
        return selArah
    
    def startController(self):
        self._setStatusLampu_(statusLampu.GREEN, 2)
        print("controller starting")
    
    def timerClick(self):
        self.LampTimer -= 1
        #kurangi queue sesuai waktu
        for index in range(0, 4) :
            lampu = self.statLampu[index]
            if lampu.status == statusLampu.GREEN :
                lampu.keluarBuffer += JML_KELUAR_PERMENIT / 60
                jumlahKeluar = min(lampu.jmlQueue, int(lampu.keluarBuffer))
                if jumlahKeluar > 0:
                    lampu.jmlQueue -= jumlahKeluar
                    lampu.keluarBuffer -= jumlahKeluar
                if lampu.jmlQueue <= 0 :
                    lampu.jmlQueue = 0
                    if (MAX_GREEN - self.LampTimer) >= MIN_GREEN :
                        self._setStatusLampu_(statusLampu.YELLOW, index)

        #ganti staus lampu jk sdh sampai max time
        if self.LampTimer <= 0 :
            for index in range(0, 4) :
                lampu = self.statLampu[index]
                if lampu.status == statusLampu.GREEN :
                    self._setStatusLampu_(statusLampu.YELLOW, index)
                    break
                elif lampu.status == statusLampu.YELLOW :
                    self._setStatusLampu_(statusLampu.RED, index)
                    break

    def getAvgVehicleMenit(self, camNumber):
        selArah : dataLampu = self.statLampu[camNumber]
        currTime = datetime.now()
        deltaSeconds = (currTime - selArah.startRed).total_seconds()
        return math.ceil(60 * selArah.jmlQueue / deltaSeconds)
    
    def getProbabilitasGreenTime(self, camNumber):
        selArah : dataLampu = self.statLampu[camNumber]
        hasil = math.ceil(60 * selArah.jmlQueue / JML_KELUAR_PERMENIT)
        if hasil > MAX_GREEN :
            hasil = MAX_GREEN 
        elif hasil < MIN_GREEN :
            hasil = MIN_GREEN
        return hasil
                

class TrafficTimer:
    def __init__(self, tc : trafficController):
        self.trafficController = tc
        self.status = "running"

    def on_timer(self):
        self.trafficController.timerClick()
        if self.status == "running":
            timer = threading.Timer(1.0, self.on_timer)
            timer.start()

    def Start(self) :
        timer = threading.Timer(1.0, self.on_timer)
        timer.start()

    def Stop(self):
        self.status = "stop"
