/*
 * ============================================
 * ROVER MODULE - Робот с навигацией по маякам
 * ============================================
 * 
 * Назначение: Принимает сигналы от маяков и движется к выбранному
 * Оборудование: ESP32 + LoRa + GPS + Драйвер моторов + Моторы
 * 
 * Функции:
 * - Принимает пакеты от маяков через LoRa
 * - Вычисляет расстояние и направление до маяков
 * - Управляет моторами для движения к выбранному маяку
 * - Отображает информацию на OLED дисплее
 */

#include <SPI.h>
#include <WiFi.h>
#include <LoRa.h>
#include <Arduino.h>
#include <TinyGPS++.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ========== LoRa настройки ==========
#define SS      18
#define RST     14
#define DI0     26
#define BAND    915E6  // 915 МГц (для России/США) или 433E6 (для Европы)

// ========== OLED дисплей ==========
#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

// ========== Драйвер моторов (TB6612FNG) ==========
// Мотор A (левый)
#define AIN1 32
#define AIN2 33
#define PWMA 25

// Мотор B (правый)
#define BIN1 4
#define BIN2 16
#define PWMB 17

// Скорость моторов (0-255)
#define MOTOR_SPEED 200
#define TURN_SPEED 150

// ========== Структуры данных ==========
struct Direction {
  int distanceFt;
  double distanceMiles;
  double heading;  // Направление в градусах (0-359)
  char ordinal[4];
};

struct Beacon {
  double lat, lng;
  char label[6];
  int rssi;
  int speed;
  unsigned long lastSeen;  // Время последнего получения пакета
  Direction locDirection;  // Направление от робота к маяку
};

// ========== Параметры устройства ==========
const int rosterSize = 20;        // Максимальное количество маяков
int rosterEntries = 0;             // Текущее количество маяков
Beacon roster[rosterSize];
int selectedBeaconIndex = 0;       // Выбранный маяк для навигации

// ========== Глобальные переменные ==========
TinyGPSPlus gps;
bool gpsFix = false;
bool navigationEnabled = false;    // Включена ли навигация

// Смещение координат (должно совпадать с маяком)
const double latOffset = 39.0;
const double lngOffset = 118.0;

// ========== Кнопка управления ==========
const int buttonPin = 2;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
const int debounceDelay = 50;

// ========== Функция ожидания с обработкой GPS ==========
static void wait(unsigned long ms) {
  unsigned long start = millis();
  do {
    while (Serial1.available())
      gps.encode(Serial1.read());
  } while (millis() - start < ms);
}

// ========== Функции управления моторами ==========
void motorStop() {
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 0);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMB, 0);
}

void motorForward() {
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, MOTOR_SPEED);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMB, MOTOR_SPEED);
}

void motorBackward() {
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  analogWrite(PWMA, MOTOR_SPEED);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
  analogWrite(PWMB, MOTOR_SPEED);
}

void motorTurnLeft() {
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  analogWrite(PWMA, TURN_SPEED);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMB, TURN_SPEED);
}

void motorTurnRight() {
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, TURN_SPEED);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
  analogWrite(PWMB, TURN_SPEED);
}

// ========== Вычисление направления и расстояния ==========
Direction getDirections(double originLat, double originLng, double targetLat, double targetLng) {
  double distanceMeters = gps.distanceBetween(originLat, originLng, targetLat, targetLng);
  double courseTo = gps.courseTo(originLat, originLng, targetLat, targetLng);
  const char* ordinal = gps.cardinal(courseTo);
  
  Direction dir;
  dir.distanceFt = (distanceMeters * 3.28084);
  dir.distanceMiles = (distanceMeters / 1609.3400);
  dir.heading = courseTo;
  strcpy(dir.ordinal, ordinal);
  
  return dir;
}

// ========== Обработка входящего пакета ==========
void handleIncomingPacket(char* passPacket, int passSize, int rssi) {
  Beacon beacon;
  char pckt[50];
  strncpy(pckt, passPacket, passSize);
  pckt[passSize] = '\0';
  
  int dataCounter = 0;
  int startPoint = 0;
  char curBuffer[50];
  char delimiter = ' ';
  
  // Парсинг пакета
  for (int i = 0; i < strlen(pckt); i++) {
    if (pckt[i] != delimiter) {
      curBuffer[i - startPoint] = pckt[i];
    } else {
      curBuffer[i - startPoint] = '\0';
      
      if (dataCounter == 0) {
        strncpy(beacon.label, curBuffer, 5);
        beacon.label[5] = '\0';
      } else if (dataCounter == 1) {
        beacon.lat = atof(curBuffer) + latOffset;  // Восстанавливаем координаты
      } else if (dataCounter == 2) {
        beacon.lng = atof(curBuffer) + lngOffset;
      } else if (dataCounter == 3) {
        beacon.speed = atoi(curBuffer);
      }
      
      memset(curBuffer, 0, sizeof(curBuffer));
      startPoint = i + 1;
      ++dataCounter;
    }
  }
  
  // Обработка последнего поля
  if (dataCounter == 3 && strlen(curBuffer) > 0) {
    beacon.speed = atoi(curBuffer);
  }
  
  beacon.rssi = rssi;
  beacon.lastSeen = millis();
  
  updateRosterWith(beacon);
}

// ========== Обновление реестра маяков ==========
void updateRosterWith(Beacon pBeacon) {
  Beacon beacon = pBeacon;
  int addAtRow = -1;
  
  // Поиск существующего маяка
  for (uint8_t i = 0; i < rosterSize; i++) {
    if (strcmp(roster[i].label, beacon.label) == 0) {
      addAtRow = i;
      break;
    }
  }
  
  // Если маяк новый, найти свободное место
  if (addAtRow == -1) {
    Serial.print("New beacon: ");
    Serial.println(beacon.label);
    rosterEntries++;
    for (uint8_t q = 0; q < rosterSize; q++) {
      if (roster[q].lat == 0) {
        addAtRow = q;
        break;
      }
    }
  }
  
  if (addAtRow == -1) {
    Serial.println("ERROR: Roster is full!");
    return;
  }
  
  // Вычисление направления от робота к маяку
  if (gps.location.isValid()) {
    beacon.locDirection = getDirections(
      gps.location.lat(), 
      gps.location.lng(), 
      beacon.lat, 
      beacon.lng
    );
  } else {
    // Если GPS недоступен, используем фиксированные координаты
    beacon.locDirection = getDirections(40.78110, -119.21143, beacon.lat, beacon.lng);
  }
  
  roster[addAtRow] = beacon;
  
  Serial.print("Beacon ");
  Serial.print(beacon.label);
  Serial.print(": ");
  Serial.print(beacon.locDirection.distanceFt);
  Serial.print(" ft, heading: ");
  Serial.println(beacon.locDirection.heading);
}

// ========== Навигация к выбранному маяку ==========
void navigateToBeacon() {
  if (rosterEntries == 0 || selectedBeaconIndex >= rosterEntries) {
    motorStop();
    return;
  }
  
  if (!gps.location.isValid()) {
    Serial.println("GPS not available for navigation");
    motorStop();
    return;
  }
  
  Beacon target = roster[selectedBeaconIndex];
  
  // Проверка актуальности данных маяка (не старше 10 секунд)
  if (millis() - target.lastSeen > 10000) {
    Serial.println("Beacon data too old");
    motorStop();
    return;
  }
  
  // Обновление направления
  target.locDirection = getDirections(
    gps.location.lat(),
    gps.location.lng(),
    target.lat,
    target.lng
  );
  
  double distance = target.locDirection.distanceFt;
  double heading = target.locDirection.heading;
  
  // Если очень близко, остановиться
  if (distance < 10) {  // 10 футов = ~3 метра
    motorStop();
    Serial.println("Target reached!");
    return;
  }
  
  // Получение текущего курса робота (упрощенно - используем GPS курс)
  double currentHeading = gps.course.deg();
  if (currentHeading < 0) currentHeading = 0;
  
  // Вычисление разницы углов
  double angleDiff = heading - currentHeading;
  
  // Нормализация угла к диапазону -180..180
  while (angleDiff > 180) angleDiff -= 360;
  while (angleDiff < -180) angleDiff += 360;
  
  // Управление моторами на основе угла
  if (abs(angleDiff) < 15) {
    // Движение вперед
    motorForward();
    Serial.print("Forward, dist: ");
    Serial.println(distance);
  } else if (angleDiff > 0) {
    // Поворот вправо
    motorTurnRight();
    Serial.print("Turn right, angle: ");
    Serial.println(angleDiff);
  } else {
    // Поворот влево
    motorTurnLeft();
    Serial.print("Turn left, angle: ");
    Serial.println(angleDiff);
  }
}

// ========== Обновление экрана ==========
void updateScreen() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  
  if (rosterEntries == 0) {
    display.println("No beacons");
    display.display();
    return;
  }
  
  display.print("Beacons: ");
  display.println(rosterEntries);
  display.print("Selected: ");
  display.println(roster[selectedBeaconIndex].label);
  
  if (gps.location.isValid()) {
    display.print("Dist: ");
    display.print(roster[selectedBeaconIndex].locDirection.distanceFt);
    display.println(" ft");
    display.print("Dir: ");
    display.println(roster[selectedBeaconIndex].locDirection.ordinal);
  } else {
    display.println("No GPS");
  }
  
  if (navigationEnabled) {
    display.println("NAV: ON");
  } else {
    display.println("NAV: OFF");
  }
  
  display.display();
}

// ========== Обработка кнопки ==========
void checkButton() {
  int reading = digitalRead(buttonPin);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading == LOW && lastButtonState == HIGH) {
      // Кнопка нажата
      if (rosterEntries > 0) {
        selectedBeaconIndex = (selectedBeaconIndex + 1) % rosterEntries;
        Serial.print("Selected beacon: ");
        Serial.println(roster[selectedBeaconIndex].label);
      }
    } else if (reading == HIGH && lastButtonState == LOW) {
      // Кнопка отпущена - переключение навигации
      navigationEnabled = !navigationEnabled;
      Serial.print("Navigation: ");
      Serial.println(navigationEnabled ? "ON" : "OFF");
      if (!navigationEnabled) {
        motorStop();
      }
    }
  }
  
  lastButtonState = reading;
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  Serial.println("=== ROVER MODULE STARTING ===");
  
  // Настройка кнопки
  pinMode(buttonPin, INPUT_PULLUP);
  
  // Настройка GPS
  Serial1.begin(9600, SERIAL_8N1, 12, 15);
  
  // Отключение WiFi и Bluetooth
  WiFi.mode(WIFI_OFF);
  btStop();
  
  // Настройка LoRa
  SPI.begin(5, 19, 27, 18);
  LoRa.setPins(SS, RST, DI0);
  
  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  
  LoRa.setTxPower(18);
  LoRa.setSpreadingFactor(7);
  LoRa.setCodingRate4(5);
  LoRa.setSignalBandwidth(31.25E3);
  LoRa.crc();
  
  Serial.println("LoRa initialized");
  
  // Настройка OLED дисплея
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Rover starting...");
  display.display();
  
  // Настройка пинов моторов
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  
  motorStop();
  
  Serial.println("Setup complete");
  Serial.println("Waiting for GPS fix...");
}

// ========== MAIN LOOP ==========
void loop() {
  // Обработка GPS
  while (Serial1.available()) {
    gps.encode(Serial1.read());
  }
  
  // Проверка GPS фикса
  if (gps.satellites.value() <= 3) {
    if (gpsFix) {
      Serial.println("Lost GPS fix...");
      gpsFix = false;
    }
  } else {
    if (!gpsFix) {
      Serial.println("GPS fix acquired!");
      gpsFix = true;
    }
  }
  
  // Прием пакетов от маяков
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    char packet[50] = "";
    int pointer = 0;
    while (LoRa.available() && pointer < 49) {
      packet[pointer] = (char)LoRa.read();
      pointer++;
    }
    packet[pointer] = '\0';
    handleIncomingPacket(packet, pointer, LoRa.packetRssi());
  }
  
  // Обработка кнопки
  checkButton();
  
  // Навигация (каждые 500 мс)
  static unsigned long lastNavTime = 0;
  if (navigationEnabled && (millis() - lastNavTime > 500)) {
    navigateToBeacon();
    lastNavTime = millis();
  } else if (!navigationEnabled) {
    motorStop();
  }
  
  // Обновление экрана (каждые 1 секунду)
  static unsigned long lastScreenUpdate = 0;
  if (millis() - lastScreenUpdate > 1000) {
    updateScreen();
    lastScreenUpdate = millis();
  }
  
  wait(50);
}

