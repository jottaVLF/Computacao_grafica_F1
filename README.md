# 🏎️ F1 Renault R25 Simulator - OpenGL & Python

Um simulador de corrida estilo arcade/retro desenvolvido do zero utilizando **Python** e **OpenGL**. O projeto recria o icônico carro **Renault R25** (Campeão de 2005) em uma pista gerada proceduralmente.

## 📋 Sobre o Projeto

Este projeto foi criado para explorar a renderização gráfica 3D sem o uso de engines prontas (como Unity ou Unreal). Toda a geometria — do carro à pista — é desenhada via código utilizando primitivas do OpenGL.

### ✨ Funcionalidades Principais
* **Modelo 3D Detalhado:** Recriação "Low Poly" do Renault R25 com suspensão, aerofólios e pneus detalhados.
* **Pista Suave (Splines):** Utilização do algoritmo **Catmull-Rom Splines** para gerar curvas suaves e orgânicas, abandonando traçados puramente matemáticos.
* **Ambiente Completo:** Zebras 3D elevadas, áreas de escape (caixa de brita) e muros de contenção.
* **Câmera Orbital:** Sistema de câmera em 3ª pessoa com rotação livre ao redor do carro.
* **Correção Visual:** Implementação de camadas de profundidade para evitar *Z-Fighting* (o efeito de texturas piscando).

## 🛠️ Tecnologias Utilizadas
* [Python 3.x](https://www.python.org/)
* [Pygame](https://www.pygame.org/) (Contexto de janela e Input)
* [PyOpenGL](http://pyopengl.sourceforge.net/) (Renderização Gráfica e GLU)
