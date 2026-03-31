# Ex01 (PyQt6) - Hello OpenGL Modern

## Objetivo didatico

Este exemplo inaugura a serie PyQt6 + OpenGL moderno com a menor estrutura
possivel:

- uma janela Qt;
- um canvas OpenGL (`QOpenGLWidget`);
- pipeline moderno com shader + VAO + VBO;
- desenho de um triangulo equilatero estatico em linhas (`GL_LINE_LOOP`).

## Controles

- `Esc`: encerra a aplicacao.
- Fechar janela na GUI: encerra a aplicacao.

## Execucao

```bash
poetry run ex01-pyqt6-hello-ogl-modern
```

## Estrutura

```text
ex01_pyqt6_hello_ogl_modern/
├── __main__.py
├── mainwindow.py
└── view/
    ├── glcanvas.py
    ├── renderer.py
    └── shaders.py
```
