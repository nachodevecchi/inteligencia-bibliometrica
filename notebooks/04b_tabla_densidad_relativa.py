import pandas as pd
import os

# ===================== CONFIGURACIÓN =====================
INFORME_1 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
INFORME_2 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNAL.xlsx"

UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_2 = "CAMPINAS"
UNIVERSIDAD_3 = "UNAL"

SHEET_NAME = "Áreas temáticas"

MIN_COUNT = 50
MIN_PER_1000 = 10
TOP_N = 20

# ⚠️ Completá con el total real de papers de cada universidad
# Lo encontrás en la hoja "Resumen" de cualquier informe comparativo
TOTALES = {
    "UBA": 13947,      # ← reemplazá con el total real
    "CAMPINAS": 1000,  # ← reemplazá con el total real
    "UNAL": 1000,      # ← reemplazá con el total real
}

OUTPUT_FILENAME = f"tabla_densidad_{UNIVERSIDAD_REFERENCIA}_{UNIVERSIDAD_2}_{UNIVERSIDAD_3}.xlsx"
# =========================================================


def cargar_columnas_universidad(file_path, sheet_name, universidad):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]
        cols = ["Area tematica", f"{universidad}_count", f"{universidad}_per_1000"]
        cols_faltantes = [c for c in cols if c not in df.columns]
        if cols_faltantes:
            raise ValueError(f"Columnas faltantes en {file_path}: {cols_faltantes}")
        return df[cols].copy()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {file_path}")
        raise
    except ValueError as e:
        print(f"❌ Error: {e}")
        raise


def fusionar_informes(informe_1, informe_2, univ_ref, univ_2, univ_3, sheet_name):
    print(f"📂 Cargando informe 1: {univ_ref} vs {univ_2}...")
    df1 = pd.read_excel(informe_1, sheet_name=sheet_name)
    df1.columns = [c.strip() for c in df1.columns]
    cols_df1 = ["Area tematica",
                f"{univ_ref}_count", f"{univ_ref}_per_1000",
                f"{univ_2}_count", f"{univ_2}_per_1000"]
    cols_faltantes = [c for c in cols_df1 if c not in df1.columns]
    if cols_faltantes:
        raise ValueError(f"Columnas faltantes en informe 1: {cols_faltantes}")
    df1 = df1[cols_df1].copy()

    print(f"📂 Cargando informe 2: {univ_ref} vs {univ_3}...")
    df2 = cargar_columnas_universidad(informe_2, sheet_name, univ_3)

    print(f"🔗 Fusionando datos...")
    merged = df1.merge(df2, on="Area tematica", how="inner")
    print(f"✅ Fusión completada: {len(merged)} áreas en común")
    return merged


def filtrar_y_seleccionar(df, universidades, min_count, min_per_1000, top_n):
    mask = pd.Series([True] * len(df), index=df.index)
    for u in universidades:
        mask &= (df[f"{u}_count"] >= min_count)
        mask &= (df[f"{u}_per_1000"] >= min_per_1000)
    df_filtrado = df[mask].copy()
    print(f"✅ Áreas que cumplen criterios: {len(df_filtrado)}")

    df_filtrado["Total_combinado"] = sum(df_filtrado[f"{u}_count"] for u in universidades)
    top = df_filtrado.sort_values("Total_combinado", ascending=False).head(top_n).reset_index(drop=True)
    print(f"✅ Top {top_n} áreas seleccionadas")
    return top


def calcular_densidad(df, universidades, totales):
    for u in universidades:
        df[f"{u}_dens_%"] = (df[f"{u}_count"] / totales[u] * 100).round(3)
    return df


def exportar_excel(df, universidades, output_filename):
    columnas_finales = ["Area tematica"]
    for u in universidades:
        columnas_finales += [f"{u}_count", f"{u}_per_1000", f"{u}_dens_%"]

    df_export = df[columnas_finales].copy()

    out_path = os.path.join(os.path.expanduser("~"), "Desktop", output_filename)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df_export.to_excel(writer, sheet_name="Densidad relativa", index=False)

        resumen_rows = []
        for u in universidades:
            resumen_rows.append({
                "Universidad": u,
                "Área con mayor densidad": df.loc[df[f"{u}_dens_%"].idxmax(), "Area tematica"],
                "Densidad máxima (%)": df[f"{u}_dens_%"].max().round(3),
                "Densidad promedio (%)": df[f"{u}_dens_%"].mean().round(3)
            })
        pd.DataFrame(resumen_rows).to_excel(writer, sheet_name="Resumen", index=False)

    print(f"✅ Excel guardado en: {out_path}")


if __name__ == "__main__":
    try:
        universidades = [UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_2, UNIVERSIDAD_3]

        df = fusionar_informes(
            INFORME_1, INFORME_2,
            UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_2, UNIVERSIDAD_3,
            SHEET_NAME
        )

        print(f"\n🔍 Filtrando y seleccionando top {TOP_N} áreas...")
        df = filtrar_y_seleccionar(df, universidades, MIN_COUNT, MIN_PER_1000, TOP_N)

        print(f"\n📐 Calculando densidad relativa...")
        df = calcular_densidad(df, universidades, TOTALES)

        print(f"\n💾 Exportando Excel...")
        exportar_excel(df, universidades, OUTPUT_FILENAME)

        print("\n✨ ¡Listo!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
