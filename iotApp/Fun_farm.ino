#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include "DHT.h"


#define POWER_PIN 32 //D0 - d32
#define A0_PIN 36 //A0 - VP
#define dhttype DHT21
#define dhtpin 4 //tín hiệu Dht21

LiquidCrystal_I2C lcd(0x27, 16, 2);  
Servo myServo;
int servoPin = 5;//tín hiệu servo
const int relayPin = 23;//tín hiệu relay
const char* ssid = "Realme 7";
const char* password = "09032004";
float h,t;
bool isRaining;
int currentServoPosition = 0; //vị trí ban đầu của servo
DHT dht(dhtpin, dhttype);

void setup() {
  Wire.begin();          
  pinMode(POWER_PIN, OUTPUT);
  dht.begin();
  myServo.attach(servoPin);
  myServo.write(currentServoPosition);
  lcd.init();                   
  lcd.backlight();

  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  pinMode(relayPin, OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
}

void postData(float t, float h, bool isRaining) {
  
    HTTPClient http;
    http.begin("http://54.179.144.116:8000/update_data/");
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"temperature\": " + String(t) + ", \"humidity\": " + String(h) + ", \"rain\": " + (isRaining ? "true" : "false") + "}";
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
}

void getData() {
    HTTPClient http;
    http.begin("http://54.179.144.116:8000/get_data/");
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Dữ liệu nhận được:");
      Serial.println(response);

      StaticJsonDocument<300> doc;
      DeserializationError error = deserializeJson(doc, response);

      if (error) {
        Serial.print("Lỗi phân tích JSON: ");
        Serial.println(error.c_str());
      } else {
        int pump = doc["pump"].as<int>();
        int servo = doc["servo"].as<int>();

        Serial.print("Pump: ");
        Serial.println(pump);
        Serial.print("Servo: ");
        Serial.println(servo);

        digitalWrite(relayPin, pump == 1 ? HIGH : LOW);
        
        if (servo == 1 && currentServoPosition == 0) {
          Serial.println("Mở Servo");
          myServo.write(90);
          currentServoPosition = 90;
        } else if (servo == 0 && currentServoPosition == 90) {
          Serial.println("Đóng Servo");
          myServo.write(0);
          currentServoPosition = 0;
        }
      }
    } else {
      Serial.print("Lỗi khi gửi yêu cầu GET: ");
      Serial.println(httpResponseCode);
    }
    http.end();
}
bool Rain(){
  int sensorValue = analogRead(A0_PIN);
  bool isRaining = sensorValue < 4095;
  return isRaining;
}

void LCD(float t, float h){
  lcd.setCursor(0, 0);
  lcd.print("Humidity: ");
  lcd.print(String(h));
  lcd.print("%");
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(String(t));
  lcd.print("*C ");
  delay(1000);
}
void loop() {
  isRaining = Rain();
  float h1 = dht.readHumidity();
  float t1 = dht.readTemperature();
  if (!isnan(h1) && !isnan(t1)){
    h = h1;
    t = t1;
  }
  Serial.println(t);
  Serial.println(h);
  LCD(t, h);
  if (WiFi.status() == WL_CONNECTED) {
    postData(t, h, isRaining);
    getData();
  }
  delay(10);
}
