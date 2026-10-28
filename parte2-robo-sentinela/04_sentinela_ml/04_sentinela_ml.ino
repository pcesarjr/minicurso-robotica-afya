/*
  MINICURSO DE ROBÓTICA — Robô Sentinela
  Sketch 04: SENTINELA INTELIGENTE (Machine Learning embarcado)

  Antes de compilar: substitua o arquivo modelo.h desta pasta pelo modelo.h
  gerado no Colab com os dados do SEU grupo.

  Comportamento:
    PATRULHA -> varre 20°..160°. Alvo a menos de LIMIAR_CM -> ATENCAO.
    ATENCAO  -> cabeça parada olhando o alvo. A cada 1 s grava uma janela,
                calcula as 6 features e pergunta ao modelo qual gesto foi feito:
                  0 PARADO    -> continua vigiando (se não houver ninguém, volta a patrulhar)
                  1 APROXIMAR -> ALARME (sirene + relé)
                  2 AFASTAR   -> "tchau", volta a PATRULHA
                  3 ACENAR    -> AMIGO: a cabeça "cumprimenta" e toca melodia
    O display mostra o estado (P, A) e a classe reconhecida (0 a 3).
*/
#include <Servo.h>
#include "modelo.h"   // contém: int classificar(const float *f)

// ---------- Ajustes ----------
const bool DISPLAY_ANODO_COMUM = false;
const bool BUZZER_ATIVO        = false;
const bool RELE_ATIVO_BAIXO    = true;
const float LIMIAR_CM  = 40.0;
const float VAZIO_CM   = 60.0;   // média da janela acima disso = ninguém na frente
const int   LDR_ESCURO = 150;
const int ANG_MIN = 20, ANG_MAX = 160, ANG_PASSO = 4;
const unsigned long PASSO_PATRULHA_MS = 60;

// ---------- Pinos ----------
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};
const int PIN_TRIG = 7, PIN_ECHO = 8, PIN_SERVO = 9, PIN_BUZZER = 10;
const int PIN_LED_VERM = 11, PIN_LED_VERDE = 12, PIN_LED_AZUL = 13;
const int PIN_LDR = A0, PIN_RELE = A2;

const byte DIGITOS[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};
const byte SEG_P = 0x73, SEG_A = 0x77;

// ---------- Janela (mesmos valores do sketch 03!) ----------
const int N_AMOSTRAS = 20;
const unsigned long PERIODO_MS = 50;
const int N_FEATURES = 6;
float janela[N_AMOSTRAS];
int nJanela = 0;

enum Estado { PATRULHA, ATENCAO };
Estado estado = PATRULHA;
Servo cabeca;
int angulo = 90, direcao = +1, contDeteccao = 0, janelasVazias = 0;
unsigned long tUltimo = 0;

const char *NOMES[4] = {"PARADO", "APROXIMAR", "AFASTAR", "ACENAR"};

// ---------- Auxiliares ----------
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
void rele(bool ligado) { digitalWrite(PIN_RELE, (ligado != RELE_ATIVO_BAIXO) ? HIGH : LOW); }
void leds(bool verm, bool verde, bool azul) {
  digitalWrite(PIN_LED_VERM, verm); digitalWrite(PIN_LED_VERDE, verde); digitalWrite(PIN_LED_AZUL, azul);
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

bool estaEscuro() { return analogRead(PIN_LDR) < LDR_ESCURO; }

// ===== EXTRAÇÃO DE FEATURES (cópia exata do sketch 03) =====
void calcularFeatures(const float *x, int n, float *f) {
  float soma = 0, mn = x[0], mx = x[0];
  for (int i = 0; i < n; i++) { soma += x[i]; if (x[i] < mn) mn = x[i]; if (x[i] > mx) mx = x[i]; }
  float media = soma / n;
  float var = 0;
  for (int i = 0; i < n; i++) var += (x[i] - media) * (x[i] - media);
  float desvio = sqrt(var / n);
  float tMedio = (n - 1) / 2.0, num = 0, den = 0;
  for (int i = 0; i < n; i++) { num += (i - tMedio) * (x[i] - media); den += (i - tMedio) * (i - tMedio); }
  float inclinacao = (num / den) * (1000.0 / PERIODO_MS);
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

// ---------- Reações (animações curtas; aqui o delay é aceitável) ----------
void reagirAlarme() {
  leds(true, false, true); rele(true);
  for (int i = 0; i < 6; i++) { bip(1500, 220); bip(900, 220); }
  rele(estaEscuro()); leds(true, false, false);
}
void reagirAmigo() {
  leds(false, true, false);
  bip(523, 120); bip(659, 120); bip(784, 120); bip(1047, 250);
  for (int i = 0; i < 3; i++) {             // "balança a cabeça"
    cabeca.write(constrain(angulo + 20, 0, 180)); delay(200);
    cabeca.write(constrain(angulo - 20, 0, 180)); delay(200);
  }
  cabeca.write(angulo);
}
void reagirTchau() { bip(900, 120); bip(600, 200); }

void irPara(Estado novo) {
  estado = novo;
  if (novo == PATRULHA) {
    leds(false, true, false); mostrar(SEG_P); rele(false); contDeteccao = 0;
    Serial.println(F("# -> PATRULHA"));
  } else {
    leds(true, false, false); mostrar(SEG_A); rele(estaEscuro());
    bip(1200, 80); delay(600);                 // dá tempo da pessoa posicionar a mão
    nJanela = 0; janelasVazias = 0;
    Serial.println(F("# -> ATENCAO (faca um gesto)"));
  }
  tUltimo = millis();
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  pinMode(PIN_TRIG, OUTPUT); pinMode(PIN_ECHO, INPUT); pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_VERM, OUTPUT); pinMode(PIN_LED_VERDE, OUTPUT); pinMode(PIN_LED_AZUL, OUTPUT);
  pinMode(PIN_RELE, OUTPUT);
  cabeca.attach(PIN_SERVO); cabeca.write(angulo);
  irPara(PATRULHA);
}

void loop() {
  unsigned long agora = millis();

  if (estado == PATRULHA) {
    if (agora - tUltimo < PASSO_PATRULHA_MS) return;
    tUltimo = agora;
    angulo += direcao * ANG_PASSO;
    if (angulo >= ANG_MAX || angulo <= ANG_MIN) direcao = -direcao;
    angulo = constrain(angulo, ANG_MIN, ANG_MAX);
    cabeca.write(angulo);
    float d = lerDistanciaCm();
    contDeteccao = (d < LIMIAR_CM) ? contDeteccao + 1 : 0;
    if (contDeteccao >= 2) irPara(ATENCAO);
    return;
  }

  // ----- ATENCAO: amostra a cada PERIODO_MS -----
  if (agora - tUltimo < PERIODO_MS) return;
  tUltimo += PERIODO_MS;
  digitalWrite(PIN_LED_AZUL, HIGH);           // azul = "ouvindo"
  float d = lerDistanciaCm();
  // mesmo filtro do sketch 03: leitura perdida no meio do gesto repete a anterior
  if (d >= 200.0 && nJanela > 0 && janela[nJanela - 1] < 200.0) d = janela[nJanela - 1];
  janela[nJanela++] = d;
  if (nJanela < N_AMOSTRAS) return;

  // Janela completa -> features -> modelo
  digitalWrite(PIN_LED_AZUL, LOW);
  nJanela = 0;
  float f[N_FEATURES];
  calcularFeatures(janela, N_AMOSTRAS, f);
  int classe = classificar(f);
  mostrar(DIGITOS[classe]);

  Serial.print(F("# features: "));
  for (int i = 0; i < N_FEATURES; i++) { Serial.print(f[i], 1); Serial.print(' '); }
  Serial.print(F("-> classe ")); Serial.print(classe);
  Serial.print(F(" (")); Serial.print(NOMES[classe]); Serial.println(')');

  if (classe == 1) { reagirAlarme(); mostrar(SEG_A); }
  else if (classe == 2) { reagirTchau(); irPara(PATRULHA); return; }
  else if (classe == 3) { reagirAmigo(); irPara(PATRULHA); return; }
  else {                                        // PARADO: há alguém ou não?
    janelasVazias = (f[0] > VAZIO_CM) ? janelasVazias + 1 : 0;
    if (janelasVazias >= 3) { irPara(PATRULHA); return; }
  }
  tUltimo = millis();                           // recomeça a janela após a reação
}
