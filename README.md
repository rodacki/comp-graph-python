# Computação Gráfica em Python

Código, *scaffolds* e demos da disciplina **CCB0941 — Computação Gráfica**
(IFC Blumenau, Bacharelado em Ciência da Computação). Docente: Paulo C. Rodacki Gomes.

O repositório tem duas áreas, de edições diferentes da disciplina:

## `aulas/` — edição atual (2026.2)

*Scaffolds* mínimos, um por aula, feitos para o aluno **ler de cima a baixo, prever,
rodar e modificar**. Stack: **pyglet** nos módulos interativos (janela, eventos,
primitivas) e rasterizador em software (`numpy`) nos módulos conceituais de 3D;
OpenGL de GPU só no fim do curso. Cada pasta traz seu `README.md` e `requirements.txt`.

```bash
cd aulas/aula01
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python primeira_janela.py
```

> O material didático (plano de curso, slides, exercícios, avaliações) fica em outro
> lugar; este repositório é **só o código** que os alunos executam.

## `src/cg_examples/` — edição 2024 (referência)

Exemplos da oferta anterior, empacotados com Poetry (`poetry run ex01-hello`, etc.).
Vão de "hello OpenGL" a um editor 2D completo em PyQt6 + ModernGL. Usam PyOpenGL
(GLUT/moderngl). **Mantidos como referência**; a edição 2026 não depende deles e
migra o que fizer sentido para `aulas/`, reescrito na stack/pedagogia nova.
