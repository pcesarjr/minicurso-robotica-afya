/*
  MINICURSO DE ROBÓTICA — Robô Sentinela
  Sketch 01: Teste de hardware

  Testa cada componente em sequência e imprime o resultado no Serial Monitor (9600 baud).
  Use antes de qualquer outra coisa: se algo não funcionar aqui, o problema é de montagem.

  Pinagem (igual em todos os sketches do curso):
    D2  botão GRAVAR (outro terminal no GND)
    D3,D4,D5,D6,A3,A4,A5  segmentos a,b,c,d,e,f,g do display (cada um com resistor 620R)
    D7  HC-SR04 TRIG     D8  HC-SR04 ECHO
    D9  servo (sinal)    D10 buzzer
    D11 LED vermelho     D12 LED verde     D13 LED azul   (cada LED com resistor 560R)
    A0  LDR (divisor com resistor 1k para o GND)
    A2  módulo relé (IN)
*/
#include <Servo.h>

// ---------- Ajustes conforme o SEU material ----------
const bool DISPLAY_ANODO_COMUM = false; // true se o pino comum do display vai no 5V
const bool BUZZER_ATIVO        = false; // true se o buzzer apita só com 5V (tem oscilador interno)
const bool RELE_ATIVO_BAIXO    = true;  // maioria dos módulos relé liga com LOW

// ---------- Pinos ----------
const int PIN_BOTAO = 2;
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5}; // a,b,c,d,e,f,g
const int PIN_TRIG = 7, PIN_ECHO = 8;
const int PIN_SERVO = 9, PIN_BUZZER = 10;
const int PIN_LED_VERM = 11, PIN_LED_VERDE = 12, PIN_LED_AZUL = 13;
const int PIN_LDR = A0, PIN_RELE = A2;

// Mapa de segmentos: bit0 = a ... bit6 = g
const byte DIGITOS[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};

Servo cabeca;

void mostrar(byte padrao) {
  for (int i = 0; i < 7; i++) {
    bool aceso = padrao & (1 << i);
    if (DISPLAY_ANODO_COMUM) aceso = !aceso;
    digitalWrite(PIN_SEG[i], aceso ? HIGH : LOW);
  }
}

void bip(int freq, int ms) {
  if (BUZZER_ATIVO) {
    digitalWrite(PIN_BUZZER, HIGH); delay(ms); digitalWrite(PIN_BUZZER, LOW);
  } else {
    tone(PIN_BUZZER, freq, ms); delay(ms);
  }
}

void rele(bool ligado) {
  digitalWrite(PIN_RELE, (ligado != RELE_ATIVO_BAIXO) ? HIGH : LOW);
}

float lerDistanciaCm() {
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 12000UL); // timeout ~2 m
  if (us == 0) return 200.0;                           // sem eco = "longe"
  float d = us * 0.0343 / 2.0;
  return d > 200.0 ? 200.0 : d;
}

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BOTAO, INPUT_PULLUP);
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  pinMode(PIN_TRIG, OUTPUT); pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_VERM, OUTPUT); pinMode(PIN_LED_VERDE, OUTPUT); pinMode(PIN_LED_AZUL, OUTPUT);
  pinMode(PIN_RELE, OUTPUT); rele(false);
  cabeca.attach(PIN_SERVO);

  Serial.println(F("# === TESTE DE HARDWARE ==="));

  Serial.println(F("# 1) LEDs: vermelho, verde, azul"));
  int leds[3] = {PIN_LED_VERM, PIN_LED_VERDE, PIN_LED_AZUL};
  for (int i = 0; i < 3; i++) { digitalWrite(leds[i], HIGH); delay(400); digitalWrite(leds[i], LOW); }

  Serial.println(F("# 2) Display: contando 0 a 9"));
  for (int d = 0; d < 10; d++) { mostrar(DIGITOS[d]); delay(300); }
  mostrar(0);

  Serial.println(F("# 3) Buzzer: tres notas"));
  bip(523, 200); bip(659, 200); bip(784, 300);

  Serial.println(F("# 4) Servo: 0 -> 180 -> 90 graus"));
  for (int a = 0; a <= 180; a += 5) { cabeca.write(a); delay(20); }
  for (int a = 180; a >= 90; a -= 5) { cabeca.write(a); delay(20); }

  Serial.println(F("# 5) Rele: liga 1 s (deve ouvir o 'clique')"));
  rele(true); delay(1000); rele(false);

  Serial.println(F("# 6) Agora em loop: distancia, LDR e botao. Abra o Serial Plotter!"));
}

void loop() {
  float d = lerDistanciaCm();
  int luz = analogRead(PIN_LDR);
  bool botao = digitalRead(PIN_BOTAO) == LOW;
  digitalWrite(PIN_LED_AZUL, botao);

  // Formato "nome:valor" funciona no Serial Plotter da IDE 2.x
  Serial.print(F("distancia_cm:")); Serial.print(d);
  Serial.print(F(",ldr:"));         Serial.print(luz / 5.0); // escala para caber no gráfico
  Serial.print(F(",botao:"));       Serial.println(botao ? 50 : 0);
  delay(60);
}
