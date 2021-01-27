#include <OneWire.h>
#include <DallasTemperature.h>
#include "BluetoothSerial.h"
#include "esp_bt_device.h"
#include "DHT.h"

#define DHTPIN 16
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

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
  
  dht.begin();
}

void loop() {
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureF = sensors.getTempFByIndex(0);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  String humidity = "Humidity : " + String(h)+ " / Temperature : " + String(t) + "C / " + String(f) + "F";
  String temperature = String(temperatureC) + "C / " + String(temperatureF) + "F";
  Serial.println(temperature);
  Serial.println(humidity);
  String DataToSend = "{\"humidity_DHT11\": " + String(h) + ", \"temperatureC_Dallas\": " + String(temperatureC) + ", \"temperatureF_Dallas\": " + String(temperatureF) + "}";
  Serial.println(DataToSend);

  if (Serial.available()) {
    SerialBT.write(Serial.print(DataToSend));
    //SerialBT.write(Serial.print(temperature));
    //SerialBT.write(Serial.print(humidity));
  }
  if (SerialBT.available()) {
    Serial.write(SerialBT.print(DataToSend));
    Serial.write(SerialBT.read());
    //Serial.write(SerialBT.print(temperature));
    //Serial.write(SerialBT.print(humidity));
  }
  
  delay(5000);
}
