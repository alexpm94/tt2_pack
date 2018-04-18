#include <ros.h>    /*#include <std_msgs/THE_TYPE_OF_THE_MESSAGE_YOU_SUBSCRIBER>*/
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>

const int ledPin =  LED_BUILTIN;//LED pin
const int Trigger = 8;          //Pin digital 8  Trigger del sensor
const int Echo = 9;             //Pin digital 9  Echo del sensor
const int Rele = 6;             //Pin digital 6  Relay
//const int pushB=5;            //Push button 5  switch 
const int ledSensor=4;          //LedSensor 
const int ledUser=3;            //LedStatus for user_recognition
const int ledBlink=2;           //LedStatus for blink
 
bool genuinoState;     //User_detected_state

ros::NodeHandle nh;

/*CALLBACK GENUINO_STATE*/
void messageCb(const std_msgs::Bool& msg){
  bool genuinoState;
  genuinoState=msg.data;
  if(genuinoState==true)
  {
    digitalWrite(Rele,HIGH);
digitalWrite(LED_BUILTIN, HIGH);    
    delay(3000);
  }
    else
    digitalWrite(Rele,LOW);
    digitalWrite(LED_BUILTIN, LOW);
}

/*Declaring ROS objects*/
/*SUBSCRIBERS*/
  ros::Subscriber<std_msgs::Bool> sub("genuinoState", &messageCb); //Blink & User
/*PUBLISHER*/
  std_msgs::Int32 str_msg;
  ros::Publisher chatter("sensorDistance", &str_msg);              //Distancia_sensor_ultrasonico
  
void setup() {
/*SETUP INPUTS*/
//  pinMode(pushB,INPUT);
/*SETUP LEDS ODER OUTPUTS*/
  pinMode(Rele,OUTPUT);
  pinMode(ledUser,OUTPUT);
  pinMode(ledSensor,OUTPUT);
/*SETUP SENSOR*/
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, LOW);//Inicializamos el pin con 0
  pinMode(13,OUTPUT);//LED
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
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = 0.017*t;             //escalamos el tiempo a una distancia en cm
  delay(80);               //60MS DATA  
  return d;
}

void loop() {
  float cm;
  bool aux1,aux2;
  cm = distance_cm();

 /*ROS*/
  str_msg.data = cm;
  chatter.publish( &str_msg ); 
  nh.spinOnce(); 

}
