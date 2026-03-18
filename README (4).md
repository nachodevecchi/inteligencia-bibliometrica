# Inteligencia Bibliométrica

Herramienta desarrollada por la Oficina de Vinculación Tecnológica de la FCEN-UBA para analizar la producción científica universitaria a partir de datos exportados de Scopus.

El repositorio contiene tres módulos. El primero es un **prerequisito** para los otros dos:

- **Enriquecimiento de la base** — limpia y enriquece el Excel exportado de Scopus con clasificaciones ASJC, grupos temáticos y campos de estudio específicos
- **Comparador de producción científica** — compara la producción entre universidades
- **Mapeo de verticales industriales** — identifica las fortalezas de investigación de una facultad y las asocia a sectores industriales

---

## Requisitos

- Python 3.8 o superior
- Jupyter Notebook instalado
- Las librerías listadas en `requirements.txt`

Si no tenés las librerías instaladas, abrí una terminal y ejecutá:

```bash
pip install -r requirements.txt
```

---

## Módulo 0 — Enriquecimiento de la base (PREREQUISITO)

> ⚠️ **Este módulo debe ejecutarse antes que cualquier otro.** Los módulos 1 y 2 dependen de las columnas que genera este paso.

### ¿Qué hace?

Toma el Excel exportado de Scopus y le agrega cuatro columnas nuevas cruzando los títulos de revistas (`Source title`) con el glosario oficial de Scopus (`ext_list_Feb_2026.xlsx`):

| Columna generada | Descripción |
|---|---|
| `All Science Journal Classification Codes (ASJC)` | Códigos numéricos ASJC de la revista, separados por `;` |
| `Campos de Estudio Específicos` | Nombres correspondientes a esos códigos (ej: `Ecology; Medicine`) |
| `Grupos Padre` | Categorías de alto nivel de Scopus: Life Sciences, Social Sciences, Physical Sciences, Health Sciences — separadas por `;` |
| `Subgrupos` | Áreas disciplinares intermedias de Scopus (ej: `2700 Medicine`, `1105 Ecology`) — separadas por `;` |

### ¿De dónde vienen estas clasificaciones?

Scopus clasifica cada revista científica utilizando el sistema **ASJC (All Science Journal Classification)**. Este sistema tiene tres niveles:

1. **Grupos Padre** (4 categorías): Life Sciences, Social Sciences, Physical Sciences, Health Sciences
2. **Subgrupos** (26 áreas): Medicine, Engineering, Environmental Science, etc.
3. **Campos específicos** (cientos de códigos): cada código numérico ASJC representa un campo de estudio puntual, como `1105 Ecology` o `2728 Neurology (clinical)`

El glosario oficial (`ext_list_Feb_2026.xlsx`) es el archivo publicado por Scopus que contiene el listado completo de revistas con sus códigos y clasificaciones asignadas.

### Archivos necesarios

| Archivo | Descripción | Dónde conseguirlo |
|---|---|---|
| `BASE DE PAPERS.xlsx` | Base de papers exportada de Scopus segun universidad | Exportá desde Scopus |
| `ext_list_Feb_2026.xlsx` | Glosario oficial de Scopus con clasificaciones ASJC | Descargable desde el sitio de Scopus |

### Cómo usar el enriquecimiento

#### Paso 1 — Abrir el notebook

Abrí Jupyter Notebook y navegá hasta `enriquecimiento/`. Abrí el archivo `enriquecer_papers_scopus.ipynb`.

#### Paso 2 — Configurar las rutas

Al principio del notebook encontrás la sección de rutas. Editá las variables con las rutas a tus archivos:

```python
PAPERS_PATH  = r"C:\Users\...\BASE NUEVA SIN FILAS VACIAS.xlsx"
SCOPUS_PATH  = r"C:\Users\...\ext_list_Feb_2026.xlsx"
OUTPUT_PATH  = r"C:\Users\...\BASE ENRIQUECIDA.xlsx"
```

#### Paso 3 — Ejecutar todas las celdas en orden

El notebook realiza automáticamente:

1. Limpieza de nombres de columna del glosario (elimina saltos de línea y espacios múltiples)
2. Detección y resolución automática de columnas aunque sus nombres difieran levemente
3. Cruce por título de revista (normalizado, sin distinción de mayúsculas)
4. Generación de las cuatro columnas nuevas
5. Reporte de cobertura (% de papers que encontraron match) y lista de revistas sin match para revisión

#### Paso 4 — Verificar cobertura y exportar

Antes de exportar, revisá las revistas sin match que lista el notebook. Pueden deberse a diferencias de nombre, abreviaturas o revistas no indexadas en Scopus. Una vez conforme, ejecutá la celda de exportación.

> 💡 El archivo resultante (`BASE ENRIQUECIDA.xlsx`) es el que usarán los módulos 1 y 2.

---

## Módulo 1 — Comparador de Producción Científica

### ¿Qué hace?

A partir de bases de datos exportadas de Scopus (enriquecidas con el Módulo 0), genera informes comparativos en Excel y gráficos de análisis entre universidades. Permite visualizar fortalezas, debilidades, similitudes y volumen de producción científica por campos de estudio, tanto en comparaciones de dos universidades como de tres.

### Datos de ejemplo

Si querés probar el módulo sin tener datos reales de Scopus, la carpeta `data/sample/` contiene archivos de ejemplo con datos sintéticos para las siguientes universidades:

| Archivo | Universidad |
|---|---|
| `sample_UBA.xlsx` | Universidad de Buenos Aires |
| `sample_CAMPINAS.xlsx` | Universidad de Campinas |
| `sample_UNAL.xlsx` | Universidad Nacional de Colombia |
| `sample_UCHILE.xlsx` | Universidad de Chile |
| `sample_TEC.xlsx` | TEC Monterrey |
| `sample_JAVERIANA.xlsx` | Pontificia Universidad Javeriana |
| `sample_SAO_PAULO.xlsx` | Universidad de São Paulo |

> ⚠️ Estos archivos contienen **datos inventados** y tienen como único propósito permitir probar el funcionamiento de los scripts. Los resultados no representan la producción científica real de ninguna universidad.

Para usarlos, simplemente apuntá las rutas de los notebooks a estos archivos en lugar de los reales.

### Cómo usar el comparador con datos reales

#### Paso 1 — Conseguir los datos

Los datos de cada universidad son archivos Excel exportados directamente desde [Scopus](https://www.scopus.com) y **enriquecidos con el Módulo 0**. Para exportarlos desde Scopus:

1. Buscá la producción de la universidad en Scopus
2. Seleccioná todos los resultados
3. Exportá como CSV y pasalo a Excel (`.xlsx`)
4. Guardá cada archivo en la carpeta `data/raw/` con un nombre claro, por ejemplo `UBA.xlsx`, `CAMPINAS.xlsx`, etc.
5. Ejecutá el Módulo 0 sobre cada archivo antes de continuar

> ⚠️ Los archivos de datos reales **no están incluidos** en el repositorio.

#### Paso 2 — Abrir Jupyter Notebook

Abrí Jupyter Notebook y navegá hasta la carpeta `notebooks/`.

#### Paso 3 — Ejecutar los notebooks

El comparador tiene dos flujos de análisis. Cada análisis tiene una versión de **gráfico** y una versión de **tabla Excel**, que podés usar de forma independiente según lo que necesites.

##### Flujo A — Comparación entre dos universidades

Primero ejecutá el notebook 01, que genera el informe base. Luego podés usar los notebooks 02 y 03 en cualquier orden:

| Notebook | ¿Qué genera? |
|----------|--------------|
| `01_generar_informe.ipynb` | Informe Excel comparativo entre dos universidades (insumo para el resto) |
| `02_graficar_fortalezas.ipynb` | Gráfico de fortalezas y debilidades |
| `02b_tabla_fortalezas.ipynb` | Tabla Excel con los mismos datos del gráfico de fortalezas |
| `03_graficar_similitudes.ipynb` | Gráfico de áreas similares |
| `03b_tabla_similitudes.ipynb` | Tabla Excel con los mismos datos del gráfico de similitudes |

##### Flujo B — Comparación entre tres universidades

Antes de usar estos notebooks necesitás haber ejecutado el notebook 01 al menos dos veces (una por cada par de universidades a comparar):

| Notebook | ¿Qué genera? |
|----------|--------------|
| `04_comparacion_densidad_relativa.ipynb` | Gráfico de densidad relativa entre tres universidades |
| `04b_tabla_densidad_relativa.ipynb` | Tabla Excel con los mismos datos del gráfico de densidad relativa |
| `05_comparacion_volumen_absoluto.ipynb` | Gráfico de volumen absoluto entre tres universidades |
| `05b_tabla_volumen_absoluto.ipynb` | Tabla Excel con los mismos datos del gráfico de volumen absoluto |

#### Paso 4 — Configurar cada notebook

Al abrir cada notebook, vas a encontrar una sección de **CONFIGURACIÓN** al principio. Solo tenés que modificar esas variables:

**En el notebook 01:**
```python
universidad1_name = "UBA"
universidad2_name = "CAMPINAS"
universidad1_file = r"data/raw/UBA.xlsx"
universidad2_file = r"data/raw/CAMPINAS.xlsx"
```

**En los notebooks 02, 02b, 03 y 03b:**
```python
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_COMPARACION = "CAMPINAS"
file_path = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
```

> 🏷️ **Ajuste de etiquetas en los gráficos (opcional):** Los notebooks 02 y 03 tienen una variable llamada `ajustes_etiquetas` que permite correr manualmente las etiquetas del gráfico si algunas se superponen. Por defecto está vacía `{}` y el gráfico funciona igual. Si necesitás ajustar alguna etiqueta, podés indicar cuántos puntos moverla en el eje x e y:
> ```python
> ajustes_etiquetas = {
>     "Nombre del área": (0, -14),   # mueve la etiqueta 14 puntos hacia abajo
>     "Otra área": (-30, +20),       # mueve 30 hacia la izquierda y 20 hacia arriba
> }
> ```
> Esto es puramente estético y no afecta los datos.

**En los notebooks 04, 04b, 05 y 05b:**
```python
INFORME_1 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
INFORME_2 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNAL.xlsx"
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_2 = "CAMPINAS"
UNIVERSIDAD_3 = "UNAL"
```

> 💡 Los informes que usan los notebooks del Flujo B los encontrás en tu escritorio, generados por el notebook 01.

#### Paso 5 — ¿Dónde encuentro los resultados?

- Los **informes Excel** (notebooks 01, 02b, 03b, 04b y 05b) se guardan automáticamente en tu **escritorio**.
- Los **gráficos** (notebooks 02, 03, 04 y 05) se guardan como `.png` en la carpeta desde donde ejecutás Jupyter y también se muestran en el notebook.

---

## Módulo 2 — Mapeo de Verticales Industriales

### ¿Qué hace?

A partir de la base enriquecida con el Módulo 0, identifica las áreas de investigación según la clasificación ASJC de Scopus y las asocia a verticales industriales (sectores como Biotecnología & Salud, Energía & Cleantech, IT & IA, etc.). Genera un Excel con el análisis completo y gráficos de distribución y tendencia temporal.

El mapeo es **totalmente configurable**: cada usuario define qué vertical le asigna a cada área de Scopus según el perfil de su institución.

### Archivos necesarios

| Archivo | Descripción | Dónde conseguirlo |
|---|---|---|
| `ext_list_Feb_2026.xlsx` | Glosario ASJC oficial de Scopus | Descargable desde el sitio de Scopus |
| `BASE ENRIQUECIDA.xlsx` | Base generada por el Módulo 0 | Output del Módulo 0 |

### Cómo usar el mapeo con datos reales

#### Paso 1 — Asegurarse de tener la base enriquecida

Este módulo requiere que la base haya pasado por el **Módulo 0**. Las columnas `Subgrupos`, `Grupos Padre` y `Campos de Estudio Específicos` deben existir en el archivo de entrada.

#### Paso 2 — Abrir el notebook

Abrí Jupyter Notebook y navegá hasta `mapeo_verticales/`. Abrí el archivo `Mapeo_de_verticales_industriales.ipynb`.

#### Paso 3 — Configurar el notebook

Al principio del notebook vas a encontrar una celda de **CONFIGURACIÓN**. Editá estas variables antes de correr cualquier otra celda:

```python
# ══════════════════════════════════════════════════════
# CONFIGURACIÓN — editá estas variables antes de correr
# ══════════════════════════════════════════════════════
RUTA_GLOSARIO        = r'ruta\a\tu\ext_list_Feb_2026.xlsx'
RUTA_DATOS           = r'ruta\a\tu\BASE ENRIQUECIDA.xlsx'
RUTA_SALIDA          = r'ruta\donde\guardar\resultado.xlsx'
NOMBRE_INSTITUCION   = 'FCEN-UBA'   # aparece en los títulos de los gráficos
```

#### Paso 4 — Adaptar el mapeo a tu institución

En la celda de mapeo vas a encontrar dos diccionarios claramente marcados como **editables**:

- `MAPEO_GRUPOS_PADRE`: asigna una vertical a cada uno de los 26 grupos temáticos de Scopus
- `MAPEO_SUBGRUPOS_ESPECIFICOS`: refinamientos para subgrupos puntuales que merecen una vertical diferente a la de su grupo padre

El notebook incluye comentarios que explican exactamente qué cambiar y qué dejar igual.

#### Paso 5 — Ejecutar y obtener resultados

Ejecutá todas las celdas en orden. El notebook genera:

- Un **Excel** con 5 hojas: glosario mapeado, verticales priorizadas, dataset completo, coautorías industriales y organizaciones no académicas detectadas
- Un **gráfico de barras** con la distribución de papers por vertical industrial
- Un **gráfico de tendencia temporal** con la evolución de las 6 verticales principales

### ¿Dónde encuentro los resultados?

El Excel se guarda en la ruta que definiste en `RUTA_SALIDA`. Los gráficos se guardan como `grafico_verticales.png` y `grafico_tendencia.png` en la carpeta desde donde ejecutás Jupyter.

---

## Estructura del repositorio

```
inteligencia-bibliometrica/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── enriquecimiento/           ← Módulo 0: Enriquecimiento de la base (PREREQUISITO)
│   └── enriquecer_papers_scopus.ipynb
│
├── data/
│   ├── raw/               ← Poné acá tus archivos Excel de Scopus (no se suben al repo)
│   │   └── README.md
│   └── sample/            ← Datos de ejemplo con datos sintéticos para probar
│
├── notebooks/             ← Módulo 1: Comparador de producción científica
│   ├── 01_generar_informe.ipynb
│   ├── 02_graficar_fortalezas.ipynb
│   ├── 02b_tabla_fortalezas.ipynb
│   ├── 03_graficar_similitudes.ipynb
│   ├── 03b_tabla_similitudes.ipynb
│   ├── 04_comparacion_densidad_relativa.ipynb
│   ├── 04b_tabla_densidad_relativa.ipynb
│   ├── 05_comparacion_volumen_absoluto.ipynb
│   └── 05b_tabla_volumen_absoluto.ipynb
│
└── mapeo_verticales/      ← Módulo 2: Mapeo de verticales industriales
    ├── Mapeo_de_verticales_industriales.ipynb
    └── data/
        └── ext_list_Feb_2026.xlsx
```

---

## Universidades analizadas en este proyecto

- UBA (Universidad de Buenos Aires)
- CAMPINAS (Universidad de Campinas)
- UNAL (Universidad Nacional de Colombia)
- Universidad de Chile
- TEC Monterrey
- Pontificia Universidad Javeriana
- SAO PAULO (Universidad de São Paulo)
