import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Nombre de la primera universidad (referencia)
UNIVERSIDAD_REFERENCIA = "UBA"

# Nombre de la segunda universidad (para comparar contra la referencia)
UNIVERSIDAD_COMPARACION = "UNIVERSIDAD_2"

# Ruta completa del archivo Excel generado por el script comparativo
file_path = r"C:\ruta\del\archivo\informe_comparativo.xlsx"

# Nombre exacto de la hoja que contiene los datos de áreas temáticas
sheet_name = "Áreas temáticas"

# Umbral mínimo: papers por cada 1000 en ambas universidades
min_per_1000 = 9

# Umbral mínimo: cantidad total de papers en ambas universidades
min_count = 50

# Cantidad de áreas a seleccionar (las más similares)
top_n_areas = 20

# Nombre del archivo de salida
output_filename = "similitud_areas.png"

# Diccionario de ajustes manuales de etiquetas (opcional)
# Formato: {"Nombre del área": (desplazamiento_x, desplazamiento_y)}
# Dejar vacío {} si no necesitas ajustes
ajustes_etiquetas = {
    # "Area ejemplo": (-5, 0),
    # "Otra area": (4, 2),
}

def cargar_datos(file_path, sheet_name, universidad_ref, universidad_comp):
    """Carga los datos del Excel y valida que existan las columnas necesarias"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.columns = [c.strip() for c in df.columns]
        
        # Validar que existan las columnas requeridas
        cols_requeridas = [
            "Area tematica",
            f"{universidad_ref}_count",
            f"{universidad_ref}_per_1000",
            f"{universidad_comp}_count",
            f"{universidad_comp}_per_1000"
        ]
        
        cols_faltantes = [col for col in cols_requeridas if col not in df.columns]
        if cols_faltantes:
            raise ValueError(f"Columnas faltantes en el Excel: {cols_faltantes}")
        
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {file_path}")
        raise
    except ValueError as e:
        print(f"❌ Error: {e}")
        raise

def filtrar_datos(df, universidad_ref, universidad_comp, min_per_1000, min_count):
    """Filtra las áreas que cumplen con los criterios mínimos en ambas universidades"""
    mask = (
        (df[f'{universidad_ref}_per_1000'] >= min_per_1000) &
        (df[f'{universidad_comp}_per_1000'] >= min_per_1000) &
        (df[f'{universidad_ref}_count'] >= min_count) &
        (df[f'{universidad_comp}_count'] >= min_count)
    )
    return df[mask].copy()

def calcular_similitud(df, universidad_ref, universidad_comp):
    """Calcula la diferencia entre universidades y la similitud"""
    df['Difference'] = df[f'{universidad_ref}_per_1000'] - df[f'{universidad_comp}_per_1000']
    df['AbsDiff'] = df['Difference'].abs()
    return df

def seleccionar_areas_similares(df, top_n):
    """Selecciona las áreas más similares (menor diferencia absoluta)"""
    return df.nsmallest(top_n, 'AbsDiff')

def plot_similitudes(df, universidad_ref, universidad_comp, title, filename, 
                     sort_by="x", ajustes=None):
    """
    Genera un gráfico scatter con abanicos de etiquetas mostrando similitudes.
    
    Parámetros:
    - df: DataFrame con los datos
    - universidad_ref: Nombre de la universidad de referencia
    - universidad_comp: Nombre de la universidad de comparación
    - title: Título del gráfico
    - filename: Nombre del archivo para guardar
    - sort_by: "x" (por UBA), "y" (por otra universidad) o "none"
    - ajustes: Dict con ajustes manuales de etiquetas
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Calcular tamaños de puntos según cantidad total de papers
    total_papers = df[f'{universidad_ref}_count'] + df[f'{universidad_comp}_count']
    sizes = 10 + 60 * (total_papers - total_papers.min()) / (total_papers.max() - total_papers.min())
    
    # Color según quién tiene más papers en esa área
    colors = ['blue' if diff >= 0 else 'red' for diff in df['Difference']]
    
    # Scatter plot
    ax.scatter(df[f'{universidad_ref}_per_1000'], df[f'{universidad_comp}_per_1000'],
               s=sizes, alpha=0.7, c=colors, edgecolor='black', linewidth=0.5)
    
    # Línea de igualdad
    max_val = max(df[f'{universidad_ref}_per_1000'].max(), 
                  df[f'{universidad_comp}_per_1000'].max()) * 1.1
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, linewidth=1)
    ax.text(max_val*0.55, max_val*0.5, f"Línea de igualdad ({universidad_ref} = {universidad_comp})",
            fontsize=10, color='gray', rotation=38, alpha=0.8)
    
    # Separar por color
    df_azul = df[df['Difference'] >= 0].copy()
    df_rojo = df[df['Difference'] < 0].copy()

    base_offset = max_val * 0.25
    coords = []

    def ordenar(df_group):
        if sort_by == "x":
            return df_group.sort_values(f'{universidad_ref}_per_1000').reset_index(drop=True)
        elif sort_by == "y":
            return df_group.sort_values(f'{universidad_comp}_per_1000').reset_index(drop=True)
        else:
            return df_group.reset_index(drop=True)

    def spread_dinamico(n, spread_base=100, spread_max=160):
        if n <= 1:
            return 0
        spread = spread_base + (n-2)*10
        return min(spread, spread_max)

    def colocar_etiquetas(df_group, angles, color, facecolor):
        for i, row in df_group.iterrows():
            x = row[f'{universidad_ref}_per_1000']
            y = row[f'{universidad_comp}_per_1000']
            
            angle = np.deg2rad(angles[i])
            label_x = x + base_offset * np.cos(angle)
            label_y = y + base_offset * np.sin(angle)
            label_y += (i % 2) * 0.03 * max_val

            # Aplicar ajustes manuales si existen
            if ajustes and row['Area tematica'] in ajustes:
                dx, dy = ajustes[row['Area tematica']]
                label_x += dx
                label_y += dy

            ax.text(label_x, label_y, str(row['Area tematica']),
                    fontsize=9, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=facecolor,
                              edgecolor=color, linewidth=0.8))
            coords.append((x, y, label_x, label_y, color))

    # Abanico azul (área donde universidad_ref tiene más papers)
    if len(df_azul) > 0:
        df_azul = ordenar(df_azul)
        spread = spread_dinamico(len(df_azul))
        angles_azul = np.linspace(270 - spread/2, 270 + spread/2, len(df_azul))
        colocar_etiquetas(df_azul, angles_azul, 'blue', (0.85, 0.85, 1.0))

    # Abanico rojo (área donde universidad_comp tiene más papers)
    if len(df_rojo) > 0:
        df_rojo = ordenar(df_rojo).iloc[::-1].reset_index(drop=True)
        spread = spread_dinamico(len(df_rojo))
        angles_rojo = np.linspace(90 - spread/2, 90 + spread/2, len(df_rojo))
        colocar_etiquetas(df_rojo, angles_rojo, 'red', (1.0, 0.85, 0.85))

    # Líneas conectando puntos con etiquetas
    for x, y, label_x, label_y, color in coords:
        ax.plot([x, label_x], [y, label_y], color=color, lw=1.2, alpha=0.9)

    # Ajuste dinámico de límites
    if coords:
        all_x = [x for x, _, _, _, _ in coords] + [lx for _, _, lx, _, _ in coords]
        all_y = [y for _, y, _, _, _ in coords] + [ly for _, _, _, ly, _ in coords]
        ax.set_xlim(min(all_x) - 0.2*max_val, max(all_x) + 0.2*max_val)
        ax.set_ylim(min(all_y) - 0.2*max_val, max(all_y) + 0.2*max_val)
    
    ax.set_aspect('equal', adjustable='datalim')
    
    ax.set_xlabel(f"{universidad_ref} (papers por cada 1000)", fontsize=12, fontweight='bold')
    ax.set_ylabel(f"{universidad_comp} (papers por cada 1000)", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(alpha=0.2)
    
    # Leyenda
    legend_elements = [
        Patch(facecolor='blue', alpha=0.7, label=f'{universidad_ref} > {universidad_comp}'),
        Patch(facecolor='red', alpha=0.7, label=f'{universidad_comp} > {universidad_ref}'),
        plt.Line2D([0], [0], linestyle='--', color='black', label='Línea de igualdad')
    ]
    ax.legend(handles=legend_elements, loc='upper left', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {filename}")
    plt.show()

# EJECUCIÓN PRINCIPAL


if __name__ == "__main__":
    try:
        print(f"📊 Cargando datos de {file_path}...")
        df = cargar_datos(file_path, sheet_name, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)
        print(f"✅ Datos cargados: {len(df)} áreas temáticas")
        
        print(f"\n🔍 Filtrando áreas con criterios mínimos...")
        df_filtrado = filtrar_datos(df, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION, 
                                    min_per_1000, min_count)
        print(f"✅ Áreas que cumplen criterios: {len(df_filtrado)}")
        
        print(f"\n📐 Calculando similitud...")
        df_filtrado = calcular_similitud(df_filtrado, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)
        
        print(f"\n🎯 Seleccionando las {top_n_areas} áreas más similares...")
        areas_similares = seleccionar_areas_similares(df_filtrado, top_n_areas)
        print(f"✅ Áreas seleccionadas: {len(areas_similares)}")
        
        print(f"\n📈 Generando gráfico...")
        title = f"Áreas con mayor similitud entre {UNIVERSIDAD_REFERENCIA} y {UNIVERSIDAD_COMPARACION}"
        plot_similitudes(
            areas_similares,
            UNIVERSIDAD_REFERENCIA,
            UNIVERSIDAD_COMPARACION,
            title,
            output_filename,
            sort_by="x",
            ajustes=ajustes_etiquetas
        )
        
        print("\n✨ ¡Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        raise
