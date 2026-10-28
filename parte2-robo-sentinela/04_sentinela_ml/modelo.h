// ATENÇÃO: MODELO DE EXEMPLO treinado com dados SINTÉTICOS (simulados).
// Serve só para o sketch compilar e para testar a montagem.
// Substitua pelo modelo.h gerado no Colab com os dados do seu grupo.
// modelo.h — gerado automaticamente no Colab (Robô Sentinela)
// Árvore de decisão: profundidade 4, 5 folhas
// f[0]=media  f[1]=desvio  f[2]=minimo  f[3]=maximo  f[4]=inclinacao  f[5]=trocas
#pragma once

int classificar(const float *f) {
  if (f[4] <= 13.7450f) {   // inclinacao
    if (f[1] <= 2.4650f) {   // desvio
      return 0;   // PARADO
    } else {
      if (f[5] <= 2.5000f) {   // trocas
        if (f[1] <= 17.5700f) {   // desvio
          return 1;   // APROXIMAR
        } else {
          return 0;   // PARADO
        }
      } else {
        return 3;   // ACENAR
      }
    }
  } else {
    return 2;   // AFASTAR
  }
}
