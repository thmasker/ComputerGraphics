import pstats

# python -m cProfile -o profile src\metaballs.py example.json

p = pstats.Stats('profile')
p.strip_dirs().sort_stats(-1).print_stats()