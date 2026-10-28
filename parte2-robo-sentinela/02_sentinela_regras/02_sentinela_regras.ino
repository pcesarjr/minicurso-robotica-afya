/*
  MINICURSO DE ROBÓTICA — Robô Sentinela
  Sketch 02: Sentinela por REGRAS (máquina de estados, sem delay no loop)

  Comportamento:
    PATRULHA -> a cabeça varre de 20° a 160° medindo distância.
    ATENCAO  -> algo a menos de LIMIAR_CM: para, olha para o alvo, LED vermelho, bip.
                Se o alvo chegar a menos de PERIGO_CM -> ALARME.
                Se o alvo sumir por TEMPO_SUMIU_MS -> volta a PATRULHA.
    ALARME   -> sirene + relé por 3 s, depois volta para ATENCAO.
    No escuro (LDR), o relé ("holofote") acende já na ATENCAO.

  Desafio do bloco: tente criar uma regra que diferencie "mão se aproximando",
  "mão se afastando" e "aceno". Vai perceber por que vamos usar Machine Learning.
*/
#include <Servo.h>

// ---------- Ajustes ----------
const bool DISPLAY_ANODO_COMUM = false;
const bool BUZZER_ATIVO        = false;
const bool RELE_ATIVO_BAIXO    = true;
const float LIMIAR_CM   = 40.0;   // distância que dispara a atenção
const float PERIGO_CM   = 12.0;   // distância que dispara o alarme
const int   LDR_ESCURO  = 150;    // abaixo disso consideramos escuro (calibre no sketch 01)
const unsigned long PASSO_MS       = 60;   // intervalo entre passos da varredura
const unsigned long TEMPO_SUMIU_MS = 3000;
const int ANG_MIN = 20, ANG_MAX = 160, ANG_PASSO = 4;

// ---------- Pinos ----------
const int PIN_SEG[7] = {3, 4, 5, 6, A3, A4, A5};
const int PIN_TRIG = 7, PIN_ECHO = 8, PIN_SERVO = 9, PIN_BUZZER = 10;
const int PIN_LED_VERM = 11, PIN_LED_VERDE = 12, PIN_LED_AZUL = 13;
const int PIN_LDR = A0, PIN_RELE = A2;

const byte SEG_P = 0x73, SEG_A = 0x77, SEG_ALARME = 0x49; // P, A, três barras

enum Estado { PATRULHA, ATENCAO, ALARME };
Estado estado = PATRULHA;

Servo cabeca;
int angulo = 90, direcao = +1;
unsigned long tUltimoPasso = 0, tUltimoAlvo = 0, tInicioAlarme = 0;
int contDeteccao = 0;

// ---------- Funções auxiliares ----------
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

void mudarPara(Estado novo) {
  estado = novo;
  switch (novo) {
    case PATRULHA: leds(false, true, false); mostrar(SEG_P); rele(false);
                   Serial.println(F("# -> PATRULHA")); break;
    case ATENCAO:  leds(true, false, false); mostrar(SEG_A); bip(1200, 80);
                   rele(estaEscuro()); tUltimoAlvo = millis();
                   Serial.println(F("# -> ATENCAO")); break;
    case ALARME:   leds(true, false, true); mostrar(SEG_ALARME); rele(true);
                   tInicioAlarme = millis();
                   Serial.println(F("# -> ALARME")); break;
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 7; i++) pinMode(PIN_SEG[i], OUTPUT);
  pinMode(PIN_TRIG, OUTPUT); pinMode(PIN_ECHO, INPUT); pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_LED_VERM, OUTPUT); pinMode(PIN_LED_VERDE, OUTPUT); pinMode(PIN_LED_AZUL, OUTPUT);
  pinMode(PIN_RELE, OUTPUT);
  cabeca.attach(PIN_SERVO); cabeca.write(angulo);
  mudarPara(PATRULHA);
}

void loop() {
  unsigned long agora = millis();
  if (agora - tUltimoPasso < PASSO_MS) return;   // ritmo fixo, sem travar o loop
  tUltimoPasso = agora;

  float d = lerDistanciaCm();
  Serial.print(F("angulo:")); Serial.print(angulo);
  Serial.print(F(",distancia:")); Serial.println(d);

  switch (estado) {
    case PATRULHA:
      angulo += direcao * ANG_PASSO;
      if (angulo >= ANG_MAX || angulo <= ANG_MIN) direcao = -direcao;
      angulo = constrain(angulo, ANG_MIN, ANG_MAX);
      cabeca.write(angulo);
      // exige 2 leituras seguidas para evitar falso alarme por ruído
      contDeteccao = (d < LIMIAR_CM) ? contDeteccao + 1 : 0;
      if (contDeteccao >= 2) { contDeteccao = 0; mudarPara(ATENCAO); }
      break;

    case ATENCAO:
      if (d < LIMIAR_CM) tUltimoAlvo = agora;
      if (d < PERIGO_CM) mudarPara(ALARME);
      else if (agora - tUltimoAlvo > TEMPO_SUMIU_MS) mudarPara(PATRULHA);
      break;

    case ALARME:
      if (BUZZER_ATIVO) digitalWrite(PIN_BUZZER, (agora / 200) % 2);
      else tone(PIN_BUZZER, ((agora / 250) % 2) ? 1500 : 900);
      if (agora - tInicioAlarme > 3000) {
        noTone(PIN_BUZZER); digitalWrite(PIN_BUZZER, LOW);
        mudarPara(ATENCAO);
      }
      break;
  }
}
