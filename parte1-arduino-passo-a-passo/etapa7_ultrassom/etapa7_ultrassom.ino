/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 7: sensor ultrassônico HC-SR04
  Montagem (fora da protoboard, com jumpers macho-fêmea):
            VCC→5 V, GND→GND, Trig→D7, Echo→D8.
  Resultado esperado: o Serial Monitor mostra a distância em cm;
            os LEDs indicam longe (verde), médio (azul) e perto (vermelho);
            o display mostra a distância em decímetros (0 a 9).
*/
const bool DISPLAY_ANODO_COMUM = false;
const int PIN_TRIG = 7, PIN_ECHO = 8;
const int LED_VERM = 11, LED_VERDE = 12, LED_AZUL = 13;
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};
const byte DIGITOS[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};

void mostrar(byte padrao) {
  for (int i = 0; i < 7; i++) {
    bool aceso = padrao & (1 << i);
    if (DISPLAY_ANODO_COMUM) aceso = !aceso;
    digitalWrite(PIN_SEG[i], aceso ? HIGH : LOW);
  }
}

float lerDistanciaCm() {
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);   // pulso de disparo
  digitalWrite(PIN_TRIG, LOW);
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 12000UL);   // tempo de ida e volta
  if (us == 0) return 200.0;                             // sem eco = longe
  return us * 0.0343 / 2.0;                              // som: 0,0343 cm/µs
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(LED_VERM, OUTPUT); pinMode(LED_VERDE, OUTPUT); pinMode(LED_AZUL, OUTPUT);
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float d = lerDistanciaCm();
  Serial.print("distancia_cm:");
  Serial.println(d);

  digitalWrite(LED_VERDE, d >= 40);
  digitalWrite(LED_AZUL,  d >= 15 && d < 40);
  digitalWrite(LED_VERM,  d < 15);

  int dm = (int)(d / 10);                  // decímetros
  mostrar(DIGITOS[dm > 9 ? 9 : dm]);
  delay(100);
}

/* Desafio: com a régua, coloque um caderno a 10, 20 e 30 cm.
   Quanto o sensor erra? O erro muda com a distância?
*/
