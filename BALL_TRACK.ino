#include <Servo.h>
#include <PID_v1.h>

int led = 4;
int led1 = 3;
Servo y;
int turnlr_time = 10;

double Kp=2, Ki=1, Kd=0.5;
double Setpoint, Input, Output;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(led,OUTPUT);
pinMode(led1,OUTPUT);

 y.attach(10);
y.writeMicroseconds(1600);

Setpoint = 86.00;
//myPID.SetOutputLimits(-255,255);
myPID.SetMode(AUTOMATIC);

}

void loop() 
{
  if(Serial.available() >0)
  {

int val = Serial.read();
double err = Setpoint-Input;
myPID.Compute();

if(err > 0)
{
  digitalWrite(led,1);
  digitalWrite(led1,0);

y.writeMicroseconds(1600+Output);
delay(turnlr_time);
y.writeMicroseconds(1600);
}

else if(err < 0)
{
 digitalWrite(led,0);
   digitalWrite(led1,1);
 

y.writeMicroseconds(1600 - Output);
delay(turnlr_time);
y.writeMicroseconds(1600);
}

  }
}
