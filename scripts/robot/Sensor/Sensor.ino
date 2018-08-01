const int sensor = A0;

void setup(){
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);
  pinMode(A6, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop(){
  int value = analogRead(sensor);
  
  Serial.println(value);
  if (value > 380){
    Serial.println("blaque");
    digitalWrite(A5,LOW); 
    digitalWrite(A6,LOW);
    digitalWrite(A4,HIGH);
  }
  else if (value > 280){
    Serial.println("grey");
    digitalWrite(A4,LOW);
    digitalWrite(A6,LOW);
    digitalWrite(A5,HIGH);
  }
  else{
    Serial.println("white");
    digitalWrite(A4,LOW);
    digitalWrite(A5,LOW);
    digitalWrite(A6,HIGH);
  }
  delay(500);
}
