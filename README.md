# Comparador de Producción Científica Universitaria

Herramienta desarrollada por la Oficina de Vinculación Tecnológica de la FCEN-UBA para comparar la producción científica entre universidades a partir de datos exportados de Scopus.

---

## ¿Qué hace este proyecto?

A partir de bases de datos exportadas de Scopus, genera informes comparativos en Excel y gráficos de análisis entre dos universidades. Permite visualizar fortalezas, debilidades y similitudes en producción científica por área temática y subgrupo disciplinar.

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

## Cómo usar el proyecto

### Paso 1 — Descargar el repositorio

En la página del repositorio en GitHub, hacé clic en **Code → Download ZIP** y descomprimí la carpeta en tu computadora.

### Paso 2 — Conseguir los datos

Los datos de cada universidad son archivos Excel exportados directamente desde [Scopus](https://www.scopus.com). Para exportarlos:

1. Buscá la producción de la universidad en Scopus
2. Seleccioná todos los resultados
3. Exportá como Excel (`.xlsx`)
4. Guardá cada archivo en la carpeta `data/raw/` con un nombre claro, por ejemplo `UBA.xlsx`, `CAMPINAS.xlsx`, etc.

> ⚠️ Los archivos de datos **no están incluidos** en el repositorio por restricciones de licencia de Scopus.

### Paso 3 — Abrir Jupyter Notebook

Abrí Jupyter Notebook y navegá hasta la carpeta del proyecto.

### Paso 4 — Ejecutar los notebooks en orden

Los notebooks deben ejecutarse en este orden:

| Orden | Archivo | ¿Qué hace? |
|-------|---------|------------|
| 1 | `notebooks/01_generar_informe.ipynb` | Compara dos universidades y genera el archivo Excel del informe en tu escritorio |
| 2 | `notebooks/02_graficar_fortalezas.ipynb` | Genera gráficos de fortalezas a partir del informe generado en el paso 1 |
| 3 | `notebooks/03_graficar_similitudes.ipynb` | Genera gráficos de similitudes a partir del informe generado en el paso 1 |

### Paso 5 — Configurar cada notebook

Al abrir cada notebook, vas a encontrar una sección de **CONFIGURACIÓN** al principio. Solo tenés que modificar esas variables:

**En el notebook 1:**
```python
universidad1_name = "UBA"           # Nombre de tu primera universidad
universidad2_name = "CAMPINAS"      # Nombre de la segunda universidad
universidad1_file = r"data/raw/UBA.xlsx"
universidad2_file = r"data/raw/CAMPINAS.xlsx"
```

**En los notebooks 2 y 3:**
```python
UNIVERSIDAD_REFERENCIA = "UBA"
UNIVERSIDAD_COMPARACION = "CAMPINAS"
file_path = r"C:\Users\TU_USUARIO\Desktop\informe_comparativo_UBA_CAMPINAS.xlsx"
```

> 💡 La ruta `file_path` es la del archivo que se generó en el paso anterior. Lo encontrás en tu escritorio.

### Paso 6 — ¿Dónde encuentro los resultados?

- El **informe Excel** se guarda automáticamente en tu **escritorio** al ejecutar el notebook 1.
- Los **gráficos** se muestran en el notebook y también se pueden guardar desde ahí.

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
│   ├── raw/               ← Poné acá tus archivos Excel de Scopus
│   │   └── README.md
│   └── sample/            ← Datos de ejemplo para probar sin datos reales
│
└── notebooks/
    ├── 01_generar_informe.ipynb
    ├── 02_graficar_fortalezas.ipynb
    └── 03_graficar_similitudes.ipynb
```

---

## Universidades analizadas en este proyecto

- UBA (Universidad de Buenos Aires)
- CAMPINAS
- UNAL (Universidad Nacional de Colombia)
- Universidad de Chile
- TEC Monterrey
- Pontificia Universidad Javeriana
- SAO PAULO

---


