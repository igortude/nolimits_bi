# scripts_ia/__init__.py

"""
Módulo central de IA do NoLimits
NÃO importa nada do dashboard aqui para evitar import circular
"""

from .contexto_negocio import CONTEXTO_NOLIMITS, CORRECOES_AUTOMATICAS
from .glossario import GLOSSARIO_NOLIMITS
from .exemplos_sql import obter_todos_exemplos

# Só exporta o que já está pronto
__all__ = [
    "CONTEXTO_NOLIMITS",
    "CORRECOES_AUTOMATICAS",
    "GLOSSARIO_NOLIMITS",
    "obter_todos_exemplos",
]