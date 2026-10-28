/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 9: módulo relé (o "holofote")
  Montagem: módulo relé com VCC→5 V, GND→GND, IN→A2.
            Nada ligado nos bornes de carga (sem tensão de rede na bancada!).
  Resultado esperado: com o LDR coberto (escuro), o relé dá um "clique"
            e acende o LED do módulo. O botão também liga o relé enquanto
            estiver apertado.
  Se o relé ficar ligado ao contrário, mude RELE_ATIVO_BAIXO.
*/
const bool RELE_ATIVO_BAIXO = true;     // a maioria dos módulos liga com LOW
const int PIN_RELE = A2, LDR = A0, BOTAO = 2, LED_AZUL = 13;
int LIMIAR = 150;                       // o mesmo valor calibrado na etapa 5

void rele(bool ligado) {
  digitalWrite(PIN_RELE, (ligado != RELE_ATIVO_BAIXO) ? HIGH : LOW);
}

void setup() {
  pinMode(PIN_RELE, OUTPUT);
  rele(false);
  pinMode(BOTAO, INPUT_PULLUP);
  pinMode(LED_AZUL, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  bool escuro = analogRead(LDR) < LIMIAR;
  bool apertado = digitalRead(BOTAO) == LOW;
  bool ligar = escuro || apertado;

  rele(ligar);
  digitalWrite(LED_AZUL, ligar);
  Serial.println(ligar ? "holofote LIGADO" : "holofote desligado");
  delay(200);
}

/* Desafio: o relé "tremula" quando a luz está bem no limiar?
   Use dois limiares (liga abaixo de 140, desliga acima de 170): isso é histerese.
*/
