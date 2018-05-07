#include <ros.h>    /*#include <std_msgs/THE_TYPE_OF_THE_MESSAGE_YOU_SUBSCRIBER>*/
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>

const int ledPin = LED_BUILTIN;//LED pin
const int Trigger = 8;          //Pin digital 8  Trigger  sensor
const int Echo = 9;             //Pin digital 9  Echo     sensor
const int pinRele = 12;         //Pin digital  Rele signal
const int pinPanel = 11;       //Pin digital   Panel signal
bool genuinoState;     //User_detected_state

  unsigned int contador = 0;

ros::NodeHandle nh;

/*CALLBACK GENUINO_STATE*/
void messageCb(const std_msgs::Bool& msg){
  bool genuinoState;
  genuinoState=msg.data;

  if(genuinoState==true)
  {
    digitalWrite(pinRele,LOW);
digitalWrite(LED_BUILTIN, HIGH);    
    delay(4000);
  }
    else
    digitalWrite(pinRele,HIGH);
    digitalWrite(LED_BUILTIN, LOW);
}
/*Declaring ROS objects*/
/*SUBSCRIBERS*/
  ros::Subscriber<std_msgs::Bool> sub("genuinoState", &messageCb); //Blink & User
/*PUBLISHER*/
  std_msgs::Int32 str_msg;
  ros::Publisher chatter("sensorDistance", &str_msg);              //Distancia_sensor_ultrasonico
  
void setup() {
/*SETUP  OUTPUTS*/
  pinMode(pinRele,OUTPUT);
  digitalWrite(pinRele, HIGH);
  pinMode(pinPanel,OUTPUT);
  digitalWrite(pinPanel, HIGH);
/*SETUP ULTRASONIC SENSOR*/
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
  Serial.print(contador);
  Serial.print("  ");
    Serial.println(cm);

if(cm<80 || cm>90){
   contador=contador+1;
   if(contador>0){
      digitalWrite(pinPanel,LOW); //enabled
   }
  delay(10);
}


if (contador>1000){
  contador=0;
  digitalWrite(pinPanel,HIGH); //disabled
}
 /*ROS*/  /*PUBLISHER*/
  str_msg.data = cm;
  chatter.publish( &str_msg ); 
  nh.spinOnce(); 
}

