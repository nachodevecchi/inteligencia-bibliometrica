import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================== CONFIGURACIÓN =====================
# Rutas de los 3 informes comparativos (generados por el notebook 01)
INFORME_1 = r"ruta del archivo"
INFORME_2 = r"ruta del archivo"

# Nombre de la universidad de referencia (la que aparece en todos los informes)
UNIVERSIDAD_REFERENCIA = "UBA"

# Nombres de las otras 3 universidades (en el mismo orden que los informes)
UNIVERSIDAD_2 = "UNSAM"
UNIVERSIDAD_3 = "LITORAL"

# Nombre de la hoja con los datos de áreas temáticas
SHEET_NAME = "Áreas temáticas"

# Filtros
MIN_COUNT = 50       # mínimo absoluto de papers por área
MIN_PER_1000 = 10    # mínimo relativo (papers por cada 1000 de producción total)
TOP_N = 20           # cantidad de áreas a mostrar

# Nombre del archivo de salida
OUTPUT_FILENAME = f"densidad_relativa_{UNIVERSIDAD_REFERENCIA}_{UNIVERSIDAD_2}_{UNIVERSIDAD_3}.png"
# =========================================================


# FUNCIONES


def cargar_columnas_universidad(file_path, sheet_name, universidad):
    """
    Carga desde un informe comparativo las columnas de área temática
    y los datos de una universidad específica.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]

        cols_requeridas = [
            "Area tematica",
            f"{universidad}_count",
            f"{universidad}_per_1000"
        ]

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


def fusionar_informes(informe_1, informe_2,
                      univ_ref, univ_2, univ_3, sheet_name):
    """
    Toma 3 informes comparativos y fusiona sus hojas de áreas temáticas
    en un único DataFrame con todas las universidades.
    La universidad de referencia se toma solo una vez del primer informe.
    """
    print(f"📂 Cargando informe 1: {univ_ref} vs {univ_2}...")
    df1 = pd.read_excel(informe_1, sheet_name=sheet_name)
    df1.columns = [c.strip() for c in df1.columns]
    # Del primer informe tomamos la referencia + universidad 2
    cols_df1 = ["Area tematica",
                f"{univ_ref}_count", f"{univ_ref}_per_1000",
                f"{univ_2}_count", f"{univ_2}_per_1000"]
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


def filtrar_areas(df, universidades, min_count, min_per_1000):
    """
    Filtra las áreas donde todas las universidades superan
    los umbrales mínimos de producción.
    """
    mask = pd.Series([True] * len(df), index=df.index)
    for u in universidades:
        mask &= (df[f"{u}_count"] >= min_count)
        mask &= (df[f"{u}_per_1000"] >= min_per_1000)
    resultado = df[mask].copy()
    print(f"✅ Áreas que cumplen criterios mínimos: {len(resultado)}")
    return resultado


def seleccionar_top_areas(df, universidades, top_n):
    """
    Selecciona las top N áreas con mayor producción combinada.
    """
    df["Total_combinado"] = sum(df[f"{u}_count"] for u in universidades)
    top = df.sort_values(by="Total_combinado", ascending=False).head(top_n).reset_index(drop=True)
    print(f"✅ Top {top_n} áreas seleccionadas")
    return top


def calcular_densidad(df, universidades, totales):
    """
    Calcula la densidad relativa (%) de cada universidad por área.
    totales: dict con {nombre_universidad: total_papers}
    """
    for u in universidades:
        if u not in totales:
            raise ValueError(f"Falta el total de papers para {u} en el diccionario 'totales'")
        df[f"{u}_dens"] = df[f"{u}_count"] / totales[u] * 100
    return df


def etiquetar_barras(ax, barras_por_uni, colores):
    """
    Etiqueta cada barra según su jerarquía de altura dentro del grupo.
    La barra más alta recibe la etiqueta arriba, la del medio adentro,
    la más baja adentro abajo.
    """
    n_areas = len(list(barras_por_uni.values())[0])

    for i in range(n_areas):
        alturas = {u: barras[i].get_height() for u, barras in barras_por_uni.items()}
        ordenadas = sorted(alturas.items(), key=lambda x: x[1], reverse=True)
        posiciones = {
            ordenadas[0][0]: "top",
            ordenadas[1][0]: "middle",
            ordenadas[2][0]: "bottom"
        }

        for u, barras in barras_por_uni.items():
            barra = barras[i]
            h = barra.get_height()
            x_pos = barra.get_x() + barra.get_width() / 2
            texto = f"{h:.1f}%"
            color_fondo = colores[u]["fondo"]
            color_texto = colores[u]["texto"]

            if posiciones[u] == "top":
                y_pos = h + 0.3
                va = "bottom"
            elif posiciones[u] == "middle":
                y_pos = h / 2
                va = "center"
            else:
                y_pos = h * 0.1
                va = "bottom"

            ax.text(x_pos, y_pos, texto,
                    ha="center", va=va, color=color_texto,
                    fontsize=9, fontweight="bold",
                    bbox=dict(facecolor=color_fondo, alpha=0.6,
                              edgecolor='none', boxstyle='round,pad=0.15'))


def graficar(df, universidades, titulo, output_filename):
    """
    Genera el gráfico de barras agrupadas con densidad relativa.
    """
    colores_disponibles = [
        {"barra": "steelblue",  "fondo": "steelblue",  "texto": "white"},
        {"barra": "goldenrod",  "fondo": "wheat",       "texto": "black"},
        {"barra": "seagreen",   "fondo": "seagreen",    "texto": "white"},
        {"barra": "tomato",     "fondo": "tomato",      "texto": "white"},
    ]

    n = len(universidades)
    colores = {u: colores_disponibles[i] for i, u in enumerate(universidades)}

    x = np.arange(len(df))
    ancho = 0.8 / n  # ancho dinámico según cantidad de universidades
    offsets = np.linspace(-(n-1)/2 * ancho, (n-1)/2 * ancho, n)

    fig, ax = plt.subplots(figsize=(14, 8))
    barras_por_uni = {}

    for i, u in enumerate(universidades):
        barras = ax.bar(x + offsets[i], df[f"{u}_dens"], ancho,
                        label=u, color=colores[u]["barra"])
        barras_por_uni[u] = barras

    etiquetar_barras(ax, barras_por_uni, colores)

    max_val = max(df[f"{u}_dens"].max() for u in universidades)
    ax.set_ylim(0, max_val * 1.15)
    ax.set_xticks(x)
    ax.set_xticklabels(df["Area tematica"], rotation=90)
    ax.set_ylabel("Densidad relativa (%)", fontsize=12, fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=20)
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

        # Paso 1: Fusionar los 3 informes
        df = fusionar_informes(
            INFORME_1, INFORME_2,
            UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_2, UNIVERSIDAD_3,
            SHEET_NAME
        )

        # Paso 2: Filtrar áreas con producción significativa
        print(f"\n🔍 Filtrando áreas con criterios mínimos...")
        df = filtrar_areas(df, universidades, MIN_COUNT, MIN_PER_1000)

        # Paso 3: Seleccionar top N áreas
        print(f"\n📊 Seleccionando top {TOP_N} áreas...")
        df = seleccionar_top_areas(df, universidades, TOP_N)

        # Paso 4: Calcular densidad relativa
        # ⚠️ Completá con el total real de papers de cada universidad
        totales = {
            UNIVERSIDAD_REFERENCIA: 10000,   # ← reemplazá con el total real
            UNIVERSIDAD_2: 3000,             # ← reemplazá con el total real
            UNIVERSIDAD_3: 4000,             # ← reemplazá con el total real
            
        }
        print(f"\n📐 Calculando densidad relativa...")
        df = calcular_densidad(df, universidades, totales)

        # Paso 5: Graficar
        print(f"\n📈 Generando gráfico...")
        titulo = f"Densidad relativa de papers: {' vs '.join(universidades)}"
        graficar(df, universidades, titulo, OUTPUT_FILENAME)

        print("\n✨ ¡Análisis completado exitosamente!")

    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        raise
