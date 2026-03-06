import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================== CONFIGURACIÓN =====================
# Rutas de los 2 informes comparativos (generados por el notebook 01)
INFORME_1 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
INFORME_2 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNAL.xlsx"

# Universidad de referencia (la que aparece en los dos informes)
UNIVERSIDAD_REFERENCIA = "UBA"

# Las otras dos universidades
UNIVERSIDAD_2 = "CAMPINAS"
UNIVERSIDAD_3 = "UNAL"

# Nombre de la hoja con los datos de áreas temáticas
SHEET_NAME = "Áreas temáticas"

# Filtros
MIN_COUNT = 50   # mínimo absoluto de papers por área (se aplica a las 3 universidades)
TOP_N = 20       # cantidad de áreas a mostrar

# Nombre del archivo de salida
OUTPUT_FILENAME = f"comparacion_absolutos_{UNIVERSIDAD_REFERENCIA}_{UNIVERSIDAD_2}_{UNIVERSIDAD_3}.png"
# =========================================================


# FUNCIONES


def cargar_columnas_universidad(file_path, sheet_name, universidad):
    """
    Carga desde un informe comparativo las columnas de área temática
    y el conteo de una universidad específica.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]

        cols_requeridas = ["Area tematica", f"{universidad}_count"]
        cols_faltantes = [c for c in cols_requeridas if c not in df.columns]
        if cols_faltantes:
            raise ValueError(f"Columnas faltantes en {file_path}: {cols_faltantes}")

        return df[cols_requeridas].copy()

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {file_path}")
        raise
    except ValueError as e:
        print(f"❌ Error: {e}")
        raise


def fusionar_informes(informe_1, informe_2, univ_ref, univ_2, univ_3, sheet_name):
    """
    Toma 2 informes comparativos y fusiona sus hojas de áreas temáticas
    en un único DataFrame con las 3 universidades.
    La universidad de referencia se toma solo una vez del primer informe.
    """
    print(f"📂 Cargando informe 1: {univ_ref} vs {univ_2}...")
    df1 = pd.read_excel(informe_1, sheet_name=sheet_name)
    df1.columns = [c.strip() for c in df1.columns]

    cols_df1 = ["Area tematica", f"{univ_ref}_count", f"{univ_2}_count"]
    cols_faltantes = [c for c in cols_df1 if c not in df1.columns]
    if cols_faltantes:
        raise ValueError(f"Columnas faltantes en informe 1: {cols_faltantes}")
    df1 = df1[cols_df1].copy()

    print(f"📂 Cargando informe 2: {univ_ref} vs {univ_3}...")
    df2 = cargar_columnas_universidad(informe_2, sheet_name, univ_3)

    print(f"\n🔗 Fusionando datos...")
    merged = df1.merge(df2, on="Area tematica", how="inner")

    print(f"✅ Fusión completada: {len(merged)} áreas temáticas en común")
    return merged


def filtrar_y_seleccionar(df, universidades, min_count, top_n):
    """
    Filtra las áreas donde todas las universidades superan el mínimo absoluto
    y selecciona las top N por promedio de papers entre las universidades.
    """
    mask = pd.Series([True] * len(df), index=df.index)
    for u in universidades:
        mask &= (df[f"{u}_count"] >= min_count)
    df_filtrado = df[mask].copy()
    print(f"✅ Áreas que cumplen criterios mínimos: {len(df_filtrado)}")

    df_filtrado["Promedio_general_count"] = df_filtrado[[f"{u}_count" for u in universidades]].mean(axis=1)
    top = df_filtrado.sort_values(by="Promedio_general_count", ascending=False).head(top_n).reset_index(drop=True)
    print(f"✅ Top {top_n} áreas seleccionadas")
    return top


def graficar_absolutos(df, universidades, output_filename):
    """
    Genera un gráfico de barras agrupadas con cantidades absolutas de papers.
    """
    colores_disponibles = ["steelblue", "goldenrod", "seagreen", "tomato"]
    colores = {u: colores_disponibles[i] for i, u in enumerate(universidades)}

    n = len(universidades)
    ancho = 0.8 / n
    offsets = np.linspace(-(n-1)/2 * ancho, (n-1)/2 * ancho, n)
    x = np.arange(len(df))

    fig, ax = plt.subplots(figsize=(14, 8))

    for i, u in enumerate(universidades):
        ax.bar(x + offsets[i], df[f"{u}_count"], ancho, label=u, color=colores[u])

    ax.set_xticks(x)
    ax.set_xticklabels(df["Area tematica"], rotation=90)
    ax.set_ylabel("Cantidad total de papers", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Comparación directa: top {len(df)} áreas con mayor producción\n({', '.join(universidades)})",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.legend()
    ax.grid(axis="y", alpha=0.2)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    print(f"✅ Gráfico guardado en: {output_filename}")
    plt.show()


# EJECUCIÓN PRINCIPAL


if __name__ == "__main__":
    try:
        universidades = [UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_2, UNIVERSIDAD_3]

        # Paso 1: Fusionar los 2 informes
        df = fusionar_informes(
            INFORME_1, INFORME_2,
            UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_2, UNIVERSIDAD_3,
            SHEET_NAME
        )

        # Paso 2: Filtrar y seleccionar top N áreas
        print(f"\n🔍 Filtrando y seleccionando top {TOP_N} áreas...")
        df = filtrar_y_seleccionar(df, universidades, MIN_COUNT, TOP_N)

        # Paso 3: Graficar
        print(f"\n📈 Generando gráfico de volumen absoluto...")
        graficar_absolutos(df, universidades, OUTPUT_FILENAME)

        print("\n✨ ¡Análisis completado exitosamente!")

    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        raise
