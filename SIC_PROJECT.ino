#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define MQ135PIN 34

const char* ssid = "H1R0'";
const char* password = "RUM4H4LL0H";
const char* serverName = "http://192.168.1.7:5000/api/data"; // Ganti <IP_ADDRESS> dengan IP komputer server

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

const float TEMPERATURE_THRESHOLD = 35.0; // Suhu batas normal
const float CO2_THRESHOLD = 1000.0;       // Kadar CO2 batas normal

void setup() {
  Serial.begin(115200);
  dht.begin();
  lcd.init();
  lcd.backlight();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float temperature = dht.readTemperature();
  int mq135_value = analogRead(MQ135PIN);
  float co2_ppm = (float)mq135_value * (5000.0 / 4096.0); // Konversi nilai ADC ke ppm untuk CO2
  
  // Tampilkan data di Serial Monitor
  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print(" C, CO2: ");
  Serial.print(co2_ppm);
  Serial.println(" ppm");
  
  // Tampilkan data di LCD
  lcd.clear();
  
  if (temperature > TEMPERATURE_THRESHOLD || co2_ppm > CO2_THRESHOLD) {
    lcd.setCursor(0, 0);
    lcd.print("Warning!");
    
    lcd.setCursor(0, 1);
    if (temperature > TEMPERATURE_THRESHOLD) {
      lcd.print("High Temp");
    }
    if (co2_ppm > CO2_THRESHOLD) {
      lcd.print("High CO2");
    }
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperature);
    lcd.setCursor(0, 1);
    lcd.print("CO2: ");
    lcd.print(co2_ppm);
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    
    String postData = "{\"temperature\":";
    postData += temperature;
    postData += ",\"co2\":";
    postData += co2_ppm;
    postData += "}";
    
    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
  
  delay(500); // Kirim data setiap 0,5 detik
}
