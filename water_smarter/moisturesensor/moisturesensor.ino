#define Moisture A0 //The definition of AO pin IO-A0 
#define DO 7        //The definition of DO pin IO-7  
  
void setup() {  
  pinMode(Moisture, INPUT); //Define A0 as input mode  
  pinMode(DO, INPUT);  
  Serial.begin(9600);  
}  
  
void loop() {  
  //Returns the serial measurement data  
  Serial.print("Moisture=");  
  Serial.print(analogRead(Moisture));//Numerical read AO
  Serial.print("|DO=");  
  Serial.println(digitalRead(DO));//Numerical read DO  
  delay(1000);  
} 
