# Ex08 - Editor 2D mínimo com OpenGL moderno

## Objetivo didático

Este exemplo demonstra a estrutura mínima para edição interativa 2D usando
**PyQt5 + OpenGL moderno** (shader, VAO, VBO), sem interface extra.

Foco do exemplo:
- mostrar o ciclo do `QOpenGLWidget` (`initializeGL`, `resizeGL`, `paintGL`);
- desenhar segmentos 2D com `glDrawArrays(GL_LINES)`;
- separar responsabilidades entre estado de interação, modelo e renderer.

## Conceitos OpenGL moderno mostrados

- Compilação e linkedição de shaders GLSL.
- Uso de `VAO` e `VBO` para armazenar atributos de vértice.
- Upload dinâmico de vértices para desenhar a cena atual.
- Renderização de linhas sólidas e preview tracejado via fragment shader.

## Estrutura simplificada

```text
ex08_2D_simple_ogl_modern/
├── __main__.py         # Entry point (QApplication + QSurfaceFormat)
├── mainwindow.py       # Janela mínima com apenas o canvas
├── globals/settings.py # Estado global (modelo, ponto pendente, cores)
├── model/              # Entidades: Ponto, Segmento, Modelo
├── state/              # Context + IdleState para interação por clique
└── view/
    ├── glcanvas.py     # QOpenGLWidget e delegação de eventos
    ├── renderer.py     # Pipeline moderno (shader + VAO/VBO + draw)
    └── shaders.py      # Fontes GLSL (vertex + fragment)
```

## Interação

- Clique esquerdo: define pontos em pares.
- Primeiro clique: define ponto inicial e ativa preview.
- Movimento do mouse: mostra preview **verde tracejado** do próximo segmento.
- Segundo clique: confirma segmento no modelo (linha sólida).
- Tecla `Esc`: encerra a aplicação.

## Observações de compatibilidade (macOS)

- O exemplo solicita contexto OpenGL 3.3 Core Profile.
- Em Core Profile no macOS, `glLineWidth` costuma aceitar apenas `1.0`.
  Por isso o exemplo fixa espessura de linha em `1.0` para estabilidade.

## Execução

```bash
poetry run ex08-simple-ogl-modern
```

## Exercícios sugeridos

1. **Cor por segmento**
   - Modifique o modelo para armazenar cor em cada `Segmento`.
   - Desenhe cada segmento com uma cor diferente.

2. **Pré-visualização com espessura diferenciada**
   - Mantenha segmentos confirmados sólidos e o preview com estilo distinto.
   - Discuta limitações de espessura de linha no Core Profile.

3. **Limpar cena com teclado**
   - Adicione atalho (por exemplo, tecla `C`) para remover todos os segmentos.
   - Documente em qual camada a ação deve ser implementada (estado vs modelo).

4. **Persistência simples em arquivo**
   - Salve segmentos em JSON (lista de pontos).
   - Recarregue a cena ao iniciar a aplicação.

5. **Snap em grade (grid snapping)**
   - Quantize coordenadas de clique para uma malha regular em NDC.
   - Compare visualmente comportamento com e sem snap.

6. **Renderização com EBO (opcional avançado)**
   - Reestruture o renderer para usar índices, discutindo diferença entre
     `glDrawArrays` e `glDrawElements`.
