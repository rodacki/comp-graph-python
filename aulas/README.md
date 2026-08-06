# aulas/ — scaffolds da edição 2026.2

Código que os alunos executam, **um diretório por aula**. Cada scaffold é um script
simples e comentado: para **ler, prever, rodar e modificar** — não um pacote a
instalar. A avaliação mira o *entendimento do resultado* (prever, depurar, explicar,
criticar), não a produção de código.

- **`aula01/`** — M1: primeira janela interativa em pyglet (primitivas, loop de
  eventos). Inclui um apêndice opcional de OpenGL "cru" (moderngl) para contraste.

Stack: **pyglet** (interativo) + **numpy** (rasterizador em software, módulos de 3D);
OpenGL de GPU só no fim. Cada pasta tem `requirements.txt` próprio (uso via `pip` num
`venv`); não depende do pacote Poetry `src/cg_examples/` (edição 2024, referência).
