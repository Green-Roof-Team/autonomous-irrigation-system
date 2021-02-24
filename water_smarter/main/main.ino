int solenoidPin = 4;    //This is the output pin on the Arduino we are using
#define Moisture A0 //The definition of AO pin IO-A0 
#define DO 7        //The definition of DO pin IO-7 
 
void setup() {
  // put your setup code here, to run once:
  pinMode(Moisture, INPUT);//Define A0 as input mode  
  pinMode(DO, INPUT);  
  pinMode(solenoidPin, OUTPUT);           //Sets the pin as an output
  Serial.begin(9600); 
  Serial.println("  Moist?");  
}
 
void loop() {
  if(analogRead(Moisture) < 666){
     Serial.println("0");
   } else if(analogRead(Moisture) <= 315){
     Serial.println("-");
   } else {
     Serial.println("1");
     }
  
  if((analogRead(Moisture)) < 310){
    //Turn solenoid valve off
    digitalWrite(solenoidPin, LOW);     //Switch Solenoid OFF
    //Serial.println("Solenoid Valve is OFF");  
    delay(5000);                      //Wait 5 Second
  }

  if((analogRead(Moisture)) > 900){
    //Turn solenoid valve on
    digitalWrite(solenoidPin, HIGH);     //Switch Solenoid OFF
    //Serial.println("Solenoid Valve is ON");  
    delay(5000);                      //Wait 5 Second
  }

  if((analogRead(Moisture)) < 900 && (analogRead(Moisture)) > 310){
    //Turn solenoid valve on
    digitalWrite(solenoidPin, HIGH);     //Switch Solenoid OFF
    //Serial.println("Solenoid Valve is ON");  
    delay(5000);                      //Wait 5 Second
  }
  
}
