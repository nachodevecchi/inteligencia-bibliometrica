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

El proyecto tiene dos flujos de análisis:

#### Flujo A — Comparación entre dos universidades

Los notebooks 01, 02 y 03 deben ejecutarse en orden:

| Orden | Archivo | ¿Qué hace? |
|-------|---------|------------|
| 1 | `01_generar_informe.ipynb` | Compara dos universidades y genera el archivo Excel del informe en tu escritorio |
| 2 | `02_graficar_fortalezas.ipynb` | Genera gráficos de fortalezas a partir del informe generado en el paso 1 |
| 3 | `03_graficar_similitudes.ipynb` | Genera gráficos de similitudes a partir del informe generado en el paso 1 |

#### Flujo B — Comparación entre tres universidades

Los notebooks 04 y 05 toman como insumo los informes Excel generados por el notebook 01. Por eso, antes de usarlos necesitás haber ejecutado el notebook 01 al menos dos veces (una por cada par de universidades a comparar).

| Archivo | ¿Qué hace? |
|---------|------------|
| `04_comparacion_densidad_relativa.ipynb` | Compara la densidad relativa de producción (papers por cada 1000) entre tres universidades |
| `05_comparacion_volumen_absoluto.ipynb` | Compara el volumen absoluto de papers entre tres universidades |

### Paso 5 — Configurar cada notebook

Al abrir cada notebook, vas a encontrar una sección de **CONFIGURACIÓN** al principio. Solo tenés que modificar esas variables:

**En el notebook 01:**
```python
universidad1_name = "UBA"
universidad2_name = "CAMPINAS"
universidad1_file = r"data/raw/UBA.xlsx"
universidad2_file = r"data/raw/CAMPINAS.xlsx"
```

**En los notebooks 02 y 03:**
```python
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_COMPARACION = "CAMPINAS"
file_path = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
```

**En los notebooks 04 y 05:**
```python
INFORME_1 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
INFORME_2 = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_UNAL.xlsx"
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_2 = "CAMPINAS"
UNIVERSIDAD_3 = "UNAL"
```

> 💡 Los informes que usan los notebooks 04 y 05 los encontrás en tu escritorio, generados por el notebook 01.

### Paso 6 — ¿Dónde encuentro los resultados?

- El **informe Excel** se guarda automáticamente en tu **escritorio** al ejecutar el notebook 01.
- Los **gráficos** se guardan como `.png` en la carpeta desde donde ejecutás Jupyter y también se muestran en el notebook.

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
    ├── 03_graficar_similitudes.ipynb
    ├── 04_comparacion_densidad_relativa.ipynb
    └── 05_comparacion_volumen_absoluto.ipynb
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

---
