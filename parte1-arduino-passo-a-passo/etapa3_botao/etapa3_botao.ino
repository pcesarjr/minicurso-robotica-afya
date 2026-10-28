/*
  MINICURSO DE ROBÓTICA — Parte 1, Etapa 3: o botão
  Montagem: botão atravessando o vão central; um pino ao D2 e o pino
            na diagonal oposta ao GND. Não precisa de resistor:
            usamos o pull-up interno do Arduino.
  Resultado esperado: cada aperto liga/desliga o LED verde,
            e o Serial Monitor (9600) mostra o estado.
*/
const int BOTAO = 2;
const int LED_VERDE = 12;

bool ledLigado = false;
int leituraAnterior = HIGH;          // solto = HIGH (pull-up)

void setup() {
  pinMode(BOTAO, INPUT_PULLUP);
  pinMode(LED_VERDE, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int leitura = digitalRead(BOTAO);

  // Borda de descida: estava solto (HIGH) e agora está apertado (LOW)
  if (leituraAnterior == HIGH && leitura == LOW) {
    ledLigado = !ledLigado;
    digitalWrite(LED_VERDE, ledLigado);
    Serial.println(ledLigado ? "LED ligado" : "LED desligado");
    delay(30);                       // debounce: ignora a trepidação do contato
  }
  leituraAnterior = leitura;
}

/* Desafios:
   1) Tire o delay(30) e aperte várias vezes. O que acontece? (trepidação)
   2) Conte quantas vezes o botão foi apertado e mostre no Serial Monitor.
*/
