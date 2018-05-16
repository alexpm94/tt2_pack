#include <TimerOne.h>
#include <ros.h>    /*#include <std_msgs/THE_TYPE_OF_THE_MESSAGE_YOU_SUBSCRIBER>*/
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>

const int ledPin = LED_BUILTIN;//LED pin
const int Trigger = 8;          //Pin digital 8  Trigger  sensor  
const int Echo = 9;             //Pin digital 9  Echo     sensor
const int pinRele = 12;         //Pin digital  Rele signal
const int pinPanel = 11;        //Pin digital   Panel signal
bool genuinoState;              //User_detected_state
volatile unsigned long blinkCount = 1;

ros::NodeHandle nh;

/*ROS_CALLBACK GENUINO_STATE*/
void messageCb(const std_msgs::Bool& msg){
  bool genuinoState;
  genuinoState=msg.data;

  if(genuinoState==true)
  {
    digitalWrite(pinRele,LOW);
   // digitalWrite(LED_BUILTIN, HIGH);    
   delay(800000);
    digitalWrite(pinRele,HIGH);
  }
    
    
   // digitalWrite(LED_BUILTIN, LOW);
}
/*Declaring ROS objects*/
/*SUBSCRIBERS*/
  ros::Subscriber<std_msgs::Bool> sub("genuinoState", &messageCb); //Blink & User
/*PUBLISHER*/
  std_msgs::Int32 str_msg;
  ros::Publisher chatter("sensorDistance", &str_msg); //Distancia_sensor_ultrasonico
  
void setup() {
/*SETUP  OUTPUTS*/
  pinMode(pinRele,OUTPUT);      
  digitalWrite(pinRele, HIGH);    //RELAY1 LOW_ENABLED   
  pinMode(pinPanel,OUTPUT);    
  digitalWrite(pinPanel, LOW);   //RELAY2 LOW_ENABLED 
/*SETUP ULTRASONIC SENSOR*/
  pinMode(Trigger, OUTPUT);       //SESNOR_PIN OUTPUT
  pinMode(Echo, INPUT);           //SENSOR_PIN INPUT
  digitalWrite(Trigger, LOW);     //SET PIN AS LOW
 // Serial.begin(9600);
/*TIMER SETUP*/
  Timer1.initialize(1000000);     //1 seg
/*ROS Node initialization*/
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
}

 /**ULTRASONIC SENSOR**/
float distance_cm(){ 
  float t,d;  //time, distance
  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  t = pulseIn(Echo, HIGH);  //obtenemos el ancho del pulso
  d = 0.017*t;             //escalamos el tiempo a una distancia en cm
  delay(80);               //60 ms Datasheet
  return d;
}

/*ISR_TIMER CALLBACK*/
   void ISR_Blink()
   {         blinkCount++;   }    // Contador veces se enciende el LED  

void loop() {
  float cm,N;
  cm = distance_cm();
  noInterrupts();               
  N = blinkCount;
  
if(cm<81|| cm>120){
   Timer1.attachInterrupt(ISR_Blink);
   blinkCount=1;
}

if(N>20) // seg
{
 Timer1.detachInterrupt();
 blinkCount=0; 
}
else if(N==0)
{
   digitalWrite(pinPanel,HIGH); //disabled 
}
else if(N>0)
{
  digitalWrite(pinPanel,LOW); //enabled
}
Serial.print("cm = ");
Serial.print(cm);
Serial.print("N = ");
Serial.println(N);
 /*ROS*/  /*PUBLISHER*/
  str_msg.data = cm;
  chatter.publish( &str_msg ); 
  nh.spinOnce(); 
  interrupts();    
}
