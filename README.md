# Proyecto 2 — Algoritmos de Búsqueda en Laberintos

**Inteligencia Artificial 2026**

## Integrantes
- Dilary Cruz — 231010
- June Herrera — 231038
- Andrés Mazariegos — 21749

## Descripción
Comparación de algoritmos de búsqueda (BFS, DFS, UCS, A*) para resolver laberintos
generados aleatoriamente con Kruskal y Prim.

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
# Problema 1: Generación de laberintos (GIFs)
python experiments/problem1_demo.py

# Problema 2: Resolver laberinto 60×80 con A*
python experiments/problem2_demo.py

# Problema 3: Comparación K=25 escenarios
python experiments/problem3_benchmark.py
```

## Estructura
```
src/maze/       — Grid, Kruskal, Prim
src/search/     — BFS, DFS, UCS, A*
src/viz/        — Render y animaciones matplotlib
src/benchmark/  — Runner K=25 y exportación CSV
experiments/    — Scripts de demostración
results/        — GIFs, plots, CSV generados
report/         — Reporte LaTeX
```
