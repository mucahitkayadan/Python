#include <header.h>

class myFuncs funcs;
char starter_byte     = 0XAA;
char source_byte      = 0X01;
char destination_byte = 0X02;
char command_byte;
char ack_byte;
int ndx = 0;
char pack[12];
char pack_ack[5];
int state;
int current_byte;
int packNum;

void prepare_ack();
     
void setup() {
  Serial.begin(9600);
  while(!Serial){;}
  state = 0;
  current_byte = 0;
  packNum = 1;
  pinMode(13, OUTPUT);
  //digitalWrite(13,LOW);
}

void loop() {
        switch (state){
          case 0:
            if(Serial.available() > 0){              
              pack[0] = Serial.read();
              if(char(pack[0]) == char(0xAA)){
                //Working
                state = 1;
                current_byte = 1;
              }
            }
            break;
          case 1:
            if(Serial.available() > 0){
              pack[current_byte]= Serial.read();
              current_byte++;
              if(current_byte >= 12){
                state = 2;
              }
            }
            break;
          case 2:
            if( funcs.checkCommandTotal(packNum, pack[4], pack[5]) && funcs.checkStarter(pack[0]) && 
            funcs.checkSource(pack[1]) && funcs.checkDest(pack[2]) && funcs.checkCommand(pack[3])){
               ack_byte = 0X01;
            }else{
               ack_byte = 0X00;
            }
            packNum++;
            state = 3;
            if(packNum == 8){ packNum = 1; }
            break;            
          case 3:
            prepare_ack();
            state = 4;
            current_byte = 0;
            break;
          case 4:
            if(Serial.availableForWrite() > 0)
            Serial.write(pack_ack[current_byte]);
            current_byte++;
            if(current_byte == 5){
              state = 0;
            }
            break;
          }
   
  }


  void prepare_ack(){
  pack_ack[0] = pack[0];
  pack_ack[1] = pack[2];
  pack_ack[2] = pack[1];
  pack_ack[3] = pack[3];
  pack_ack[4] = ack_byte;
  }
     
  
