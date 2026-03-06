# Comparador de Producción Científica Universitaria

Herramienta desarrollada por la Oficina de Vinculación Tecnológica de la FCEN-UBA para comparar la producción científica entre universidades a partir de datos exportados de Scopus.

---

## ¿Qué hace este proyecto?

A partir de bases de datos exportadas de Scopus, genera informes comparativos en Excel y gráficos de análisis entre universidades. Permite visualizar fortalezas, debilidades, similitudes y volumen de producción científica por campos de estudio, tanto en comparaciones de dos universidades como de tres.

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

## Datos de ejemplo

Si querés probar el proyecto sin tener datos reales de Scopus, la carpeta `data/sample/` contiene archivos de ejemplo con datos sintéticos para las siguientes universidades:

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

---

## Cómo usar el proyecto con datos reales

### Paso 1 — Descargar el repositorio

En la página del repositorio en GitHub, hacé clic en **Code → Download ZIP** y descomprimí la carpeta en tu computadora.

### Paso 2 — Conseguir los datos

Los datos de cada universidad son archivos Excel exportados directamente desde [Scopus](https://www.scopus.com). Para exportarlos:

1. Buscá la producción de la universidad en Scopus
2. Seleccioná todos los resultados
3. Exportá como CSV y pasalo a Excel (`.xlsx`)
4. Guardá cada archivo en la carpeta `data/raw/` con un nombre claro, por ejemplo `UBA.xlsx`, `CAMPINAS.xlsx`, etc.

> ⚠️ Los archivos de datos reales **no están incluidos** en el repositorio.

### Paso 3 — Abrir Jupyter Notebook

Abrí Jupyter Notebook y navegá hasta la carpeta del proyecto.

### Paso 4 — Ejecutar los notebooks

El proyecto tiene dos flujos de análisis. Cada análisis tiene una versión de **gráfico** y una versión de **tabla Excel**, que podés usar de forma independiente según lo que necesites.

#### Flujo A — Comparación entre dos universidades

Primero ejecutá el notebook 01, que genera el informe base. Luego podés usar los notebooks 02 y 03 en cualquier orden:

| Notebook | ¿Qué genera? |
|----------|--------------|
| `01_generar_informe.ipynb` | Informe Excel comparativo entre dos universidades (insumo para el resto) |
| `02_graficar_fortalezas.ipynb` | Gráfico de fortalezas y debilidades |
| `02b_tabla_fortalezas.ipynb` | Tabla Excel con los mismos datos del gráfico de fortalezas |
| `03_graficar_similitudes.ipynb` | Gráfico de áreas similares |
| `03b_tabla_similitudes.ipynb` | Tabla Excel con los mismos datos del gráfico de similitudes |

#### Flujo B — Comparación entre tres universidades

Antes de usar estos notebooks necesitás haber ejecutado el notebook 01 al menos dos veces (una por cada par de universidades a comparar):

| Notebook | ¿Qué genera? |
|----------|--------------|
| `04_comparacion_densidad_relativa.ipynb` | Gráfico de densidad relativa entre tres universidades |
| `04b_tabla_densidad_relativa.ipynb` | Tabla Excel con los mismos datos del gráfico de densidad relativa |
| `05_comparacion_volumen_absoluto.ipynb` | Gráfico de volumen absoluto entre tres universidades |
| `05b_tabla_volumen_absoluto.ipynb` | Tabla Excel con los mismos datos del gráfico de volumen absoluto |

### Paso 5 — Configurar cada notebook

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

### Paso 6 — ¿Dónde encuentro los resultados?

- Los **informes Excel** (notebooks 01, 02b, 03b, 04b y 05b) se guardan automáticamente en tu **escritorio**.
- Los **gráficos** (notebooks 02, 03, 04 y 05) se guardan como `.png` en la carpeta desde donde ejecutás Jupyter y también se muestran en el notebook.

---

## Estructura del proyecto

```
scientific-output-comparator/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/               ← Poné acá tus archivos Excel de Scopus (no se suben al repo)
│   │   └── README.md
│   └── sample/            ← Datos de ejemplo con datos sintéticos para probar
│
└── notebooks/
    ├── 01_generar_informe.ipynb
    ├── 02_graficar_fortalezas.ipynb
    ├── 02b_tabla_fortalezas.ipynb
    ├── 03_graficar_similitudes.ipynb
    ├── 03b_tabla_similitudes.ipynb
    ├── 04_comparacion_densidad_relativa.ipynb
    ├── 04b_tabla_densidad_relativa.ipynb
    ├── 05_comparacion_volumen_absoluto.ipynb
    └── 05b_tabla_volumen_absoluto.ipynb
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
