import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
from scipy.spatial import KDTree
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

# Cantidad de áreas extremas a seleccionar (fortalezas y debilidades)
# El script seleccionará top_n_extremos de cada universidad
top_n_extremos = 10

# Cantidad de áreas similares a destacar
top_n_similares = 20

# Margen adicional a la derecha del gráfico (para ajustar etiquetas)
margen_derecho_extra = 15

# Nombre del archivo de salida
output_filename = "fortalezas_debilidades.png"

# Diccionario de ajustes manuales de etiquetas (opcional)
# Formato: {"Nombre del área": (desplazamiento_x, desplazamiento_y)}
# Dejar vacío {} si no necesitas ajustes
ajustes_etiquetas = {
    # "Area ejemplo": (0, -14),
    # "Otra area": (-30, +20),
}


# FUNCIONES


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

def calcular_diferencia(df, universidad_ref, universidad_comp):
    """Calcula la diferencia entre universidades"""
    df['Difference'] = df[f'{universidad_ref}_per_1000'] - df[f'{universidad_comp}_per_1000']
    df['AbsDiff'] = df['Difference'].abs()
    return df

def seleccionar_extremos(df, universidad_ref, universidad_comp, top_n):
    """Selecciona las áreas donde cada universidad tiene mayor fortaleza (mayor diferencia)"""
    # Áreas donde universidad_ref domina
    top_ref = df.nlargest(top_n, 'Difference')
    # Áreas donde universidad_comp domina
    top_comp = df.nsmallest(top_n, 'Difference')
    
    return pd.concat([top_ref, top_comp])

def seleccionar_similares(df, top_n):
    """Selecciona las áreas más similares (menor diferencia absoluta)"""
    return df.nsmallest(top_n, 'AbsDiff')

def plot_fortalezas_debilidades(df_extremos, df_similares, universidad_ref, universidad_comp, 
                                title, filename, margen_extra, ajustes=None):
    """
    Genera un gráfico scatter mostrando fortalezas y debilidades de ambas universidades.
    
    Parámetros:
    - df_extremos: DataFrame con áreas extremas (mayor diferencia)
    - df_similares: DataFrame con áreas similares
    - universidad_ref: Nombre de la universidad de referencia
    - universidad_comp: Nombre de la universidad de comparación
    - title: Título del gráfico
    - filename: Nombre del archivo para guardar
    - margen_extra: Margen adicional a la derecha
    - ajustes: Dict con ajustes manuales de etiquetas
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Calcular tamaños de puntos según cantidad total de papers
    total_papers = df_extremos[f'{universidad_ref}_count'] + df_extremos[f'{universidad_comp}_count']
    sizes = 80 + 500 * (total_papers - total_papers.min()) / (total_papers.max() - total_papers.min())
    
    # Color según quién tiene más papers en esa área
    point_colors = np.where(df_extremos['Difference'] >= 0, 'blue', 'red')
    
    # Scatter de áreas extremas
    ax.scatter(df_extremos[f'{universidad_ref}_per_1000'], 
               df_extremos[f'{universidad_comp}_per_1000'],
               s=sizes, alpha=0.7, c=point_colors, edgecolor='black', linewidth=0.5)
    
    # Scatter de áreas similares
    ax.scatter(df_similares[f'{universidad_ref}_per_1000'], 
               df_similares[f'{universidad_comp}_per_1000'],
               s=60, alpha=0.7, c='green', edgecolor='black', linewidth=0.5)
    
    # Línea de igualdad
    max_val = max(df_extremos[f'{universidad_ref}_per_1000'].max(), 
                  df_extremos[f'{universidad_comp}_per_1000'].max()) * 1.1
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, linewidth=1)

    # Texto de la línea de igualdad
    x_text = max_val * 0.6
    y_text = x_text
    ax.text(x_text, y_text + 10, f"Línea de igualdad ({universidad_ref} = {universidad_comp})",
            fontsize=10, color='gray', rotation=30,
            rotation_mode='anchor', ha='left', va='bottom', alpha=0.8)
    
    # Preparar etiquetas
    texts, coords, colors_for_labels = [], [], []
    points = df_extremos[[f'{universidad_ref}_per_1000', f'{universidad_comp}_per_1000']].values
    tree = KDTree(points)
    
    # Áreas que siempre se deben etiquetar (las extremas)
    always_label = set(df_extremos['Area tematica'])

    for _, row in df_extremos.iterrows():
        label = row['Area tematica']
        x_val = row[f'{universidad_ref}_per_1000']
        y_val = row[f'{universidad_comp}_per_1000']
        
        distances, _ = tree.query([x_val, y_val], k=3)
        avg_distance = np.mean(distances[1:]) if len(distances) > 1 else 0.0
        abs_diff = abs(row['Difference'])
        is_extreme_diff = abs_diff > df_extremos['AbsDiff'].quantile(0.7)
        
        # Mostrar etiqueta si es extrema o está alejada de otros puntos
        if (label in always_label) or (avg_distance > 2 or is_extreme_diff):
            color = 'blue' if row['Difference'] >= 0 else 'red'
            facecolor = (0.85, 0.85, 1.0) if color == 'blue' else (1.0, 0.85, 0.85)
            text = ax.text(x_val, y_val, label, fontsize=9,
                           bbox=dict(boxstyle="round,pad=0.3", facecolor=facecolor,
                                     edgecolor=color, linewidth=0.8))
            texts.append(text)
            coords.append((x_val, y_val))
            colors_for_labels.append(color)
    
    # Ajuste automático de etiquetas
    adjust_text(texts, ax=ax, arrowprops=None,
                expand_points=(1.2, 1.8), expand_text=(1.1, 1.5),
                force_text=(0.8, 1.2), only_move={'points': 'xy', 'text': 'xy'},
                lim=1000, precision=0.001)
    
    # Aplicar ajustes manuales si existen
    if ajustes:
        for text in texts:
            label = text.get_text()
            if label in ajustes:
                dx, dy = ajustes[label]
                x, y = text.get_position()
                text.set_position((x + dx, y + dy))
    
    # Conectores entre puntos y etiquetas
    for text, (x, y), color in zip(texts, coords, colors_for_labels):
        box_x, box_y = text.get_position()
        dx, dy = box_x - x, box_y - y
        if dx == 0 and dy == 0:
            continue
        ax.plot([x, box_x], [y, box_y], color=color, lw=1.0, alpha=0.9)
    
    # Expandir límites según cajas de texto
    renderer = fig.canvas.get_renderer()
    all_extents = [text.get_window_extent(renderer=renderer).transformed(ax.transData.inverted()) 
                   for text in texts]
    if all_extents:
        min_x = min(b.x0 for b in all_extents)
        max_x = max(b.x1 for b in all_extents)
        min_y = min(b.y0 for b in all_extents)
        max_y = max(b.y1 for b in all_extents)
        ax.set_xlim(min_x - 10, max(max_val, max_x + margen_extra))
        ax.set_ylim(min_y - 30, max(max_val, max_y + 5))
    
    ax.set_xlabel(f"{universidad_ref} (papers por cada 1000)", fontsize=12, fontweight='bold')
    ax.set_ylabel(f"{universidad_comp} (papers por cada 1000)", fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(alpha=0.2)
    
    # Leyenda
    legend_elements = [
        Patch(facecolor='blue', alpha=0.7, label=f'{universidad_ref} > {universidad_comp}'),
        Patch(facecolor='red', alpha=0.7, label=f'{universidad_comp} > {universidad_ref}'),
        Patch(facecolor='green', alpha=0.7, label='Áreas con mayor similitud de producción'),
        plt.Line2D([0], [0], linestyle='--', color='black', label='Línea de igualdad')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.08),
              ncol=2, framealpha=0.9)
    
    fig.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.15)
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
        
        print(f"\n📐 Calculando diferencias...")
        df_filtrado = calcular_diferencia(df_filtrado, UNIVERSIDAD_REFERENCIA, UNIVERSIDAD_COMPARACION)
        
        print(f"\n💪 Seleccionando fortalezas y debilidades...")
        df_extremos = seleccionar_extremos(df_filtrado, UNIVERSIDAD_REFERENCIA, 
                                          UNIVERSIDAD_COMPARACION, top_n_extremos)
        print(f"✅ Áreas extremas seleccionadas: {len(df_extremos)}")
        print(f"   - Fortalezas {UNIVERSIDAD_REFERENCIA}: {len(df_extremos[df_extremos['Difference'] >= 0])}")
        print(f"   - Fortalezas {UNIVERSIDAD_COMPARACION}: {len(df_extremos[df_extremos['Difference'] < 0])}")
        
        print(f"\n🎯 Seleccionando áreas similares...")
        df_similares = seleccionar_similares(df_filtrado, top_n_similares)
        print(f"✅ Áreas similares seleccionadas: {len(df_similares)}")
        
        print(f"\n📈 Generando gráfico...")
        title = f"Fortalezas y Debilidades: {UNIVERSIDAD_REFERENCIA} vs {UNIVERSIDAD_COMPARACION}"
        plot_fortalezas_debilidades(
            df_extremos,
            df_similares,
            UNIVERSIDAD_REFERENCIA,
            UNIVERSIDAD_COMPARACION,
            title,
            output_filename,
            margen_derecho_extra,
            ajustes=ajustes_etiquetas
        )
        
        print("\n✨ ¡Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        raise
