/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 6b: contador (botão + display + buzzer)
  Montagem: nada novo — junta o que já está montado.
  Resultado esperado: cada aperto soma 1 no display (0 a 9, depois volta a 0)
            com um bip; no 9, o LED vermelho acende.
*/
const bool DISPLAY_ANODO_COMUM = false;
const bool BUZZER_ATIVO = false;
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};
const int BOTAO = 2, BUZZER = 10, LED_VERM = 11;
const byte DIGITOS[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};

int contagem = 0;
int leituraAnterior = HIGH;

void mostrar(byte padrao) {
  for (int i = 0; i < 7; i++) {
    bool aceso = padrao & (1 << i);
    if (DISPLAY_ANODO_COMUM) aceso = !aceso;
    digitalWrite(PIN_SEG[i], aceso ? HIGH : LOW);
  }
}

void bip() {
  if (BUZZER_ATIVO) { digitalWrite(BUZZER, HIGH); delay(60); digitalWrite(BUZZER, LOW); }
  else { tone(BUZZER, 1200, 60); }
}

void setup() {
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  pinMode(BOTAO, INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);
  pinMode(LED_VERM, OUTPUT);
  mostrar(DIGITOS[0]);
}

void loop() {
  int leitura = digitalRead(BOTAO);
  if (leituraAnterior == HIGH && leitura == LOW) {
    contagem = (contagem + 1) % 10;              // 9 + 1 volta para 0
    mostrar(DIGITOS[contagem]);
    digitalWrite(LED_VERM, contagem == 9);
    bip();
    delay(30);                                   // debounce
  }
  leituraAnterior = leitura;
}

/* Desafio: segurar o botão por 1 s zera a contagem (use millis()).
*/
