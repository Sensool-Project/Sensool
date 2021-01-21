#include <OneWire.h>
#include <DallasTemperature.h>
#include "BluetoothSerial.h"
#include "esp_bt_device.h"


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


// GPIO where the DS18B20 is connected to
const int oneWireBus = 4;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

BluetoothSerial SerialBT;

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
  sensors.begin();
  
  Serial.println("\n---Start---");
  SerialBT.begin("ESP32Sensool"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  Serial.println("Device Name: ESP32Sensool");
  Serial.print("BT MAC: ");
  printDeviceAddress();
  Serial.println();
}

void loop() {
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureF = sensors.getTempFByIndex(0);
  String temperature = String(temperatureC) + "C / " + String(temperatureF) + "F";
  Serial.println(temperature);

  if (Serial.available()) {
    //SerialBT.write(Serial.read());
    SerialBT.write(Serial.print(temperature));
  }
  if (SerialBT.available()) {
    //Serial.write(SerialBT.read());
    Serial.write(SerialBT.print(temperature));
  }
  delay(5000);
}
