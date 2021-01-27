#include <Servo_ESP32.h>

#include <dummy.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "BluetoothSerial.h"
#include "esp_bt_device.h"
#include "DHT.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
Servo_ESP32 myservo; 
int pos = 0; 
int servoPin = 18;
int trigger;

void printDeviceAddress() {
 
  const uint8_t* point = esp_bt_dev_get_address();
 
  for (int i = 0; i < 6; i++) {
 
    char str[3];
 
    sprintf(str, "%02X", (int)point[i]);
    Serial.print(str);
 
    if (i < 5){
      Serial.print(":");
    }
  }
}


void setup() {
  // Start the Serial Monitor
  Serial.begin(115200);
  // Start the DS18B20 sensor
  
  Serial.println("\n---Start---");
  SerialBT.begin("ESP32SensoolBis"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  Serial.println("Device Name: n");
  Serial.print("BT MAC: ");
  printDeviceAddress();
  Serial.println(); 
  myservo.attach(servoPin);
}

void loop() {
  int salut;
  if (SerialBT.available()) {
    salut = SerialBT.read();
    Serial.println(salut);
    //trigger = Serial.write(SerialBT.read());
    //trigger_int = trigger.toInt();
    //Serial.println(trigger);

    if(salut == 49){
      Serial.println("Hello2");
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo.write(pos);    // tell servo to go to position in variable 'pos'
        delay(15);             // waits 15ms for the servo to reach the position
      }
    }
  }
  
  delay(1000);
}
