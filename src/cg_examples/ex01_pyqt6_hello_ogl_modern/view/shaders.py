"""Fontes GLSL usadas pelo renderer do ex01 PyQt6."""

VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec2 a_pos;

void main() {
    gl_Position = vec4(a_pos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;
uniform vec3 u_color;

void main() {
    FragColor = vec4(u_color, 1.0);
}
"""
