from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Max2828_Window as myWindow
##import Max2828_Communication as myCommunication
import serial
from time import sleep
import struct
import sqlite3
starter_byte      = 0XAA 
Max2828_command   = 0X02 
Max5866_command   = 0X03 
command_byte      = 0XBB 
RF_command        = 0x01 
PADAC_command     = 0X02 
RX_command        = 0X03 
TX_command        = 0X04 
LNA_command       = 0X05 
GAIN_command      = 0X06
MAX_command       = 0X07
Zero_Byte         = 0X00

class WindowEdit(object):
    source_byte       = 0X01 
    destination_byte  = 0X02
    ValueofChangeMax  = 2
    counter_of_SaveDB = 1
    ComPort           = 'COM3'
    globalnameDB      = 'LastPowerDown.db'
    checkPackageList     = True
    ctr=0
    print("RF     PADAC    RX     TX    LNA   GAIN    M2828    M5866")
    def checkDevice(self,ui):
        if self.con.is_open:
            ui.ConnectionGraphic.setText(self.con.name +" Connected")
        else:
            ui.ConnectionGraphic.setText("Disconnected")
    def SerialConnection(self,ui):
        try:
            self.ComPort = ui.ComPort_Line.text()
            self.con = serial.Serial(self.ComPort, 9600 , timeout = 1)
        except serial.SerialException:
            print("No Port Found")
            ui.ConnectionGraphic.setText("Disonnected")
            ui.close_application()
            raise
        except:
            print("Communication Port Error")
            ui.ConnectionGraphic.setText("Disconnected")
            ui.close_application()
    def PrintDB(self):
        try:
            result = self.theCursor.execute("SELECT ID,RF, PADAC, RXVGA, TXVGA, TXLNA, RXGAIN, MAX, PORT FROM DB")
            for row in result:
                print("ID     :", row[0])
                print("RF     :", row[1])
                print("PADAC  :", row[2])
                print("RXVGA  :", row[3])
                print("TXVGA  :", row[4])
                print("TXLNA  :", row[5])
                print("RXGAIN :", row[6])
                print("MAX    :", row[7])
                print("PORT   :", row[8])
                print("        ")
        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")
        except:
            print("Couldn't Retrieve Data From Database")
            
    def SaveDB(self, ui, nameofDB):
        db_conn = sqlite3.connect(nameofDB)
        self.theCursor = db_conn.cursor()
        try:
            RF_value    = int(ui.RFFrequency_Line.text())
            PADAC_value = int(ui.PADACOutputBias_Line.text()) 
            RXVGA_value = int(ui.RXVGAGain_Line.text())      
            TXVGA_value = int(ui.TXVGAGain_Line.text())            
            LNA_value   = ui.RXLNAGain_ComboBox.currentIndex()
            GAIN_value  = ui.TXBasebandGain_ComboBox.currentIndex()
            MAX_value   = self.ValueofChangeMax
            Port_value  = ui.ComPort_Line.text()
            params = ( RF_value, PADAC_value, RXVGA_value, TXVGA_value, LNA_value, GAIN_value, MAX_value, Port_value)
            db_conn.execute("DROP TABLE IF EXISTS DB")
            db_conn.commit()
            db_conn.execute("CREATE TABLE DB(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,RF INT,PADAC INT,RXVGA INT,TXVGA INT,TXLNA INT,RXGAIN INT,MAX INT,PORT TEXT);")
            db_conn.commit()            
            db_conn.execute("INSERT INTO DB VALUES (NULL,?,?,?,?,?,?,?,?)",params)
            db_conn.commit()
            print("Table Created")
        except sqlite3.OperationalError:
            print("Table couldn't be Created")
        print(params)
        self.PrintDB()
    def SaveComboboxDB(self, ui):
        CB1_value   = ui.Setups_ComboBox.itemText(2)
        CB2_value   = ui.Setups_ComboBox.itemText(3)
        CB3_value   = ui.Setups_ComboBox.itemText(4)
        rcvDB = sqlite3.connect('CDBase.db')
        cur = rcvDB.cursor()    
              
        param       = (CB1_value,CB2_value,CB3_value)
        rcvDB.execute("DROP TABLE IF EXISTS CDB")
        rcvDB.commit()
        rcvDB.execute("CREATE TABLE CDB(CB1 INT, CB2 INT, CB3 INT );")
        rcvDB.commit()            
        rcvDB.execute("INSERT INTO CDB VALUES (?,?,?)",param)
        rcvDB.commit()
        print("Table Created")
        try:
            result = cur.execute("SELECT CB1, CB2, CB3 FROM CDB")
            for row in result:                
                print("1   :", row[0])
                print("2   :", row[1])
                print("3   :", row[2])
        except sqlite3.OperationalError:
            print("Operational Error")
        except:
            print("Couldn't Retrieve Data From Database")
        
    def ReceiveDB(self,ui, nameofDB):
        rcvDB = sqlite3.connect(nameofDB)
        cur = rcvDB.cursor()
        result = cur.execute("SELECT ID,RF, PADAC, RXVGA, TXVGA, TXLNA, RXGAIN, MAX,PORT FROM DB")
        try:
            for row in result:
                ui.RFFrequency_Line.setText(str(row[1]))
                ui.PADACOutputBias_Line.setText(str(row[2]))
                ui.RXVGAGain_Line.setText(str(row[3]))
                ui.TXVGAGain_Line.setText(str(row[4]))
                ui.RXLNAGain_ComboBox.setCurrentIndex(int(row[5]))
                ui.TXBasebandGain_ComboBox.setCurrentIndex(int(row[6]))
                self.ValueofChangeMax = int(row[7])
                ui.ComPort_Line.setText(str(row[8]))
        except sqlite3.OperationalError:
            print("Operational Error")
        except:
            print("Couldn't Retrieve Data From Database")
    
    def ReceiveComboboxDB(self,ui):
        rcvDB = sqlite3.connect('CDBase.db')
        cur = rcvDB.cursor()
        result = cur.execute("SELECT CB1,CB2,CB3 FROM CDB")
        try:
            for row in result:
                ui.Setups_ComboBox.insertItem(2,str(row[0]))
                ui.Setups_ComboBox.insertItem(3,str(row[1]))
                ui.Setups_ComboBox.insertItem(4,str(row[2]))
                ui.Setups_ComboBox.setItemText(2,str(row[0]))
                ui.Setups_ComboBox.setItemText(3,str(row[1]))
                ui.Setups_ComboBox.setItemText(4,str(row[2]))
        except sqlite3.OperationalError:
            print("Operational Error")
        except:
            print("Couldn't Retrieve Data From Database")
        
    def send(self,PackageList):
        try:
            self.con.write(PackageList)
        except serial.SerialException:
            print("No connection found")
            self.try3Times(PackageList)
            raise
        except:
            print("Error occured")
            
    def try3Times(self,PackageList):
        try:
            for i in range(3):
                ctr = ctr+1
                print("Trying again... "+ str(i+1) + ". time ")
                if ctr >= 3:
                    print("Couldn't success");
                    break;
                self.mainFunction(PackageList)
                if self.checkPackageList == True:
                    print("Succeed in " + str(i+1) + ". time")
                    break;
            print("========================================================")
        except:
            print("Communication Error")
    def receive(self,PackageList):
        try:
            our_buffer = []
            counter = 0
            while counter < len(PackageList):
                msg = self.con.read()
                msg = msg.hex()
                msg = int(msg,16)
                our_buffer.append(msg)            
                print(msg)
                counter = counter + 1
            print(PackageList)
            print(our_buffer)
            if our_buffer == PackageList:
                print("Package received successfully")
            else:
                for i in range(3):
                    print("Trying again... "+ str(i+1) + ". time ")
                    self.mainFunction(PackageList)                    
                print("Package could not be transfered")
            print("========================================================")
        except serial.SerialException:
            print("No connection found")
            raise
        except:
            print("Error occured")
    def receiveAck(self,PackageList):
        try:
            our_buffer = []
            counter = 0
            while counter < 5:
                msg = self.con.read()
                msg = msg.hex()
                msg = int(msg,16)
                our_buffer.append(msg)            
                print(msg)
                counter = counter + 1                
            print(our_buffer)
            if (PackageList[0] == our_buffer[0] and PackageList[1] == our_buffer[2] and PackageList[2] == our_buffer[1] ):
                if (our_buffer[4] == 1):
                    print("Acknowledgement received successfully")
                    print("Package is correct!")                    
                elif(our_buffer[4] == 0):
                    print("Acknowledgement received successfully")
                    print("Package is not correct:(")
                self.checkPackageList = True   
            else:
                self.checkPackageList = False
                self.try3Times(PackageList)
        except serial.SerialException:
            print("Serial Error for Ack")
            self.try3Times(PackageList)
        except:
            print("Error occured for Ack")
            self.try3Times(PackageList)
    def mainFunction(self, PackageList):
        try:
            self.send(PackageList)
##            self.receive(PackageList)
            self.receiveAck(PackageList)
        except serial.SerialException:
            print("No connection found")
            raise
        except:
            print("Error occured")
    def des2828(self):
        self.destination_byte = 0X02
        self.ValueofChangeMax  = 2
    def des5866(self):
        self.destination_byte = 0X03
        self.ValueofChangeMax  = 3
    def checktoDestination(self):
        if   self.ValueofChangeMax == 2:
            self.mainFunction(self.Max2828_Package)
        elif self.ValueofChangeMax == 3:
            self.mainFunction(self.Max5866_Package)
        else:
            pass
    def ValuetoHex(self,ui):
        ValueofRFFrequency      = ui.RFFrequency_ScrollBar.value()
        ValueofPADACOutputBias  = ui.PADACOutputBias_ScrollBar.value()
        ValueofRXVGAGain        = ui.RXVGAGain_ScrollBar.value()
        ValueofTXVGAGain        = ui.TXVGAGain_ScrollBar.value()
        ValueofLNA  = ui.RXLNAGain_ComboBox.currentIndex()
        ValueofGAIN = ui.TXBasebandGain_ComboBox.currentIndex()
        ValueofMax2828 = ui.Max2828_ComboBox.currentIndex()
        ValueofMax5866 = ui.Max5866_ComboBox.currentIndex()
        RF   = struct.pack('>h', ValueofRFFrequency)
        RF   = RF.hex()
        RF1 = int(RF[:2], 16)
        RF2 = int(RF[-2:], 16)
        PADAC = struct.pack('>h', ValueofPADACOutputBias)
        PADAC = PADAC.hex().zfill(4)
        PADAC1 = int(PADAC[:2], 16)
        PADAC2 = int(PADAC[-2:], 16)
        RX   = struct.pack('>h', ValueofRXVGAGain)
        RX   = RX.hex().zfill(4)
        RX1 = int(RX[:2], 16)
        RX2 = int(RX[-2:], 16)
        TX   = struct.pack('>h', ValueofTXVGAGain)
        TX   = TX.hex().zfill(4)
        TX1 = int(TX[:2], 16)
        TX2 = int(TX[-2:], 16)
        LNA   = struct.pack('>h', ValueofLNA)
        LNA   = LNA.hex().zfill(4)
        LNA1 = int(LNA[:2], 16)
        LNA2 = int(LNA[-2:], 16)
        GAIN   = struct.pack('>h', ValueofGAIN)
        GAIN   = GAIN.hex().zfill(4)
        GAIN1 = int(GAIN[:2], 16)
        GAIN2 = int(GAIN[-2:], 16)
        Max2828   = struct.pack('>h', ValueofMax2828)
        Max2828   = Max2828.hex()
        Max28281 = int(Max2828[:2], 16)
        Max28282 = int(Max2828[-2:], 16)
        Max5866   = struct.pack('>h', ValueofMax5866)
        Max5866   = Max5866.hex()
        Max58661 = int(Max5866[:2], 16)
        Max58662 = int(Max5866[-2:], 16)
        print(RF + "    " + PADAC + "   " + RX + "   " + TX + "   " + LNA + "  " + GAIN + "    " + Max2828 + "    " + Max5866 )

        self.RF_Package    = [starter_byte, self.source_byte, self.destination_byte, RF_command,
                           RF1, RF2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.PADAC_Package = [starter_byte, self.source_byte, self.destination_byte, PADAC_command,
                           PADAC1, PADAC2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.RX_Package    = [starter_byte, self.source_byte, self.destination_byte, RX_command,
                           RX1, RX2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.TX_Package    = [starter_byte, self.source_byte, self.destination_byte, TX_command,
                           TX1, TX2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.LNA_Package   = [starter_byte, self.source_byte, self.destination_byte, LNA_command,
                           LNA1, LNA2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.GAIN_Package  = [starter_byte, self.source_byte, self.destination_byte, GAIN_command,
                           GAIN1, GAIN2, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.Max2828_Package    = [starter_byte, self.source_byte, self.destination_byte, MAX_command,
                           Max28281, Max28282, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        self.Max5866_Package    = [starter_byte, self.source_byte, self.destination_byte, MAX_command,
                           Max58661, Max58662, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte, Zero_Byte ]
        

            
    def mainLoop(self):
        app = QtWidgets.QApplication(sys.argv)
        ui = myWindow.Ui_MainWindow()        
        MainWindow = ui.callMain()    
        ui.setupUi(MainWindow)
        MainWindow.show()
        self.SerialConnection(ui)
        self.ValuetoHex(ui)
        self.checkDevice(ui)
##########
        ui.ComPort_Line.editingFinished.connect(lambda: self.SerialConnection(ui))
##########    Menu Side
        ui.actionExit.triggered.connect(ui.close_application)
##########    ScrollBar Side
        ui.RFFrequency_ScrollBar.valueChanged.connect(lambda: ui.ScrollBarValue(ui.RFFrequency_ScrollBar, ui.RFFrequency_Line))
        ui.PADACOutputBias_ScrollBar.valueChanged.connect(lambda: ui.ScrollBarValue(ui.PADACOutputBias_ScrollBar, ui.PADACOutputBias_Line))
        ui.RXVGAGain_ScrollBar.valueChanged.connect(lambda: ui.ScrollBarValue(ui.RXVGAGain_ScrollBar, ui.RXVGAGain_Line))
        ui.TXVGAGain_ScrollBar.valueChanged.connect(lambda: ui.ScrollBarValue(ui.TXVGAGain_ScrollBar, ui.TXVGAGain_Line))

        ui.RFFrequency_Line.editingFinished.connect(lambda: ui.RFFrequency_ScrollBar.setSliderPosition(int(ui.RFFrequency_Line.text())))
        ui.PADACOutputBias_Line.editingFinished.connect(lambda: ui.PADACOutputBias_ScrollBar.setSliderPosition(int(ui.PADACOutputBias_Line.text())))
        ui.RXVGAGain_Line.editingFinished.connect(lambda: ui.RXVGAGain_ScrollBar.setSliderPosition(int(ui.RXVGAGain_Line.text())))
        ui.TXVGAGain_Line.editingFinished.connect(lambda: ui.TXVGAGain_ScrollBar.setSliderPosition(int(ui.TXVGAGain_Line.text())))
##########  Button Side
        def removeCombobox():
            if (  ui.Setups_ComboBox.currentText() == "LastPowerDown" or ui.Setups_ComboBox.currentText() == "" ):
                pass
            else:
                ui.Setups_ComboBox.removeItem(ui.Setups_ComboBox.currentIndex())  
        ui.Del_Button.clicked.connect(lambda: removeCombobox())
##########  Combobox Side
        
            
########## Line Edit Side
        ui.RFFrequency_Line.setText(str( ui.RFFrequency_ScrollBar.value()))
        ui.PADACOutputBias_Line.setText(str( ui.PADACOutputBias_ScrollBar.value()))
        ui.RXVGAGain_Line.setText(str( ui.RXVGAGain_ScrollBar.value()))
        ui.TXVGAGain_Line.setText(str( ui.TXVGAGain_ScrollBar.value()))

        ui.RFFrequency_Line.editingFinished.connect(lambda: ui.CheckingLines(ui.RFFrequency_ScrollBar, ui.RFFrequency_Line))
        ui.PADACOutputBias_Line.editingFinished.connect(lambda: ui.CheckingLines(ui.PADACOutputBias_ScrollBar, ui.PADACOutputBias_Line))
        ui.RXVGAGain_Line.editingFinished.connect(lambda: ui.CheckingLines(ui.RXVGAGain_ScrollBar, ui.RXVGAGain_Line))
        ui.TXVGAGain_Line.editingFinished.connect(lambda: ui.CheckingLines(ui.TXVGAGain_ScrollBar, ui.TXVGAGain_Line))
########## Communication Side
        
        
        ui.RFFrequency_ScrollBar.valueChanged.connect(lambda: self.ValuetoHex(ui))        
        ui.PADACOutputBias_ScrollBar.valueChanged.connect(lambda: self.ValuetoHex(ui))
        ui.RXVGAGain_ScrollBar.valueChanged.connect(lambda: self.ValuetoHex(ui))
        ui.TXVGAGain_ScrollBar.valueChanged.connect(lambda: self.ValuetoHex(ui))
        ui.RXLNAGain_ComboBox.currentIndexChanged.connect(lambda: self.ValuetoHex(ui))
        ui.TXBasebandGain_ComboBox.currentIndexChanged.connect(lambda: self.ValuetoHex(ui))
        ui.Max2828_ComboBox.currentIndexChanged.connect(lambda: self.des2828())
        ui.Max2828_ComboBox.currentIndexChanged.connect(lambda: self.ValuetoHex(ui))
        ui.Max5866_ComboBox.currentIndexChanged.connect(lambda: self.des5866())
        ui.Max5866_ComboBox.currentIndexChanged.connect(lambda: self.ValuetoHex(ui))
##############  Database&Combobox
##        indexOfSetupsCombobox
  
        def ComboboxDB():
            if ui.Setups_ComboBox.currentText() != '':
                self.globalnameDB = ui.Setups_ComboBox.currentText()+'.db'
                self.SaveDB(ui, self.globalnameDB)
            print(self.globalnameDB + " created")
        ui.actionExit.triggered.connect(lambda: self.SaveComboboxDB(ui))
        ui.actionExit.triggered.connect(lambda: self.ReceiveComboboxDB(ui))
        
        ui.Setups_ComboBox.currentIndexChanged.connect(lambda: ComboboxDB())
        ui.RFFrequency_ScrollBar.valueChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.PADACOutputBias_ScrollBar.valueChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.RXVGAGain_ScrollBar.valueChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.TXVGAGain_ScrollBar.valueChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.RXLNAGain_ComboBox.currentIndexChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.TXBasebandGain_ComboBox.currentIndexChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))        
        ui.Max2828_ComboBox.currentIndexChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))        
        ui.Max5866_ComboBox.currentIndexChanged.connect(lambda: self.SaveDB(ui, self.globalnameDB))
        ui.Setups_ComboBox.currentIndexChanged.connect(lambda: self.ReceiveDB(ui, self.globalnameDB))
        
                                                 
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.RF_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.PADAC_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.RX_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.TX_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.LNA_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.mainFunction(self.GAIN_Package))
        ui.SendAll_Button.clicked.connect(lambda: self.checktoDestination())
      
##############        
##############
        sys.exit(app.exec_())


if __name__ == "__main__":
    Edit = WindowEdit()
    Edit.mainLoop()






    






