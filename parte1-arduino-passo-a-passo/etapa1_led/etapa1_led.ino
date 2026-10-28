/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 1: o primeiro LED
  Montagem: LED vermelho com o anodo (perna longa) ligado ao D11;
            catodo com resistor de 560 Ω até o trilho GND.
  Resultado esperado: o LED pisca a cada meio segundo.
*/
const int LED_VERM = 11;

void setup() {
  pinMode(LED_VERM, OUTPUT);       // D11 passa a ser uma SAÍDA
}

void loop() {
  digitalWrite(LED_VERM, HIGH);    // 5 V no pino: acende
  delay(500);                      // espera 500 ms
  digitalWrite(LED_VERM, LOW);     // 0 V no pino: apaga
  delay(500);
}

/* Desafios:
   1) Pisque mais rápido. Até quantos ms o olho ainda percebe o pisca?
   2) Faça "SOS" em código Morse (curto = 200 ms, longo = 600 ms).
*/
