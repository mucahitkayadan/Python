#ifndef HEADER_H_INCLUDED
#define HEADER_H_INCLUDED
#include "Arduino.h"

class myFuncs{
   public:
    bool checkStarter(int myByte);
    bool checkSource(int myByte);
    bool checkDest(int myByte);
    bool checkCommand(int myByte);
    bool checkCommand1(int *myByte);
    bool checkCommand1(int myByte1, int myByte2);
    bool checkCommand2(int myByte1, int myByte2);
    bool checkCommand3(int myByte1, int myByte2);
    bool checkCommand4(int myByte1, int myByte2);
    bool checkCommand5(int myByte1, int myByte2);
    bool checkCommand6(int myByte1, int myByte2);
    bool checkCommand7(int myByte1, int myByte2);
    bool checkCommandTotal(int param, int myByte1, int myByte2);
};


#endif // HEADER_H_INCLUDED
