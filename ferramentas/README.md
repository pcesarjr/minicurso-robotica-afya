# Ferramentas

Scripts que geraram os diagramas e a apostila. Só são necessários se você quiser alterar a montagem ou o texto.

| Script | Gera | Requisitos |
|---|---|---|
| `diagrama_montagem.py` | `img_montagem.png` (diagrama completo com legenda) | Python 3 + matplotlib |
| `diagrama_etapas.py` | pasta `etapas/` (um diagrama por etapa, Arduino e protoboard comentados) | Python 3 + matplotlib |
| `diagramas.py` | `img_pipeline.png` e `img_estados.png` | Python 3 + matplotlib |
| `gerar_apostila.js` | `Minicurso_Robo_Sentinela_ML.docx` | Node.js + `npm install docx` |

Os arquivos são gerados na pasta de onde o script é executado. O `gerar_apostila.js` precisa das imagens `img_pipeline.png`, `img_estados.png` e `img_montagem.png` nessa mesma pasta.
