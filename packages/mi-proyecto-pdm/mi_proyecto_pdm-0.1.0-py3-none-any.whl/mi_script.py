# Librerías de producción
import django
import requests
import psycopg2

# Librerías de desarrollo
import pytest


# black y ruff se usan por consola, por eso no se importan aquí

def mostrar_versiones():
    print("📦 Verificación de versiones de librerías instaladas con PDM\n")

    print("Versión de Django:", django.get_version())
    print("Versión de requests:", requests.__version__)
    print("Versión de psycopg2-binary:", psycopg2.__version__)
    print("Versión de pytest:", pytest.__version__)

    print(
        "\n🛠️ Nota: Las herramientas 'black' y 'ruff' no se usan desde el código Python, sino que se ejecutan por terminal.")


if __name__ == "__main__":
    mostrar_versiones()

