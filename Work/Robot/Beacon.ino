/*
 * ============================================
 * BEACON MODULE - Маяк для навигации робота
 * ============================================
 * 
 * Назначение: Передает GPS координаты через LoRa
 * Оборудование: ESP32 + LoRa модуль + GPS модуль
 * 
 * Функции:
 * - Получает GPS координаты
 * - Передает их через LoRa каждые 2 секунды
 * - Формат пакета: "LABEL LAT LNG SPEED"
 */

#include <SPI.h>
#include <WiFi.h>
#include <LoRa.h>
#include <Arduino.h>
#include <TinyGPS++.h>

// ========== LoRa настройки ==========
#define SS      18
#define RST     14
#define DI0     26
#define BAND    915E6  // 915 МГц (для России/США) или 433E6 (для Европы)

// ========== GPS настройки ==========
// GPS подключен к Serial1: TX=12, RX=15

// ========== Параметры устройства ==========
const char deviceName[] = "BKN01";  // Имя маяка (макс 5 символов)
const int txInterval = 2000;        // Интервал передачи (мс)
const int userRadioId = 1;          // ID для временной синхронизации
const int modValue = 5;             // Модуль для синхронизации

// ========== Глобальные переменные ==========
TinyGPSPlus gps;
int sentPacketCount = 0;
bool gpsFix = false;

// ========== Смещение координат (из оригинального кода) ==========
const double latOffset = 39.0;
const double lngOffset = 118.0;

// ========== Функция ожидания с обработкой GPS ==========
static void wait(unsigned long ms) {
  unsigned long start = millis();
  do {
    while (Serial1.available())
      gps.encode(Serial1.read());
  } while (millis() - start < ms);
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  Serial.println("=== BEACON MODULE STARTING ===");
  
  // Настройка GPS
  Serial1.begin(9600, SERIAL_8N1, 12, 15);  // TX=12, RX=15
  
  // Отключение WiFi и Bluetooth для экономии энергии
  WiFi.mode(WIFI_OFF);
  btStop();
  
  // Настройка LoRa
  SPI.begin(5, 19, 27, 18);
  LoRa.setPins(SS, RST, DI0);
  
  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  
  // Настройка параметров LoRa
  LoRa.setTxPower(18);              // Мощность передачи (2-20 dBm)
  LoRa.setSpreadingFactor(7);        // SF7 (баланс скорости/дальности)
  LoRa.setCodingRate4(5);           // Coding rate 5
  LoRa.setSignalBandwidth(31.25E3);  // Полоса пропускания 31.25 kHz
  LoRa.crc();                        // Включить CRC
  
  Serial.println("LoRa initialized successfully");
  Serial.print("Device name: ");
  Serial.println(deviceName);
  Serial.print("Transmission interval: ");
  Serial.print(txInterval);
  Serial.println(" ms");
  Serial.println("Waiting for GPS fix...");
}

// ========== MAIN LOOP ==========
void loop() {
  // Обработка GPS данных
  while (Serial1.available()) {
    gps.encode(Serial1.read());
  }
  
  // Проверка наличия GPS фикса
  if (gps.satellites.value() <= 3) {
    if (gpsFix) {
      Serial.println("Lost GPS fix...");
      gpsFix = false;
    }
    wait(1000);
    return;
  }
  
  // Первый фикс GPS
  if (!gpsFix) {
    Serial.println("GPS position found!");
    Serial.print("Lat: ");
    Serial.print(gps.location.lat(), 6);
    Serial.print(", Lng: ");
    Serial.println(gps.location.lng(), 6);
    gpsFix = true;
  }
  
  // Передача координат по расписанию (временная синхронизация)
  if (gps.time.isValid() && (gps.time.second() % modValue == userRadioId)) {
    transmitLocation();
  } else if (!gps.time.isValid()) {
    // Если время GPS недоступно, передаем каждые txInterval мс
    static unsigned long lastTx = 0;
    if (millis() - lastTx >= txInterval) {
      transmitLocation();
      lastTx = millis();
    }
  }
  
  wait(100);
}

// ========== Передача координат ==========
void transmitLocation() {
  if (!gps.location.isValid()) {
    Serial.println("GPS location invalid, skipping transmission");
    return;
  }
  
  sentPacketCount++;
  
  // Применяем смещение координат (как в оригинальном коде)
  const double sendableLat = (gps.location.lat() - latOffset);
  const double sendableLng = (gps.location.lng() - lngOffset);
  const int sendableSpeed = gps.speed.mph();
  
  Serial.print("[TX #");
  Serial.print(sentPacketCount);
  Serial.print("] Sending: ");
  Serial.print(deviceName);
  Serial.print(" ");
  Serial.print(sendableLat, 5);
  Serial.print(" ");
  Serial.print(sendableLng, 5);
  Serial.print(" ");
  Serial.println(sendableSpeed);
  
  // Отправка пакета через LoRa
  LoRa.beginPacket();
  LoRa.print(deviceName);
  LoRa.print(" ");
  LoRa.print(sendableLat, 5);  // 5 знаков после запятой = точность ~1.1м
  LoRa.print(" ");
  LoRa.print(sendableLng, 5);
  LoRa.print(" ");
  LoRa.print(sendableSpeed);
  LoRa.print(" ");
  LoRa.print(sentPacketCount);
  LoRa.endPacket();
  
  Serial.print("Packet sent. RSSI: ");
  Serial.println(LoRa.packetRssi());
}

