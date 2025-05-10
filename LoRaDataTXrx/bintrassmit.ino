// Подключение библиотек для LoRa и DHT
#include <LoRa_E220.h>
#include <SoftwareSerial.h>
#include <DHT.h>

// Пины для LoRa и DHT
#define M0 8
#define M1 9
#define AUX 12
#define DHTPIN 2
#define DHTTYPE DHT11

// Инициализация модулей
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial mySerial(10, 11);
LoRa_E220 e220ttl(&mySerial, AUX, M0, M1);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);

  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(AUX, INPUT);

  digitalWrite(M0, LOW);
  digitalWrite(M1, LOW);

  dht.begin();
  e220ttl.begin();

  ResponseStructContainer c = e220ttl.getConfiguration();
  if (c.status.code == 1) {
    Configuration configuration = *(Configuration*)c.data;
    configuration.CHAN = 18;
    e220ttl.setConfiguration(configuration);
  }
  c.close();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Не удалось считать данные с датчика");
    return;
  }

  int16_t humidity_int = humidity * 100;
  int16_t temperature_int = temperature * 100;

  uint8_t buffer[4];
  memcpy(buffer, &humidity_int, 2);
  memcpy(buffer + 2, &temperature_int, 2);

  e220ttl.sendMessage((const char*)buffer, sizeof(buffer));

  Serial.print("Отправлено: Влажность = ");
  Serial.print(humidity);
  Serial.print("%, Температура = ");
  Serial.print(temperature);
  Serial.println("°C");

  delay(5000);
}