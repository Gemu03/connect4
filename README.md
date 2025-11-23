# Agente Inteligente para Connect-4 (Grupo C)

Este repositorio contiene la implementación de **`Policy`**, un agente diseñado para el "Reto Connect-4" del curso Fundamentos de Inteligencia Artificial (2025.2) en la Universidad de La Sabana.

## 🧠 Estrategia del Agente

Nuestro agente utiliza una **Arquitectura Híbrida** que combina búsqueda adversaria con aprendizaje por refuerzo para garantizar un rendimiento robusto desde la primera partida:

1.  **Motor de Búsqueda:** Algoritmo **Minimax con Poda Alfa-Beta** y profundidad dinámica (`depth=4`) para razonamiento táctico.
2.  **Heurística Posicional:** Evaluación matemática basada en el control del centro y ventanas de 4 fichas para guiar la búsqueda en nodos hoja desconocidos.
3.  **Persistencia (Q-Learning):** Integración de una **Q-Table** que permite al agente "recordar" estados visitados y aprender de partidas previas (*Self-Play*).
4.  **Defensa Reactiva:** Lógica de bloqueo de emergencia para evitar derrotas inmediatas antes de iniciar la búsqueda profunda.

## 📂 Estructura del Proyecto

```text
.
├── groups/
│   └── GroupC/
│       ├── policy.py          # Código fuente del agente (Policy)
│       └── train/
│           └── q_table.pkl    # Conocimiento aprendido (Persistencia)
├── connect4/                  # Lógica base del juego (entorno)
├── entrega.ipynb              # Notebook de validación, entrenamiento y gráficas
└── README.md                  # Este archivo
```

## 🚀 Instalación y Ejecución

1. Clona este repositorio:
```bash
git clone https://github.com/Gemu03/connect4
cd connect4
```

2. Instala las dependencias necesarias
```bash
pip install numpy matplotlib tqdm notebook    
```

##  Documentación 
La Documentación completa del proyecto, se encuentra en el archivo `entrega.ipynb`, donde se detalla la implementación, pruebas y resultados obtenidos por el agente.

##  Presentaicón
La presentación del proyecto se puede encontrar en el siguiente enlace: [Presentación Connect-4](https