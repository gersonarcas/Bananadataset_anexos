
"""
Script para seleccionar N imágenes al azar de una carpeta
y copiarlas a otra carpeta.
"""

import os
import random
import shutil
from pathlib import Path

# ==============================
# CONFIGURACIÓN
# ==============================
CARPETA_ORIGEN = "C:\\utp1\\TESIS\\DATASET_PIUSUUBANANA\\dataset_sinparticion\\sigatoka"
CARPETA_DESTINO = "c:\\utp1\\TESIS\\DATASET_PIUSUUBANANA\\dataset_sinparticion\\validacion sigatoka"
CANTIDAD = 100
random.seed(42)  # Semilla para reproducibilidad
# Extensiones de imagen que se van a considerar
EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}


def seleccionar_y_copiar(origen, destino, cantidad):
    origen = Path(origen)
    destino = Path(destino)

    if not origen.is_dir():
        raise FileNotFoundError(f"La carpeta de origen no existe: {origen}")

    # Crear carpeta destino si no existe
    destino.mkdir(parents=True, exist_ok=True)

    # Listar solo archivos de imagen
    imagenes = [
        f for f in origen.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONES_VALIDAS
    ]

    if not imagenes:
        print("No se encontraron imágenes en la carpeta de origen.")
        return

    if len(imagenes) < cantidad:
        print(f"Solo hay {len(imagenes)} imágenes disponibles, "
              f"se copiarán todas en lugar de {cantidad}.")
        seleccionadas = imagenes
    else:
        seleccionadas = random.sample(imagenes, cantidad)

    for i, imagen in enumerate(seleccionadas, start=1):
        destino_archivo = destino / imagen.name
        # Evitar sobrescribir si ya existe un archivo con el mismo nombre
        contador = 1
        while destino_archivo.exists():
            destino_archivo = destino / f"{imagen.stem}_{contador}{imagen.suffix}"
            contador += 1

        shutil.copy2(imagen, destino_archivo)
        print(f"[{i}/{len(seleccionadas)}] Copiado: {imagen.name}")

    print(f"\nListo. Se copiaron {len(seleccionadas)} imágenes a: {destino}")


if __name__ == "__main__":
    seleccionar_y_copiar(CARPETA_ORIGEN, CARPETA_DESTINO, CANTIDAD)
