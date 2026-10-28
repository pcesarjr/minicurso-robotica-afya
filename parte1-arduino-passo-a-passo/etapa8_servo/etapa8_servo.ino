/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 8: servo motor = pescoço do robô
  Montagem: servo com marrom→GND, vermelho→5 V, laranja→D9.
            Capacitor de 100 µF entre os trilhos 5 V e GND (faixa − no GND).
            Cole o HC-SR04 no braço do servo: nasce a "cabeça" do robô.
  Resultado esperado: a cabeça varre de 20° a 160° e volta, como um radar.
            O Serial Monitor mostra "ângulo, distância"; o LED vermelho
            acende quando há algo a menos de 40 cm.
*/
#include <Servo.h>

const int PIN_SERVO = 9, PIN_TRIG = 7, PIN_ECHO = 8, LED_VERM = 11;
Servo cabeca;

float lerDistanciaCm() {
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 12000UL);
  if (us == 0) return 200.0;
  return us * 0.0343 / 2.0;
}

void medirEm(int angulo) {
  cabeca.write(angulo);
  delay(60);                                 // tempo para o servo chegar e o eco morrer
  float d = lerDistanciaCm();
  digitalWrite(LED_VERM, d < 40);
  Serial.print(angulo);
  Serial.print(", ");
  Serial.println(d);
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(LED_VERM, OUTPUT);
  cabeca.attach(PIN_SERVO);
  Serial.begin(9600);
  Serial.println("angulo, distancia_cm");
}

void loop() {
  for (int a = 20; a <= 160; a += 4) medirEm(a);
  for (int a = 160; a >= 20; a -= 4) medirEm(a);
}

/* Desafios:
   1) Encaixe o braço do servo para que 90° aponte para a frente.
   2) Copie as linhas do Serial Monitor e desenhe o "mapa" do radar numa planilha.
*/
