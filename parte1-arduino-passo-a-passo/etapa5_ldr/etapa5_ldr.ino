/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 5: o sensor de luz (LDR)
  Montagem: LDR com uma perna no 5 V e a outra numa coluna livre.
            Dessa coluna: um fio ao A0 e um resistor de 1 kΩ até o GND
            (divisor de tensão).
  Resultado esperado: o Serial Plotter mostra a luz; cobrindo o LDR,
            o valor cai e o LED azul acende.
*/
const int LDR = A0;
const int LED_AZUL = 13;
int LIMIAR = 150;                  // ajuste com o valor que você ler no escuro

void setup() {
  pinMode(LED_AZUL, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(LDR);       // 0 (0 V) a 1023 (5 V)
  Serial.print("luz:");
  Serial.print(luz);
  Serial.print(",limiar:");
  Serial.println(LIMIAR);

  digitalWrite(LED_AZUL, luz < LIMIAR ? HIGH : LOW);
  delay(100);
}

/* Desafios:
   1) Anote o valor no claro e com o LDR coberto. Escolha um LIMIAR no meio.
   2) Faça o LED piscar mais rápido quanto mais escuro estiver.
*/
