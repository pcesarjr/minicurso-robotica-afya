const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, ImageRun,
  WidthType, ShadingType, BorderStyle, AlignmentType, LevelFormat, PageBreak, VerticalAlign,
  Header, Footer, PageNumber,
} = require("docx");
const fs = require("fs");

const NAVY = "1F3864", GOLD = "B58B2C", LIGHT = "F2F2F2", FONT = "Calibri", MONO = "Consolas";
const W = 9638; // largura útil A4 com margens de 2 cm

// ---------- helpers ----------
const run = (text, o = {}) => new TextRun({ text, size: 21, font: FONT, ...o });
function rich(parts) { // parts: string ou [texto, {bold...}]
  return parts.map((p) => (typeof p === "string" ? run(p) : run(p[0], p[1])));
}
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 },
    border: { bottom: { color: GOLD, space: 4, style: BorderStyle.SINGLE, size: 8 } },
    children: [new TextRun({ text, bold: true, color: NAVY, size: 30, font: FONT })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 100 },
    children: [new TextRun({ text, bold: true, color: NAVY, size: 24, font: FONT })],
  });
}
function h3(text) {
  return new Paragraph({ spacing: { before: 180, after: 80 }, keepNext: true,
    children: [new TextRun({ text, bold: true, color: GOLD, size: 21, font: FONT })] });
}
function p(content, o = {}) {
  return new Paragraph({ spacing: { after: 120 }, alignment: o.align,
    children: Array.isArray(content) ? rich(content) : [run(content, o)] });
}
function bullet(content, level = 0) {
  return new Paragraph({ numbering: { reference: "bullets", level }, spacing: { after: 60 },
    children: Array.isArray(content) ? rich(content) : [run(content)] });
}
function num(content, ref = "passos") {
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 60 },
    children: Array.isArray(content) ? rich(content) : [run(content)] });
}
const noBorders = {
  insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
};
function codeBlock(lines) {
  const b = { style: BorderStyle.SINGLE, size: 2, color: "444444" };
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    borders: { top: b, bottom: b, left: b, right: b, ...noBorders },
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: "1E1E1E" },
      margins: { top: 120, bottom: 120, left: 180, right: 180 },
      children: lines.map((l) => new Paragraph({ spacing: { after: 10 },
        children: [new TextRun({ text: l.length ? l : " ", font: MONO, size: 17, color: "D4D4D4" })] })),
    })] })],
  });
}
function box(title, content, fill = "FFF4DE", bar = GOLD) {
  const items = Array.isArray(content) ? content : [content];
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: fill }, bottom: { style: BorderStyle.SINGLE, size: 2, color: fill },
      left: { style: BorderStyle.SINGLE, size: 24, color: bar }, right: { style: BorderStyle.SINGLE, size: 2, color: fill },
      ...noBorders,
    },
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill },
      margins: { top: 110, bottom: 110, left: 220, right: 220 },
      children: [
        new Paragraph({ spacing: { after: 50 }, children: [run(title, { bold: true, size: 20, color: NAVY })] }),
        ...items.map((t) => new Paragraph({ spacing: { after: 40 },
          children: Array.isArray(t) ? rich(t).map((r) => r) : [run(t, { size: 20 })] })),
      ],
    })] })],
  });
}
const dica = (t, c) => box(t, c);
const alerta = (t, c) => box(t, c, "FDECEA", "C0392B");
const conceito = (t, c) => box(t, c, "EAF1FB", NAVY);
const spacer = (h = 100) => new Paragraph({ spacing: { after: h }, children: [] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

function table(header, rows, widths) {
  const cell = (text, isH, w, shade) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: isH ? { type: ShadingType.CLEAR, fill: NAVY } : shade ? { type: ShadingType.CLEAR, fill: LIGHT } : undefined,
    verticalAlign: VerticalAlign.CENTER, margins: { top: 80, bottom: 80, left: 110, right: 110 },
    children: String(text).split("\n").map((t) => new Paragraph({
      children: [new TextRun({ text: t, bold: isH, color: isH ? "FFFFFF" : "000000", size: 19, font: FONT })] })),
  });
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, true, widths[i])) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, false, widths[i], ri % 2 === 1)) })),
    ],
  });
}
function image(file, widthPx) {
  const data = fs.readFileSync(file);
  const w = data.readUInt32BE(16), h = data.readUInt32BE(20);
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 },
    children: [new ImageRun({ type: "png", data, transformation: { width: widthPx, height: Math.round(widthPx * h / w) } })] });
}
const caption = (t) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
  children: [run(t, { italics: true, size: 18, color: "555555" })] });

// ---------- conteúdo ----------
const C = [];

// CAPA
C.push(
  new Paragraph({ spacing: { before: 1500 }, children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "MINICURSO DE ROBÓTICA", bold: true, size: 52, color: NAVY, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120 }, children: [new TextRun({ text: "Robô Sentinela com Machine Learning embarcado", size: 32, color: GOLD, font: FONT, italics: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120 }, children: [new TextRun({ text: "Arduino Uno · HC-SR04 · servo · árvore de decisão treinada em Python e executada em C", size: 21, color: "555555", font: FONT })] }),
  image("img_pipeline.png", 600),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 300 }, children: [run("Carga horária: 4 horas  |  Nível: intermediário  |  Formato: prático, em grupos")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [run("Público: primeiros períodos de Engenharia de Computação")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60 }, children: [run("4 grupos (kit + servo cada) + kit do professor para demonstração")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 700 }, children: [run("Prof. Paulo César da Silva Junior", { bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [run("Roteiro do Professor + Apostila do Aluno", { color: "555555", size: 19 })] }),
  pageBreak(),
);

// 1. VISÃO GERAL
C.push(h1("1. O que vamos construir"));
C.push(p("Um robô sentinela: uma \"cabeça\" com sensor ultrassônico montada sobre um servo motor, que patrulha o ambiente, percebe quando alguém se aproxima e reconhece gestos feitos com a mão. O reconhecimento não é feito com regras escritas à mão — é feito por um modelo de Machine Learning que os próprios alunos treinam com dados gravados no seu robô e depois embarcam no Arduino."));
C.push(table(["Gesto", "Classe", "Reação do robô"], [
  ["Mão parada / ninguém", "0 PARADO", "Continua vigiando; sem ninguém por 3 s, volta a patrulhar"],
  ["Mão se aproximando", "1 APROXIMAR", "ALARME: sirene + relé (\"holofote\")"],
  ["Mão se afastando", "2 AFASTAR", "\"Tchau\": bip descendente, volta a patrulhar"],
  ["Aceno (vai-e-vem)", "3 ACENAR", "AMIGO: cabeça balança + melodia"],
], [2900, 1900, 4838]));
C.push(spacer());
C.push(h2("Por que este curso é \"intermediário\""));
C.push(bullet([["Arquitetura de robô: ", { bold: true }], "percepção → decisão → ação, organizada como máquina de estados."]));
C.push(bullet([["Programação de tempo real simples: ", { bold: true }], "loop sem delay() usando millis(), amostragem em ritmo fixo."]));
C.push(bullet([["Pipeline completo de ML: ", { bold: true }], "coleta e rotulagem de dados, extração de features, treino/teste, matriz de confusão, overfitting e generalização."]));
C.push(bullet([["ML embarcado (TinyML): ", { bold: true }], "o modelo treinado em Python é convertido automaticamente em código C e roda em um microcontrolador de 2 KB de RAM."]));
C.push(spacer());
C.push(h2("Objetivos de aprendizagem"));
C.push(p("Ao final, o aluno deve ser capaz de:"));
C.push(bullet("Montar e testar um sistema com sensores e atuadores, identificando falhas de montagem."));
C.push(bullet("Implementar uma máquina de estados não bloqueante no Arduino."));
C.push(bullet("Explicar a diferença entre programar regras e aprender regras a partir de dados."));
C.push(bullet("Coletar um dataset rotulado, treinar e avaliar um classificador, e reconhecer overfitting."));
C.push(bullet("Integrar um modelo treinado ao firmware e validar o comportamento no robô real."));

// 2. ORGANIZAÇÃO E MATERIAIS
C.push(pageBreak());
C.push(h1("2. Organização e materiais"));
C.push(h2("Turma"));
C.push(bullet("4 grupos de 3 a 5 alunos, cada um com 1 kit + 1 servo. O 5º kit fica com o professor, já montado e com o robô final funcionando, para a demonstração de abertura e para substituir peças."));
C.push(bullet("Cada grupo precisa de 1 computador com a Arduino IDE. Para o treino do modelo, ao menos 1 computador por grupo com navegador e conta Google (Google Colab). Plano B: o professor treina no próprio computador com os arquivos de dados dos grupos."));
C.push(h2("Por grupo"));
C.push(table(["Item", "Qtd.", "Uso no robô"], [
  ["Placa UNO R3 + cabo USB (kit)", "1", "Cérebro"],
  ["Protoboard 400 pontos (kit)", "1", "Display, LEDs, resistores"],
  ["Sensor ultrassônico HC-SR04 (kit)", "1", "\"Olho\" — mede distância"],
  ["Micro servo SG90", "1", "\"Pescoço\" — gira a cabeça"],
  ["Display 7 segmentos 1 dígito (kit)", "1", "Mostra estado (P, A) e classe (0–3)"],
  ["LEDs vermelho, verde e azul (kit)", "1 de cada", "Alerta, patrulha, \"ouvindo\""],
  ["Buzzer 5V (kit)", "1", "Bips, sirene, melodia"],
  ["Módulo relé 1 canal (kit)", "1", "\"Holofote\" / sirene externa"],
  ["Push button (kit)", "1", "Botão GRAVAR na coleta de dados"],
  ["Sensor LDR (kit)", "1", "Detecta escuro → liga o relé"],
  ["Resistores 620 Ω (kit)", "7", "Segmentos do display"],
  ["Resistores 560 Ω (kit)", "3", "LEDs"],
  ["Resistor 1 kΩ (kit)", "1", "Divisor de tensão do LDR"],
  ["Capacitor eletrolítico 100 µF (kit)", "1", "Estabiliza a alimentação do servo"],
  ["Jumpers macho-macho (kit)", "~25", "Ligações na protoboard"],
  ["Jumpers macho-fêmea", "4", "HC-SR04 na cabeça (comprar à parte)"],
  ["Fita dupla face / abraçadeira / papelão", "—", "Fixar o HC-SR04 no braço do servo e o servo na mesa"],
], [4300, 1300, 4038]));
C.push(spacer());
C.push(alerta("Atenção: itens que o kit não traz", [
  "1) Jumpers macho-fêmea: o HC-SR04 tem pinos machos e vai ficar em cima do servo, longe da protoboard. Os jumpers do kit são só macho-macho. Compre 4 macho-fêmea por grupo (são baratos).",
  "2) Servo SG90: o curso conta com os 4 servos já disponíveis. O conector fêmea do servo aceita os jumpers macho-macho do kit.",
]));

// 3. PREPARAÇÃO
C.push(h2("Checklist do professor (antes da aula)"));
C.push(bullet("Instalar a Arduino IDE (2.x) em todos os computadores e testar o upload (driver CH340 para placas compatíveis)."));
C.push(bullet("Rodar o sketch 01 em cada kit. Anotar: o display é cátodo ou ânodo comum? O buzzer é ativo ou passivo? O relé liga com LOW ou HIGH? (veja a seção 3)."));
C.push(bullet("Montar a cabeça de cada robô: HC-SR04 colado no braço (horn) do servo com fita dupla face; servo preso a uma base (caixinha, papelão grosso) para não sair andando."));
C.push(bullet("Deixar o kit do professor montado com o sketch 04 e um modelo treinado com os seus próprios gestos (faça a coleta do sketch 03 antes)."));
C.push(bullet("Distribuir a pasta de códigos (Codigos_Robo_Sentinela.zip) e abrir o notebook no Colab uma vez para conferir que roda (use dados_exemplo_simulado.csv)."));

// 4. HARDWARE
C.push(h1("3. Montagem: pinagem completa"));
C.push(p("A mesma pinagem vale para os 4 sketches — a montagem é feita uma única vez, na Parte 1."));
C.push(table(["Componente", "Pino Arduino", "Ligação"], [
  ["Botão GRAVAR", "D2", "Outro terminal no GND (usa pull-up interno)"],
  ["Display seg. a, b, c, d", "D3, D4, D5, D6", "Cada um via resistor 620 Ω"],
  ["Display seg. e, f, g", "A3, A4, A5", "Pinos analógicos usados como digitais; via 620 Ω"],
  ["Display pino comum", "GND ou 5V", "GND = cátodo comum; 5V = ânodo comum"],
  ["HC-SR04 TRIG / ECHO", "D7 / D8", "VCC no 5V, GND no GND"],
  ["Servo (fio laranja/amarelo)", "D9", "Vermelho no 5V, marrom no GND"],
  ["Capacitor 100 µF", "—", "Entre 5V (+) e GND (−), perto do servo"],
  ["Buzzer", "D10", "Negativo no GND"],
  ["LED vermelho / verde / azul", "D11 / D12 / D13", "Anodo no pino; catodo via 560 Ω ao GND"],
  ["LDR", "A0", "LDR entre 5V e A0; resistor 1 kΩ entre A0 e GND"],
  ["Módulo relé (IN)", "A2", "VCC no 5V, GND no GND"],
], [2900, 2200, 4538]));
C.push(pageBreak());
C.push(h2("Diagrama de montagem"));
C.push(image("img_montagem.png", 640));
C.push(caption("Figura — Montagem na protoboard de 400 pontos. Cada etiqueta (D3, A5…) indica o pino do Arduino de destino daquele fio."));
C.push(spacer());
C.push(conceito("Por que estes pinos? (vale explicar em sala)", [
  "A biblioteca Servo usa o Timer1 do ATmega328P — isso desliga o PWM dos pinos 9 e 10. A função tone() usa o Timer2 — afeta o PWM dos pinos 3 e 11. Como nada no robô usa analogWrite(), podemos colocar servo e buzzer nesses pinos sem conflito.",
  "O Uno tem 14 pinos digitais, mas D0/D1 são da serial (USB). Faltaram pinos para o display, então A3–A5 entram como saídas digitais comuns — todo pino analógico do Uno também funciona como digital.",
]));
C.push(spacer());
C.push(h3("Ajustes no início de cada sketch"));
C.push(codeBlock([
  "const bool DISPLAY_ANODO_COMUM = false; // true se o comum do display vai no 5V",
  "const bool BUZZER_ATIVO        = false; // true se o buzzer apita só com 5V",
  "const bool RELE_ATIVO_BAIXO    = true;  // a maioria dos módulos relé liga com LOW",
]));
C.push(spacer());
C.push(dica("Dicas de montagem na protoboard de 400 pontos", [
  "Display no centro da protoboard, com os 7 resistores saindo dele. LEDs na ponta. HC-SR04, servo e relé ficam fora da protoboard, ligados por jumpers.",
  "Se o Arduino reiniciar quando o servo se mexe, é queda de tensão no USB: confira o capacitor de 100 µF (polaridade!) e use uma porta USB do próprio computador, não de hub.",
]));

// 5. CRONOGRAMA
C.push(pageBreak());
C.push(h1("4. Cronograma (4 h)"));
C.push(table(["Horário", "Bloco", "Atividade", "Sketch"], [
  ["0:00–1:40", "Parte 1", "Arduino passo a passo: montar e testar cada componente", "etapas 1–9 + 01"],
  ["1:40–1:50", "—", "Intervalo", "—"],
  ["1:50–2:20", "Bloco 2", "Comportamento por regras: máquina de estados com millis()", "02"],
  ["2:20–3:15", "Bloco 3", "Machine Learning: coleta de dados, treino no Colab, avaliação", "03 + Colab"],
  ["3:15–3:50", "Bloco 4", "Integração do modelo no robô, testes e ajustes", "04"],
  ["3:50–4:00", "Encerramento", "Teste cruzado entre grupos", "04"],
], [1400, 1500, 5138, 1600]));
C.push(spacer());
C.push(image("img_estados.png", 600));
C.push(caption("Figura 1 — Máquina de estados do robô final (sketch 04)."));

// PARTE 1
C.push(pageBreak());
C.push(h1("5. Parte 1 — Arduino passo a passo (1h40)"));
C.push(p("A Parte 1 tem apresentação própria (\"Minicurso Parte 1 — Arduino passo a passo\") e funciona como o Bloco 1: em vez de montar tudo de uma vez, cada componente é montado direto no seu lugar definitivo e testado com um código curto antes do próximo. Ao final, a protoboard está igual ao diagrama da seção 3."));
C.push(table(["Etapa", "Componente", "Código", "Tempo"], [
  ["—", "Abertura, Arduino, IDE, protoboard, kit, resistores", "—", "15 min"],
  ["0", "Energia nos trilhos (5 V e GND)", "—", "3 min"],
  ["1", "LED vermelho (D11)", "etapa1_led", "8 min"],
  ["2", "LEDs verde e azul (D12, D13)", "etapa2_leds", "6 min"],
  ["3", "Botão (D2, pull-up interno)", "etapa3_botao", "8 min"],
  ["4", "Buzzer (D10)", "etapa4_buzzer", "6 min"],
  ["5", "LDR + 1 kΩ (A0) — calibrar o limiar", "etapa5_ldr", "8 min"],
  ["6", "Display 7 segmentos + contador", "etapa6_display, etapa6b_contador", "20 min"],
  ["7", "HC-SR04 (D7, D8)", "etapa7_ultrassom", "8 min"],
  ["8", "Servo (D9) + capacitor 100 µF", "etapa8_servo", "10 min"],
  ["9", "Relé (A2)", "etapa9_rele", "5 min"],
  ["✓", "Teste geral do robô montado", "01_teste_hardware", "5 min"],
], [900, 4300, 2938, 1500]));
C.push(spacer());
C.push(box("✔ Checkpoint da Parte 1", "Todos os componentes funcionaram no 01_teste_hardware e o grupo anotou: tipo de display, tipo de buzzer, lógica do relé e valor do LDR no escuro.", "E8F5E9", "2E7D32"));

// BLOCO 2
C.push(pageBreak());
C.push(h1("6. Bloco 2 — Comportamento por regras (30 min)"));
C.push(h2("Objetivo"));
C.push(p("Dar comportamento ao robô com uma máquina de estados e mostrar, na prática, o limite de regras escritas à mão."));
C.push(h2("Roteiro"));
C.push(num("(8 min) Conceito: máquina de estados (PATRULHA, ATENCAO, ALARME) e loop não bloqueante com millis().", "b2"));
C.push(num("(7 min) Upload do sketch 02. Observar a patrulha, a detecção (alvo < 40 cm) e o alarme (alvo < 12 cm). No escuro, o relé acende na atenção.", "b2"));
C.push(num("(7 min) Ajustes: mudar LIMIAR_CM, PERIGO_CM, velocidade da varredura (PASSO_MS, ANG_PASSO). Discutir por que exigimos 2 leituras seguidas para disparar.", "b2"));
C.push(num("(8 min) Desafio: escrever uma regra que diferencie APROXIMAR, AFASTAR e ACENAR. Deixe tentar — a maioria vai perceber que os limiares dependem da pessoa, da velocidade e da distância.", "b2"));
C.push(h3("Conceito-chave: o padrão de loop sem delay()"));
C.push(codeBlock([
  "void loop() {",
  "  unsigned long agora = millis();",
  "  if (agora - tUltimoPasso < PASSO_MS) return;  // ainda não é hora",
  "  tUltimoPasso = agora;",
  "",
  "  float d = lerDistanciaCm();",
  "  switch (estado) {",
  "    case PATRULHA: /* move a cabeça, procura alvo */  break;",
  "    case ATENCAO:  /* vigia, decide alarme/voltar */  break;",
  "    case ALARME:   /* sirene por 3 s */               break;",
  "  }",
  "}",
]));
C.push(spacer());
C.push(conceito("Ponte para o Bloco 3", "Em vez de nós inventarmos os limiares (\"se a inclinação for menor que X e o desvio maior que Y...\"), vamos mostrar exemplos ao computador e deixar um algoritmo encontrar as regras. Isso é aprendizado supervisionado."));

// BLOCO 3
C.push(pageBreak());
C.push(h1("7. Bloco 3 — Machine Learning (55 min)"));
C.push(h2("Objetivo"));
C.push(p("Percorrer o ciclo completo de um projeto de ML: dados → features → treino → avaliação → exportação."));
C.push(h2("7.1 Conceitos (15 min)"));
C.push(bullet([["Dataset rotulado: ", { bold: true }], "cada exemplo é um gesto gravado + a resposta certa (a classe)."]));
C.push(bullet([["Janela: ", { bold: true }], "20 leituras de distância, uma a cada 50 ms (1 segundo de movimento)."]));
C.push(bullet([["Features: ", { bold: true }], "20 números crus são difíceis de comparar; resumimos a janela em 6 características com significado físico."]));
C.push(bullet([["Treino × teste: ", { bold: true }], "o modelo aprende com 75% dos dados e é avaliado nos 25% que nunca viu."]));
C.push(bullet([["Árvore de decisão: ", { bold: true }], "uma sequência de perguntas do tipo \"inclinação ≤ −19?\". Vira if/else em C — cabe nos 2 KB de RAM do Uno."]));
C.push(spacer());
C.push(table(["Feature", "O que mede", "Ajuda a reconhecer"], [
  ["media", "Distância média na janela (cm)", "Se há alguém perto ou não"],
  ["desvio", "Quanto a distância variou (desvio padrão)", "Mão parada × mão em movimento"],
  ["minimo / maximo", "Menor e maior distância", "Alcance do gesto"],
  ["inclinacao", "Tendência da reta (cm/s): negativa = aproximando", "APROXIMAR × AFASTAR"],
  ["trocas", "Quantas vezes a mão inverteu o sentido", "ACENAR (vai-e-vem)"],
], [1900, 4300, 3438]));
C.push(h2("7.2 Coleta de dados (15 min)"));
C.push(num("Upload do sketch 03. Abrir o Serial Monitor (9600 baud).", "b3"));
C.push(num("Digitar a classe (0, 1, 2 ou 3) e Enter — o display mostra a classe escolhida.", "b3"));
C.push(num("Apertar GRAVAR: bip grave = prepare-se; bip agudo + LED azul = gravando por 1 s. Fazer o gesto durante o LED azul.", "b3"));
C.push(num("Repetir até ~20 gravações por classe (o Serial Monitor mostra a contagem). Variar: quem faz o gesto, a velocidade, a distância.", "b3"));
C.push(num("Copiar todo o texto do Serial Monitor (Ctrl+A, Ctrl+C), colar num editor e salvar como dados_grupoX.csv.", "b3"));
C.push(spacer());
C.push(table(["Classe", "Como fazer o gesto"], [
  ["0 PARADO", "Metade das gravações com a mão parada a 10–30 cm; metade sem nada na frente"],
  ["1 APROXIMAR", "Mão começa a ~40 cm e chega a ~10 cm durante o LED azul"],
  ["2 AFASTAR", "Mão começa a ~10 cm e vai até ~40 cm"],
  ["3 ACENAR", "Vai-e-vem rápido da mão, de frente para o sensor, entre ~10 e ~30 cm"],
], [2000, 7638]));
C.push(spacer());
C.push(alerta("Erro mais comum", "Gravar todas as amostras do mesmo jeito, com a mesma pessoa. O modelo decora aquele jeito e falha com outra pessoa. Diversidade nos dados vale mais do que quantidade."));
C.push(pageBreak());
C.push(h2("7.3 Treino no Colab (20 min)"));
C.push(num("Abrir colab.research.google.com → Arquivo → Fazer upload de notebook → treino_modelo_colab.ipynb.", "b3b"));
C.push(num("Executar as células em ordem (Shift+Enter). Na célula 1, enviar o dados_grupoX.csv.", "b3b"));
C.push(num("Observar os gráficos: qual feature separa melhor cada classe?", "b3b"));
C.push(num("Treinar com PROFUNDIDADE = 4, ler a acurácia de treino e de teste e a matriz de confusão.", "b3b"));
C.push(num("Rodar o experimento de profundidade (1 a 10) e discutir o gráfico de overfitting.", "b3b"));
C.push(num("Na última célula, o notebook gera e baixa o arquivo modelo.h.", "b3b"));
C.push(h3("Exemplo de modelo.h gerado"));
C.push(codeBlock([
  "int classificar(const float *f) {",
  "  if (f[4] <= -18.9750f) {          // inclinacao",
  "    return 1;                        // APROXIMAR",
  "  } else {",
  "    if (f[1] <= 2.4650f) {           // desvio",
  "      return 0;                      // PARADO",
  "    } else {",
  "      if (f[5] <= 3.5000f) return 2; // trocas -> AFASTAR",
  "      else                 return 3; // ACENAR",
  "    }",
  "  }",
  "}",
]));
C.push(spacer());
C.push(h2("7.4 Discussão (5 min)"));
C.push(bullet("Treino 100% e teste 70%: o que aconteceu? (overfitting — a árvore decorou)."));
C.push(bullet("Onde a matriz de confusão mostra mais erros? Faz sentido fisicamente? (ex.: AFASTAR lento parece PARADO)."));
C.push(bullet("Compare a árvore com as regras que vocês tentaram no Bloco 2."));
C.push(spacer());
C.push(dica("Plano B (sem internet ou sem Colab)", "Os grupos entregam o .csv ao professor (pendrive), que roda o mesmo notebook no próprio computador (Jupyter) e devolve o modelo.h. Se a coleta falhar, o arquivo dados_exemplo_simulado.csv permite rodar o notebook inteiro — mas é simulado e não substitui os dados reais do sensor."));

// BLOCO 4
C.push(pageBreak());
C.push(h1("8. Bloco 4 — Integração: o robô ganha cérebro (35 min)"));
C.push(h2("Roteiro"));
C.push(num("(5 min) Copiar o modelo.h baixado para a pasta 04_sentinela_ml, substituindo o de exemplo.", "b4"));
C.push(num("(5 min) Conferir que os ajustes do topo do sketch (display, buzzer, relé, LDR_ESCURO) estão iguais aos do sketch 01.", "b4"));
C.push(num("(15 min) Upload e testes. O Serial Monitor mostra as features e a classe de cada janela — use para entender os erros.", "b4"));
C.push(num("(10 min) Se o robô errar um gesto com frequência: gravar mais exemplos dessa classe (sketch 03), retreinar e subir de novo. Esse é o ciclo real de quem trabalha com ML.", "b4"));
C.push(h3("O coração do sketch 04"));
C.push(codeBlock([
  "janela[nJanela++] = d;                   // 1 leitura a cada 50 ms",
  "if (nJanela < N_AMOSTRAS) return;        // janela ainda incompleta",
  "",
  "calcularFeatures(janela, N_AMOSTRAS, f); // mesmas 6 features da coleta",
  "int classe = classificar(f);             // <- o modelo treinado no Colab",
  "mostrar(DIGITOS[classe]);",
  "",
  "if      (classe == 1) reagirAlarme();",
  "else if (classe == 2) { reagirTchau(); irPara(PATRULHA); }",
  "else if (classe == 3) { reagirAmigo(); irPara(PATRULHA); }",
]));
C.push(spacer());
C.push(conceito("Por que as features precisam ser idênticas", "O modelo aprendeu a partir dos números calculados pela função calcularFeatures() do sketch 03. Se o sketch 04 calcular de outro jeito (outra janela, outro período, outro filtro), o modelo recebe números que nunca viu e erra. Por isso a função é uma cópia exata — e N_AMOSTRAS e PERIODO_MS também."));

// ENCERRAMENTO
C.push(h1("9. Encerramento: teste cruzado (10 min)"));
C.push(bullet("Cada grupo apresenta o robô em 2 minutos: a acurácia no Colab e uma demonstração."));
C.push(bullet("Depois, um aluno de outro grupo faz os gestos no robô. Ele acerta tanto quanto com o próprio grupo?"));
C.push(bullet("Fechamento: os dados de treino definem o que o modelo sabe. Para generalizar, é preciso dados de muitas pessoas — e foi isso que a célula 7 do notebook (treinar com todos os grupos menos um) mostrou."));
C.push(bullet("Gancho para o curso: sistemas embarcados, inteligência artificial, processamento de sinais, controle."));

// SOLUÇÃO DE PROBLEMAS
C.push(pageBreak());
C.push(h1("10. Solução de problemas"));
C.push(table(["Sintoma", "Causa provável", "O que fazer"], [
  ["Distância sempre 200", "TRIG/ECHO invertidos ou sem 5V", "Conferir D7 = TRIG, D8 = ECHO e alimentação"],
  ["Distância oscila muito", "Superfície inclinada ou macia; mão muito longe", "Testar com objeto plano a 10–40 cm"],
  ["Arduino reinicia quando o servo mexe", "Queda de tensão no USB", "Capacitor 100 µF no 5V/GND; porta USB direta"],
  ["Servo treme parado", "Ruído de alimentação", "Mesmo acima; prender bem o servo na base"],
  ["Display mostra tudo invertido", "Tipo de display trocado", "Inverter DISPLAY_ANODO_COMUM"],
  ["Buzzer sempre com o mesmo som", "Buzzer ativo", "BUZZER_ATIVO = true (melodias viram bips)"],
  ["Relé ligado o tempo todo", "Módulo com lógica invertida", "Inverter RELE_ATIVO_BAIXO"],
  ["Erro 'modelo.h: No such file'", "Arquivo fora da pasta do sketch", "modelo.h deve estar ao lado do .ino"],
  ["Colab: '0 amostras carregadas'", "Arquivo copiado sem as linhas de dados", "Abrir o .csv e conferir as linhas com 7 números"],
  ["Robô confunde dois gestos", "Poucos ou pouco variados exemplos", "Gravar mais dessa classe e retreinar"],
  ["Robô reage a qualquer coisa como APROXIMAR", "A pessoa chega para fazer o gesto", "Esperar o bip da ATENÇÃO antes de gesticular"],
], [2900, 3200, 3538]));

// DESAFIOS
C.push(h1("11. Desafios extras (para quem terminar antes)"));
C.push(bullet([["Nova classe: ", { bold: true }], "\"dois acenos\" ou \"mão parada muito perto\". Grave, retreine e programe uma reação nova."]));
C.push(bullet([["Modelo da turma: ", { bold: true }], "envie os CSVs dos 4 grupos juntos ao Colab e compare com o modelo de um grupo só."]));
C.push(bullet([["Outro algoritmo: ", { bold: true }], "no notebook, compare a árvore com k-NN (KNeighborsClassifier). Por que o k-NN seria difícil de levar para o Uno?"]));
C.push(bullet([["Radar: ", { bold: true }], "no sketch 02, imprima ângulo e distância e desenhe um mapa da sala no Python."]));
C.push(bullet([["Temperatura: ", { bold: true }], "o kit tem um sensor NTC — use-o em A1 para um alarme de temperatura alta."]));

// ANEXOS
C.push(pageBreak());
C.push(h1("Anexo A — Arquivos do curso"));
C.push(table(["Pasta / arquivo", "Para que serve", "Quando"], [
  ["parte1-arduino-passo-a-passo/etapa1_led … etapa9_rele", "Um código de teste por componente", "Parte 1"],
  ["parte2-robo-sentinela/01_teste_hardware", "Testa o robô inteiro; Serial Plotter", "Fim da Parte 1"],
  ["parte2-robo-sentinela/02_sentinela_regras", "Robô por regras (máquina de estados)", "Bloco 2"],
  ["parte2-robo-sentinela/03_coleta_dados", "Grava gestos rotulados em CSV", "Bloco 3"],
  ["parte2-robo-sentinela/ml/treino_modelo_colab.ipynb", "Treina, avalia e exporta o modelo.h", "Bloco 3"],
  ["parte2-robo-sentinela/ml/dados_exemplo_simulado.csv", "Dados simulados (plano B)", "Bloco 3"],
  ["parte2-robo-sentinela/04_sentinela_ml", "Robô final; modelo.h de exemplo para substituir", "Bloco 4"],
  ["docs/diagramas", "Diagrama completo e diagramas de cada etapa", "Montagem"],
], [4300, 3838, 1500]));
C.push(spacer());
C.push(p([["Observação: ", { bold: true }], "a Arduino IDE exige que cada .ino fique numa pasta com o mesmo nome — por isso cada código tem a sua pasta."]));

C.push(h1("Anexo B — Ficha de coleta do grupo"));
C.push(p("Grupo: ____________   Integrantes: ________________________________________________"));
C.push(table(["Classe", "Quem gravou / como variou", "Qtd.", "Acurácia teste"], [
  ["0 PARADO", "", "", ""],
  ["1 APROXIMAR", "", "", ""],
  ["2 AFASTAR", "", "", ""],
  ["3 ACENAR", "", "", ""],
], [2000, 4638, 1300, 1700]));
C.push(spacer());
C.push(p("Profundidade escolhida: ______   Acurácia treino: ______ %   Acurácia teste: ______ %"));
C.push(p("Gesto que o robô mais errou e por quê: ____________________________________________________"));
C.push(p("_______________________________________________________________________________________"));
C.push(p("Acerto no teste cruzado (aluno de outro grupo): ______ de ______ gestos"));

// ---------- documento ----------
const bulletLevels = [
  { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 260 } } } },
];
const numCfg = (ref) => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 300 } } } }] });

const doc = new Document({
  creator: "Paulo César da Silva Junior",
  title: "Minicurso de Robótica — Robô Sentinela com Machine Learning",
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  numbering: { config: [{ reference: "bullets", levels: bulletLevels }, ...["passos", "b1", "b2", "b3", "b3b", "b4"].map(numCfg)] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      border: { bottom: { color: "CCCCCC", space: 4, style: BorderStyle.SINGLE, size: 4 } },
      children: [new TextRun({ text: "Minicurso de Robótica — Robô Sentinela com ML", size: 16, color: "888888", font: FONT })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Página ", size: 16, color: "888888", font: FONT }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888", font: FONT })] })] }) },
    children: C,
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync("Minicurso_Robo_Sentinela_ML.docx", b); console.log("ok"); });
