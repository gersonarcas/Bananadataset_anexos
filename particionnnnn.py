"""
dividir_train_val_test.py

Divide tus carpetas por clase (fusarium, sana, sigatoka, ...) en
train/val/test, respetando la proporcion 70/15/15 DENTRO de cada clase
(split estratificado), para que ninguna particion quede desbalanceada
ni haya fuga de datos entre train/val/test.

Estructura de entrada esperada:
    ROOT_DIR/
        fusarium/
            img1.jpg
            img2.jpg
            ...
        sana/
            ...
        sigatoka/
            ...

Estructura de salida generada:
    OUTPUT_DIR/
        train/
            fusarium/...
            sana/...
            sigatoka/...
        val/
            ...
        test/
            ...

Por defecto los archivos se COPIAN (no se mueven), para no arriesgar
tus datos ya limpios y redimensionados. Si prefieres moverlos para
ahorrar espacio en disco, cambia COPIAR_NO_MOVER a False.

USO:
    python dividir_train_val_test.py

Antes de correr, edita la seccion CONFIGURACION mas abajo.
"""

import random
import shutil
from pathlib import Path

# =========================================================
# CONFIGURACION - AJUSTA ESTO A TU CASO
# =========================================================

ROOT_DIR = ""    # carpeta que contiene fusarium/, sana/, sigatoka/
OUTPUT_DIR = ""        # carpeta donde se creara train/val/test
PROPORCIONES = {
    "train": 0.70,
    "val": 0.15,
    "test": 0.15,
}

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

# Semilla fija para que el split sea reproducible (mismo resultado cada
# vez que corras el script sobre los mismos archivos).
SEMILLA = 42

# True = copia los archivos (mas seguro, usa mas disco)
# False = mueve los archivos (ahorra disco, pero es destructivo)
COPIAR_NO_MOVER = True


def main():
    assert abs(sum(PROPORCIONES.values()) - 1.0) < 1e-6, \
        "Las proporciones de PROPORCIONES deben sumar 1.0"

    root = Path(ROOT_DIR)
    if not root.is_dir():
        print(f"ERROR: no se encontro '{ROOT_DIR}'. Ajusta ROOT_DIR.")
        return

    output_root = Path(OUTPUT_DIR)
    random.seed(SEMILLA)

    resumen = {}

    labels = [d for d in sorted(root.iterdir()) if d.is_dir()]
    if not labels:
        print(f"No se encontraron subcarpetas de clases dentro de '{ROOT_DIR}'.")
        return

    for label_dir in labels:
        label = label_dir.name
        imagenes = [p for p in sorted(label_dir.iterdir())
                    if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS]

        if not imagenes:
            print(f"  [!] '{label}' no tiene imagenes, se omite.")
            continue

        random.shuffle(imagenes)

        n_total = len(imagenes)
        n_train = round(n_total * PROPORCIONES["train"])
        n_val = round(n_total * PROPORCIONES["val"])
        # El resto va a test, para asegurar que la suma cuadre exacto
        n_test = n_total - n_train - n_val

        splits = {
            "train": imagenes[:n_train],
            "val": imagenes[n_train:n_train + n_val],
            "test": imagenes[n_train + n_val:],
        }

        resumen[label] = {}

        for split, archivos in splits.items():
            destino_dir = output_root / split / label
            destino_dir.mkdir(parents=True, exist_ok=True)

            for img_path in archivos:
                destino = destino_dir / img_path.name
                if COPIAR_NO_MOVER:
                    shutil.copy2(img_path, destino)
                else:
                    shutil.move(str(img_path), str(destino))

            resumen[label][split] = len(archivos)

    print(f"\n=== RESUMEN DEL SPLIT ({'copiado' if COPIAR_NO_MOVER else 'movido'}) ===")
    print(f"{'label':15s} | {'train':>6s} | {'val':>6s} | {'test':>6s} | {'total':>6s}")
    totales = {"train": 0, "val": 0, "test": 0}
    for label, counts in resumen.items():
        total_label = sum(counts.values())
        print(f"{label:15s} | {counts['train']:6d} | {counts['val']:6d} | "
              f"{counts['test']:6d} | {total_label:6d}")
        for s in totales:
            totales[s] += counts[s]

    print("-" * 55)
    print(f"{'TOTAL':15s} | {totales['train']:6d} | {totales['val']:6d} | "
          f"{totales['test']:6d} | {sum(totales.values()):6d}")

    print(f"\nGuardado en: {OUTPUT_DIR}/train|val|test/<label>/")
    print("Siguiente paso: corre generar_csv_dataset.py sobre "
          f"'{OUTPUT_DIR}' para obtener el CSV de control final.")


if __name__ == "__main__":
    main()