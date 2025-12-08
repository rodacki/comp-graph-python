#version 330 core

layout(location = 0) in vec2 a_pos;

uniform mat4 u_viewproj;

void main() {
    gl_Position = u_viewproj * vec4(a_pos, 0.0, 1.0);
}