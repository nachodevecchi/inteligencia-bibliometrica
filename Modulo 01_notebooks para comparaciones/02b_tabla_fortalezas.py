import pandas as pd
import os

# ===================== CONFIGURACIÓN =====================
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_COMPARACION = "UNIVERSIDAD_2"

file_path = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNIVERSIDAD_2.xlsx"
sheet_name = "Áreas temáticas"

min_per_1000 = 9
min_count = 50
top_n_extremos = 10

OUTPUT_FILENAME = f"tabla_fortalezas_{UNIVERSIDAD_REFERENCIA}_{UNIVERSIDAD_COMPARACION}.xlsx"
# =========================================================


def cargar_datos(file_path, sheet_name, univ_ref, univ_comp):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]
        cols_requeridas = [
            "Area tematica",
            f"{univ_ref}_count", f"{univ_ref}_per_1000",
            f"{univ_comp}_count", f"{univ_comp}_per_1000"
        ]
        cols_faltantes = [c for c in cols_requeridas if c not in df.columns]
        if cols_faltantes:
            raise ValueError(f"Columnas faltantes: {cols_faltantes}")
        return df[cols_requeridas].copy()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {file_path}")
        raise
    except ValueError as e:
        print(f"❌ Error: {e}")
        raise


def filtrar_datos(df, univ_ref, univ_comp, min_per_1000, min_count):
    mask = (
        (df[f"{univ_ref}_per_1000"] >= min_per_1000) &
        (df[f"{univ_comp}_per_1000"] >= min_per_1000) &
        (df[f"{univ_ref}_count"] >= min_count) &
        (df[f"{univ_comp}_count"] >= min_count)
    )
    return df[mask].copy()


def calcular_diferencia(df, univ_ref, univ_comp):
    df["Diferencia_per_1000"] = (df[f"{univ_ref}_per_1000"] - df[f"{univ_comp}_per_1000"]).round(3)
    df["Domina"] = df["Diferencia_per_1000"].apply(lambda x: univ_ref if x >= 0 else univ_comp)
    return df


def seleccionar_extremos(df, univ_ref, univ_comp, top_n):
    top_ref = df.nlargest(top_n, "Diferencia_per_1000").copy()
    top_ref["Grupo"] = f"Fortalezas {univ_ref}"
    top_comp = df.nsmallest(top_n, "Diferencia_per_1000").copy()
    top_comp["Grupo"] = f"Fortalezas {univ_comp}"
    return pd.concat([top_ref, top_comp]).reset_index(drop=True)


def exportar_excel(df, univ_ref, univ_comp, output_filename):
    columnas_finales = [
        "Grupo",
        "Area tematica",
        f"{univ_ref}_count",
        f"{univ_ref}_per_1000",
        f"{univ_comp}_count",
        f"{univ_comp}_per_1000",
        "Diferencia_per_1000",
        "Domina"
    ]
    df = df[columnas_finales]

    out_path = os.path.join(os.path.expanduser("~"), "Desktop", output_filename)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Fortalezas y Debilidades", index=False)

        # Hoja resumen
        fortalezas_ref = df[df["Grupo"] == f"Fortalezas {univ_ref}"]
        fortalezas_comp = df[df["Grupo"] == f"Fortalezas {univ_comp}"]
        resumen = pd.DataFrame({
            "Categoría": [f"Áreas donde domina {univ_ref}", f"Áreas donde domina {univ_comp}"],
            "Cantidad de áreas": [len(fortalezas_ref), len(fortalezas_comp)]
        })
        resumen.to_excel(writer, sheet_name="Resumen", index=False)

    print(f"✅ Excel guardado en: {out_path}")


if __name__ == "__main__":
    try:
        print(f"📊 Cargando datos...")
        df = cargar_datos(file_path, sheet_name, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)

        print(f"🔍 Filtrando áreas...")
        df = filtrar_datos(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION, min_per_1000, min_count)
        print(f"✅ Áreas que cumplen criterios: {len(df)}")

        print(f"📐 Calculando diferencias...")
        df = calcular_diferencia(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)

        print(f"💪 Seleccionando fortalezas...")
        df = seleccionar_extremos(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION, top_n_extremos)

        print(f"💾 Exportando Excel...")
        exportar_excel(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION, OUTPUT_FILENAME)

        print("\n✨ ¡Listo!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
