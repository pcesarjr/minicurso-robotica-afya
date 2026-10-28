/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 6: display de 7 segmentos
  Montagem: display atravessando o vão central (colunas 12 a 16).
            Os dois pinos comuns (C) no GND. Cada segmento passa por um
            resistor de 620 Ω até o Arduino:
            a→D3  b→D4  c→D5  d→D6  e→A3  f→A4  g→A5
  Resultado esperado: o display conta de 0 a 9.
  Se aparecer "em negativo", o display é de ÂNODO comum: ligue os
  pinos C no 5 V e mude DISPLAY_ANODO_COMUM para true.
*/
const bool DISPLAY_ANODO_COMUM = false;
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};   // a, b, c, d, e, f, g

// Cada dígito é um byte: bit 0 = a ... bit 6 = g (1 = aceso)
const byte DIGITOS[10] = {
  0x3F, // 0
  0x06, // 1
  0x5B, // 2
  0x4F, // 3
  0x66, // 4
  0x6D, // 5
  0x7D, // 6
  0x07, // 7
  0x7F, // 8
  0x6F  // 9
};

void mostrar(byte padrao) {
  for (int i = 0; i < 7; i++) {
    bool aceso = padrao & (1 << i);              // o bit i está ligado?
    if (DISPLAY_ANODO_COMUM) aceso = !aceso;
    digitalWrite(PIN_SEG[i], aceso ? HIGH : LOW);
  }
}

void setup() {
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
}

void loop() {
  for (int n = 0; n <= 9; n++) {
    mostrar(DIGITOS[n]);
    delay(600);
  }
}

/* Desafios:
   1) Conte de 9 até 0.
   2) Mostre a palavra CAFE, uma letra por vez: C=0x39, A=0x77, F=0x71, E=0x79.
*/
