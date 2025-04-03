
/*
  Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
  Ported to Arduino ESP32 by Evandro Copercini
  updated by chegewara and MoThunderz
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Adafruit_NeoPixel.h>

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
BLEDescriptor* pDescr;
BLE2902* pBLE2902;

bool deviceConnected = false;
bool oldDeviceConnected = false;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, 10, NEO_GRB + NEO_KHZ800);

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};

void setup() {
  Serial.begin(115200);
  pixels.begin();
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(70, 255, 0));
  pixels.show();

  // Create the BLE Device
  BLEDevice::init("AudioMixer - 00");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService* pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_NOTIFY);


  pBLE2902 = new BLE2902();
  pBLE2902->setNotifications(true);
  pCharacteristic->addDescriptor(pBLE2902);

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");
  
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();
}

uint8_t slider[] = { 0, 0, 0, 0, 0 };
uint8_t data[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
uint8_t prevSlider[] = { 0, 0, 0, 0, 0 };

void loop() {
  // notify changed value
  if (deviceConnected) {
    if (updateValues()) {
      //generateValue();
      pCharacteristic->setValue(slider, 5);
      pCharacteristic->notify();
    }
    delay(100);
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    pixels.setPixelColor(0, pixels.Color(0, 255, 0));
    pixels.show();
    delay(100);                   // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising();  // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    pixels.setPixelColor(0, pixels.Color(0, 0, 255));
    pixels.show();
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
    Serial.println("connected");
    delay(100);
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
    
  }
}

bool updateValues() {
  bool update = false;
  uint16_t val = 0;
  for (int i = 0; i < 5; i++) {
    val = analogRead(i);
    val = 110 - int(floatMap(log(val+13.1616887)/log(13.1616887), 1.0, 3.01, 0.0, 110.0));
    //Serial.printf("%d: %d -> %f -> %f\t", i, val, log(val+13.1616887)/log(13.1616887), floatMap(log(val+13.1616887)/log(13.1616887), 1.0, 3.01, 0.0, 100.0));
    if (abs(val - prevSlider[i]) >= 2 && val <= 95) {
      slider[i] = val;
      update = true;
    }
    prevSlider[i] = val;
  }
  //Serial.println("");
  return update;
}

void generateValue() {
  for (int i = 0; i < 5; i++) {
    data[i/2] = slider[i];
    data[i/2+1] = slider[i] >> 8;
  }
  //Serial.printf("primo: %d %d -> %d, secondo: %d %d -> %d, terzo: %d %d -> %d, quarto: %d %d -> %d, quinto: %d %d -> %d\n", data[0], data[1], slider[0], data[2], data[3], slider[1], data[4], data[5], slider[2], data[6], data[7], slider[3], data[8], data[9], slider[4]);
}

float floatMap(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
