/*
  MINICURSO DE ROBÓTICA — Robô Sentinela
  Sketch 03: COLETA DE DADOS para Machine Learning

  Como usar:
   1. Abra o Serial Monitor (9600 baud, "Nova linha" ou "Sem final de linha").
   2. Digite o número da classe que vai gravar e tecle Enter:
        0 = PARADO     (mão parada a ~20 cm, ou nada na frente)
        1 = APROXIMAR  (mão vem de ~40 cm até ~10 cm em 1 segundo)
        2 = AFASTAR    (mão vai de ~10 cm até ~40 cm em 1 segundo)
        3 = ACENAR     (mão faz vai-e-vem rápido entre ~10 e ~30 cm)
      O display mostra a classe escolhida.
   3. Aperte o botão GRAVAR. Bip curto = prepare-se; bip agudo + LED azul = gravando (1 s).
   4. Cada gravação imprime UMA linha CSV. Grave ~20 por classe (varie velocidade, distância, quem faz).
   5. No final, copie TODO o texto do Serial Monitor e salve como dados_grupoX.csv.
      Linhas começando com '#' são comentários e são ignoradas no Colab.

  A janela tem 20 leituras a cada 50 ms (1 s). Dela tiramos 6 "features" (características).
  É isso que o modelo vai enxergar — não a mão, e sim estes 6 números.
*/

// ---------- Ajustes ----------
const bool DISPLAY_ANODO_COMUM = false;
const bool BUZZER_ATIVO        = false;

// ---------- Pinos ----------
const int PIN_BOTAO = 2;
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};
const int PIN_TRIG = 7, PIN_ECHO = 8, PIN_BUZZER = 10;
const int PIN_LED_VERM = 11, PIN_LED_VERDE = 12, PIN_LED_AZUL = 13;

const byte DIGITOS[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};

// ---------- Janela e features ----------
const int N_AMOSTRAS = 20;
const unsigned long PERIODO_MS = 50;
const int N_FEATURES = 6;
float janela[N_AMOSTRAS];

int classeAtual = 0;
int contPorClasse[4] = {0, 0, 0, 0};

void mostrar(byte padrao) {
  for (int i = 0; i < 7; i++) {
    bool aceso = padrao & (1 << i);
    if (DISPLAY_ANODO_COMUM) aceso = !aceso;
    digitalWrite(PIN_SEG[i], aceso ? HIGH : LOW);
  }
}
void bip(int freq, int ms) {
  if (BUZZER_ATIVO) { digitalWrite(PIN_BUZZER, HIGH); delay(ms); digitalWrite(PIN_BUZZER, LOW); }
  else { tone(PIN_BUZZER, freq, ms); delay(ms); }
}
float lerDistanciaCm() {
  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 12000UL);
  if (us == 0) return 200.0;
  float d = us * 0.0343 / 2.0;
  return d > 200.0 ? 200.0 : d;
}

// Grava N_AMOSTRAS leituras em ritmo fixo
void gravarJanela() {
  unsigned long t = millis();
  for (int i = 0; i < N_AMOSTRAS; i++) {
    while (millis() - t < PERIODO_MS) { }
    t += PERIODO_MS;
    float d = lerDistanciaCm();
    // leitura perdida (sem eco) no meio do gesto: repete a anterior (filtro simples)
    if (d >= 200.0 && i > 0 && janela[i - 1] < 200.0) d = janela[i - 1];
    janela[i] = d;
  }
}

// ===== EXTRAÇÃO DE FEATURES (idêntica no sketch 04!) =====
// f[0] media      f[1] desvio padrão   f[2] mínimo   f[3] máximo
// f[4] inclinação (cm/s, reta de mínimos quadrados)
// f[5] trocas de sentido (quantas vezes a mão inverte o movimento)
void calcularFeatures(const float *x, int n, float *f) {
  float soma = 0, mn = x[0], mx = x[0];
  for (int i = 0; i < n; i++) { soma += x[i]; if (x[i] < mn) mn = x[i]; if (x[i] > mx) mx = x[i]; }
  float media = soma / n;

  float var = 0;
  for (int i = 0; i < n; i++) var += (x[i] - media) * (x[i] - media);
  float desvio = sqrt(var / n);

  // inclinação: cov(t, x) / var(t), com t em amostras -> converte para cm/s
  float tMedio = (n - 1) / 2.0, num = 0, den = 0;
  for (int i = 0; i < n; i++) { num += (i - tMedio) * (x[i] - media); den += (i - tMedio) * (i - tMedio); }
  float inclinacao = (num / den) * (1000.0 / PERIODO_MS);

  // trocas de sentido, ignorando variações menores que 2 cm (ruído)
  int trocas = 0, sentidoAnterior = 0;
  for (int i = 1; i < n; i++) {
    float dx = x[i] - x[i - 1];
    int s = (dx > 2.0) ? 1 : (dx < -2.0 ? -1 : 0);
    if (s != 0) {
      if (sentidoAnterior != 0 && s != sentidoAnterior) trocas++;
      sentidoAnterior = s;
    }
  }

  f[0] = media; f[1] = desvio; f[2] = mn; f[3] = mx; f[4] = inclinacao; f[5] = trocas;
}

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BOTAO, INPUT_PULLUP);
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  pinMode(PIN_TRIG, OUTPUT); pinMode(PIN_ECHO, INPUT); pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_VERM, OUTPUT); pinMode(PIN_LED_VERDE, OUTPUT); pinMode(PIN_LED_AZUL, OUTPUT);
  mostrar(DIGITOS[classeAtual]);
  digitalWrite(PIN_LED_VERDE, HIGH);
  Serial.println(F("# Digite 0,1,2 ou 3 para escolher a classe; aperte o botao para gravar."));
  Serial.println(F("media,desvio,minimo,maximo,inclinacao,trocas,classe"));
}

void loop() {
  // troca de classe pelo teclado
  while (Serial.available()) {
    char c = Serial.read();
    if (c >= '0' && c <= '3') {
      classeAtual = c - '0';
      mostrar(DIGITOS[classeAtual]);
      Serial.print(F("# classe atual: ")); Serial.println(classeAtual);
    }
  }

  if (digitalRead(PIN_BOTAO) == LOW) {
    digitalWrite(PIN_LED_VERDE, LOW);
    bip(800, 80); delay(500);          // prepara...
    bip(1600, 60);                     // ...já!
    digitalWrite(PIN_LED_AZUL, HIGH);
    gravarJanela();
    digitalWrite(PIN_LED_AZUL, LOW);

    float f[N_FEATURES];
    calcularFeatures(janela, N_AMOSTRAS, f);
    for (int i = 0; i < N_FEATURES; i++) { Serial.print(f[i], 2); Serial.print(','); }
    Serial.println(classeAtual);

    contPorClasse[classeAtual]++;
    Serial.print(F("# amostras por classe: "));
    for (int k = 0; k < 4; k++) { Serial.print(contPorClasse[k]); Serial.print(k < 3 ? " / " : "\n"); }

    while (digitalRead(PIN_BOTAO) == LOW) { } // espera soltar o botão
    delay(200);
    digitalWrite(PIN_LED_VERDE, HIGH);
  }
}
