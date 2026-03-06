import pandas as pd
import os

# ===================== CONFIGURACIÓN =====================
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_COMPARACION = "UNIVERSIDAD_2"

file_path = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNIVERSIDAD_2.xlsx"
sheet_name = "Áreas temáticas"

min_per_1000 = 9
min_count = 50
top_n_similares = 20

OUTPUT_FILENAME = f"tabla_similitudes_{UNIVERSIDAD_REFERENCIA}_{UNIVERSIDAD_COMPARACION}.xlsx"
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


def calcular_similitud(df, univ_ref, univ_comp):
    df["Diferencia_per_1000"] = (df[f"{univ_ref}_per_1000"] - df[f"{univ_comp}_per_1000"]).round(3)
    df["Diferencia_absoluta"] = df["Diferencia_per_1000"].abs().round(3)
    df["Domina"] = df["Diferencia_per_1000"].apply(lambda x: univ_ref if x >= 0 else univ_comp)
    return df


def exportar_excel(df, univ_ref, univ_comp, top_n, output_filename):
    df_similares = df.nsmallest(top_n, "Diferencia_absoluta").reset_index(drop=True)

    columnas_finales = [
        "Area tematica",
        f"{univ_ref}_count",
        f"{univ_ref}_per_1000",
        f"{univ_comp}_count",
        f"{univ_comp}_per_1000",
        "Diferencia_per_1000",
        "Diferencia_absoluta",
        "Domina"
    ]
    df_similares = df_similares[columnas_finales]

    out_path = os.path.join(os.path.expanduser("~"), "Desktop", output_filename)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df_similares.to_excel(writer, sheet_name="Áreas similares", index=False)

        resumen = pd.DataFrame({
            "Métrica": [
                "Total de áreas similares seleccionadas",
                f"De esas, domina {univ_ref}",
                f"De esas, domina {univ_comp}",
                "Diferencia absoluta promedio (per 1000)"
            ],
            "Valor": [
                len(df_similares),
                len(df_similares[df_similares["Domina"] == univ_ref]),
                len(df_similares[df_similares["Domina"] == univ_comp]),
                df_similares["Diferencia_absoluta"].mean().round(3)
            ]
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

        print(f"📐 Calculando similitud...")
        df = calcular_similitud(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)

        print(f"💾 Exportando Excel...")
        exportar_excel(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION, top_n_similares, OUTPUT_FILENAME)

        print("\n✨ ¡Listo!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
