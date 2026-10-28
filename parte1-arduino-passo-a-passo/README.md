# Parte 1 — Arduino passo a passo

Cada componente entra **direto no lugar definitivo** da protoboard e é testado com um código curto antes do próximo. Ao final, a montagem é exatamente a do robô da Parte 2. Nada precisa ser desmontado.

Em cada diagrama, a peça nova aparece em destaque. As etiquetas coloridas (D11, A0…) indicam para qual pino do Arduino vai aquele fio.

| Etapa | Componente | Código | Diagrama |
|---|---|---|---|
| 0 | Energia nos trilhos (5 V e GND) | — | [e0](../docs/diagramas/etapas/e0_alimentacao.png) |
| 1 | LED vermelho → D11 | [`etapa1_led`](etapa1_led) | [e1](../docs/diagramas/etapas/e1_led.png) |
| 2 | LEDs verde → D12 e azul → D13 | [`etapa2_leds`](etapa2_leds) | [e2](../docs/diagramas/etapas/e2_leds.png) |
| 3 | Botão → D2 (pull-up interno) | [`etapa3_botao`](etapa3_botao) | [e3](../docs/diagramas/etapas/e3_botao.png) |
| 4 | Buzzer → D10 | [`etapa4_buzzer`](etapa4_buzzer) | [e4](../docs/diagramas/etapas/e4_buzzer.png) |
| 5 | LDR + 1 kΩ → A0 (calibrar o limiar) | [`etapa5_ldr`](etapa5_ldr) | [e5](../docs/diagramas/etapas/e5_ldr.png) |
| 6 | Display 7 segmentos → D3–D6, A3–A5 | [`etapa6_display`](etapa6_display) | [e6](../docs/diagramas/etapas/e6_display.png) |
| 6b | Contador: botão + display + buzzer | [`etapa6b_contador`](etapa6b_contador) | — |
| 7 | HC-SR04 → D7 (Trig), D8 (Echo) | [`etapa7_ultrassom`](etapa7_ultrassom) | [e7](../docs/diagramas/etapas/e7_hcsr04.png) |
| 8 | Servo → D9 + capacitor 100 µF | [`etapa8_servo`](etapa8_servo) | [e8](../docs/diagramas/etapas/e8_servo.png) |
| 9 | Relé → A2 | [`etapa9_rele`](etapa9_rele) | [e9](../docs/diagramas/etapas/e9_rele.png) |
| ✓ | Teste geral | [`../parte2-robo-sentinela/01_teste_hardware`](../parte2-robo-sentinela/01_teste_hardware) | [completo](../docs/diagramas/etapas/e10_completo.png) |

Cada código traz no comentário inicial a montagem e o resultado esperado. No fim de cada código há desafios para quem terminar antes.

## Regras de ouro

1. Monte com a USB **desligada**.
2. Nunca ligue 5 V direto no GND.
3. Respeite a polaridade do LED, do buzzer e do capacitor.
4. Montou, não mexe mais: cada peça já vai para o lugar final.
