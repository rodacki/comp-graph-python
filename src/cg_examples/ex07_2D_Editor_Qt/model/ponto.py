from dataclasses import dataclass

@dataclass
class Ponto:
    """Representa um ponto 2D no plano cartesiano."""
    x: float = 0.0
    y: float = 0.0

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"