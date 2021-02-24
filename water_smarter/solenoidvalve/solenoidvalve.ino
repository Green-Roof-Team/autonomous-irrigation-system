int solenoidPin = 4;    //This is the output pin on the Arduino we are using
 
void setup() {
  // put your setup code here, to run once:
  pinMode(solenoidPin, OUTPUT);           //Sets the pin as an output
  Serial.begin(9600);  
}
 
void loop() {
  //Returns the serial measurement data  

  digitalWrite(solenoidPin, HIGH);    //Switch Solenoid ON
  Serial.println("ON");  
  delay(10000);                      //Wait 1 Second

  digitalWrite(solenoidPin, LOW);     //Switch Solenoid OFF
  Serial.println("OFF");  
  delay(10000);                      //Wait 1 Second
}
