#include <LoRa_E220.h>

#define AUX 32
#define M0 38
#define M1 40

LoRa_E220 e220ttl(&Serial2, AUX, M0, M1);

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);

  pinMode(M0, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(AUX, INPUT);

  digitalWrite(M0, LOW);
  digitalWrite(M1, LOW);

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
  ResponseContainer rc = e220ttl.receiveMessage();

  if (rc.status.code == 1 && rc.data.length() == 4) {
    int16_t humidity_int, temperature_int;

    memcpy(&humidity_int, rc.data.c_str(), 2);
    memcpy(&temperature_int, rc.data.c_str() + 2, 2);

    float humidity = humidity_int / 100.0;
    float temperature = temperature_int / 100.0;

    Serial.print("Получено: Влажность = ");
    Serial.print(humidity);
    Serial.print("%, Температура = ");
    Serial.print(temperature);
    Serial.println("°C");
  } else {
    Serial.println("Ошибка при приёме сообщения или некорректный размер данных.");
  }

  delay(5000);
}