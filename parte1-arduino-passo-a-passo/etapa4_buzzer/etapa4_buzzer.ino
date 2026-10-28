/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 4: o buzzer
  Montagem: buzzer com o + no D10 e o − no GND.
  Resultado esperado: ao apertar o botão, toca a escala dó-ré-mi.
  Buzzer ATIVO (apita sozinho com 5 V)? Mude BUZZER_ATIVO para true:
  ele só faz bips, na mesma nota.
*/
const bool BUZZER_ATIVO = false;
const int BUZZER = 10;
const int BOTAO = 2;

//               dó   ré   mi   fá   sol  lá   si   dó
int notas[8] = {262, 294, 330, 349, 392, 440, 494, 523};   // em Hz

void tocar(int freq, int ms) {
  if (BUZZER_ATIVO) {
    digitalWrite(BUZZER, HIGH); delay(ms); digitalWrite(BUZZER, LOW);
  } else {
    tone(BUZZER, freq, ms);        // onda quadrada de 'freq' Hz por 'ms'
    delay(ms);
  }
  delay(20);                       // pequena pausa entre as notas
}

void setup() {
  pinMode(BUZZER, OUTPUT);
  pinMode(BOTAO, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(BOTAO) == LOW) {
    for (int i = 0; i < 8; i++) {
      tocar(notas[i], 150);
    }
  }
}

/* Desafios:
   1) Toque a escala de volta, do agudo para o grave.
   2) Faça uma sirene: alterne 900 Hz e 1500 Hz enquanto o botão estiver apertado.
*/
