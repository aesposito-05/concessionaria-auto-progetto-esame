#!/usr/bin/env python
"""Utility a riga di comando di Django per attivita' amministrative."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concessionaria_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossibile importare Django. Assicurati che sia installato e "
            "disponibile sulla variabile d'ambiente PYTHONPATH. Hai dimenticato "
            "di attivare un virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
