/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 2: três LEDs em sequência
  Montagem: LED verde no D12 e azul no D13, iguais ao vermelho
            (anodo no pino; catodo com 560 Ω até o GND).
  Resultado esperado: vermelho → verde → azul, repetindo.
*/
const int LEDS[3] = {11, 12, 13};   // vermelho, verde, azul

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(LEDS[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(LEDS[i], HIGH);
    delay(300);
    digitalWrite(LEDS[i], LOW);
  }
}

/* Desafios:
   1) Faça a luz ir e voltar (vermelho → verde → azul → verde → vermelho).
   2) Semáforo: verde 3 s, azul (no papel do amarelo) 1 s, vermelho 3 s.
*/
