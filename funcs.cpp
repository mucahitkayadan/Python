#include "Arduino.h"
#include "header.h"
bool myFuncs::checkStarter(int myByte){
  if (char(myByte) == char(0XAA)) return true; else return false;
  }
bool myFuncs::checkSource(int myByte){
  if (char(myByte) == char(0X01)) return true; else return false;
  }
bool myFuncs::checkDest(int myByte){
  if (char(myByte) == char(0X02)) return true;  else return false;//It will work just for max2828
  }
bool myFuncs::checkCommand(int myByte){
  if (char(myByte) >= char(0X01) && myByte <= char(0X07)) return true; else return false;
  }
bool myFuncs::checkCommand1(int *myByte){
    short int myInt;
    memcpy(myInt, myByte[4],2);
    if (myInt >= 4900 && myInt <= 5900) return true;  else return false;
  }
bool myFuncs::checkCommand1(int myByte1, int myByte2){ //RFFrequency
  if (char(myByte1) >= char(0X13) && char(myByte1) <= char(0X17)){
    if ((char(myByte1) == char(0X13)) && (char(myByte2) < char(0X24)) ){
        return false;
    }
    else if ((char(myByte1) == char(0X17)) && (char(myByte2) > char(0X0C)) ){
        return false;
    }
    else return true;
  }
  else return false;
    //if (char(myByte1+myByte2) >= char(0X1324) && char(myByte1+myByte2) <= char(0X170C)) return true; else return false;
  }
bool myFuncs::checkCommand2(int myByte1, int myByte2){ //PADAC
    if (char(myByte1) >= char(0X00) && char(myByte1) <= char(0X02)) return true;  else return false;
  /*int myInt1 = atoi(myByte1);
  int myInt2 = atoi(myByte2);
  int myInt = myInt1*100+myByte2;
  if (myInt >= 0 && myInt <= 512) return true;  else return false;*/
   // if (char(myByte1+myByte2) >= char(0X00) && char(myByte1+myByte2) <= char(0X200)) return true; else return false;
  }
bool myFuncs::checkCommand3(int myByte1, int myByte2){ //RX VGA Gain
  if (char(myByte1) == char(0X00) && char(myByte2) >= char(0X00) && char(myByte2) <= char(0X20))
    return true; else return false;
  }
bool myFuncs::checkCommand4(int myByte1, int myByte2){ //TX VGA Gain
  if ( char(myByte1) == char(0X00) && char(myByte2) >= char(0X00) && char(myByte2) <= char(0X40))
    return true;  else return false;
  }
bool myFuncs::checkCommand5(int myByte1, int myByte2){ //RX LNA Gain
  if (char(myByte1) == char(0X00) && char(myByte2) >= char(0X00) && char(myByte2) <= char(0X02))
    return true;  else return false;
  }
bool myFuncs::checkCommand6(int myByte1, int myByte2){ //TX LNA Gain
  if (char(myByte1) == char(0X00) && char(myByte2) >= char(0X00) && char(myByte2) <= char(0X01))
    return true;  else return false;
  }
bool myFuncs::checkCommand7(int myByte1, int myByte2){ //Device
  if (char(myByte1) == char(0X00) && ((char(myByte2) >= char(0X02) && char(myByte2) <= char(0X03)) || char(myByte2) == char(0X00)))
    return true;  else return false;
  }
bool myFuncs::checkCommandTotal(int param, int myByte1, int myByte2){
  switch(param){
    case 1: return  checkCommand1(myByte1,myByte2); break;
    case 2: return  checkCommand2(myByte1,myByte2); break;
    //case 1: return  checkCommand1(myByte1); break;
    //case 1: return true; break;
    //case 2: return true; break;
    case 3: return checkCommand3(myByte1,myByte2); break;
    case 4: return checkCommand4(myByte1,myByte2); break;
    case 5: return checkCommand5(myByte1,myByte2); break;
    case 6: return checkCommand6(myByte1,myByte2); break;
    case 7: return checkCommand7(myByte1,myByte2); break;
    default: return -1;
    }
  }

