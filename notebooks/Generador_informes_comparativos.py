import os
import pandas as pd

# 1 - Nombres de universidades y Rutas de archivos 
universidad1_name = "UBA"  # Cambiar por el nombre de tu primera universidad
universidad2_name = "UNIVERSIDAD_COMPARACIÓN"  # Cambiar por el nombre de la segunda universidad

universidad1_file = r"ruta/del/archivo/universidad1.xlsx"
universidad2_file = r"ruta/del/archivo/universidad2.xlsx"

# 2 - FUNCIONES

def normalize_colnames(df):
    return df.rename(columns={c: c.strip() for c in df.columns})

def find_col(df, candidates):
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols:
            return cols[cand.lower()]
    for cand in candidates:  # búsqueda parcial
        for c in df.columns:
            if cand.lower() in c.lower():
                return c
    return None

def explode_multivalues(df, column, sep=';'):
    s = df[column].fillna('').astype(str).str.split(sep)
    rows = []
    for idx, vals in s.items():
        vals = [v.strip() for v in vals if v.strip() != '']
        if not vals:
            rows.append({**df.loc[idx].to_dict(), column: None})
        else:
            for v in vals:
                row = df.loc[idx].to_dict()
                row[column] = v
                rows.append(row)
    return pd.DataFrame(rows)

# 3 - CARGAR ARCHIVOS

df_uni1 = pd.read_excel(universidad1_file)
df_uni2 = pd.read_excel(universidad2_file)

df_uni1 = normalize_colnames(df_uni1)
df_uni2 = normalize_colnames(df_uni2)

# 4 - IDENTIFICAR COLUMNAS RELEVANTES

subgrupo_col_uni1 = find_col(df_uni1, ["Subgrupo"])
area_col_uni1 = find_col(df_uni1, ["Area tematica", "Área temática"])
autores_col_uni1 = find_col(df_uni1, ["autores", "Autores", "authors"])

subgrupo_col_uni2 = find_col(df_uni2, ["Subgrupo"])
area_col_uni2 = find_col(df_uni2, ["Area tematica", "Área temática"])

# 5 - COMPLETAR SI FALTA ALGUNA COLUMNA

if subgrupo_col_uni1 is None: df_uni1["Subgrupo"] = ""; subgrupo_col_uni1 = "Subgrupo"
if subgrupo_col_uni2 is None: df_uni2["Subgrupo"] = ""; subgrupo_col_uni2 = "Subgrupo"
if area_col_uni1 is None: df_uni1["Area tematica"] = ""; area_col_uni1 = "Area tematica"
if area_col_uni2 is None: df_uni2["Area tematica"] = ""; area_col_uni2 = "Area tematica"
if autores_col_uni1 is None: df_uni1["autores"] = ""; autores_col_uni1 = "autores"

# 6 - TOTALES

n_uni1 = len(df_uni1)
n_uni2 = len(df_uni2)

# 7 - SUBGRUPO: CONTEOS Y COMPARACIÓN

uni1_sub_expl = explode_multivalues(df_uni1, subgrupo_col_uni1)
uni2_sub_expl = explode_multivalues(df_uni2, subgrupo_col_uni2)

uni1_sub_counts = uni1_sub_expl[subgrupo_col_uni1].value_counts().rename_axis("Subgrupo").reset_index(name=f"{universidad1_name}_count")
uni2_sub_counts = uni2_sub_expl[subgrupo_col_uni2].value_counts().rename_axis("Subgrupo").reset_index(name=f"{universidad2_name}_count")

sub_df = pd.merge(uni1_sub_counts, uni2_sub_counts, on="Subgrupo", how="outer").fillna(0)
sub_df[f"{universidad1_name}_count"] = sub_df[f"{universidad1_name}_count"].astype(int)
sub_df[f"{universidad2_name}_count"] = sub_df[f"{universidad2_name}_count"].astype(int)
sub_df[f"{universidad1_name}_per_1000"] = (sub_df[f"{universidad1_name}_count"] / max(n_uni1,1) * 1000).round(3)
sub_df[f"{universidad2_name}_per_1000"] = (sub_df[f"{universidad2_name}_count"] / max(n_uni2,1) * 1000).round(3)
sub_df["Difference_per_1000"] = (sub_df[f"{universidad1_name}_per_1000"] - sub_df[f"{universidad2_name}_per_1000"]).round(3)
sub_df = sub_df.sort_values(by=f"{universidad1_name}_count", ascending=False).reset_index(drop=True)

# 8 - ÁREA TEMÁTICA: CONTEOS Y COMPARACIÓN

uni1_area_expl = explode_multivalues(df_uni1, area_col_uni1)
uni2_area_expl = explode_multivalues(df_uni2, area_col_uni2)

uni1_area_counts = uni1_area_expl[area_col_uni1].value_counts().rename_axis("Area tematica").reset_index(name=f"{universidad1_name}_count")
uni2_area_counts = uni2_area_expl[area_col_uni2].value_counts().rename_axis("Area tematica").reset_index(name=f"{universidad2_name}_count")

area_df = pd.merge(uni1_area_counts, uni2_area_counts, on="Area tematica", how="outer").fillna(0)
area_df[f"{universidad1_name}_count"] = area_df[f"{universidad1_name}_count"].astype(int)
area_df[f"{universidad2_name}_count"] = area_df[f"{universidad2_name}_count"].astype(int)
area_df[f"{universidad1_name}_per_1000"] = (area_df[f"{universidad1_name}_count"] / max(n_uni1,1) * 1000).round(3)
area_df[f"{universidad2_name}_per_1000"] = (area_df[f"{universidad2_name}_count"] / max(n_uni2,1) * 1000).round(3)
area_df["Difference_per_1000"] = (area_df[f"{universidad1_name}_per_1000"] - area_df[f"{universidad2_name}_per_1000"]).round(3)
area_df = area_df.sort_values(by=f"{universidad1_name}_count", ascending=False).reset_index(drop=True)

# 9 - PAPERS CON AUTORES DE LA FACULTAD DE CIENCIAS EXACTAS (UBA)

uni1_fcen_mask = df_uni1[autores_col_uni1].fillna('').astype(str).str.strip() != ""
uni1_fcen = df_uni1[uni1_fcen_mask]
n_uni1_fcen = len(uni1_fcen)

uni1_fcen_sub_expl = explode_multivalues(uni1_fcen, subgrupo_col_uni1)
uni1_fcen_sub_counts = uni1_fcen_sub_expl[subgrupo_col_uni1].value_counts().rename_axis("Subgrupo").reset_index(name=f"{universidad1_name}_FCEN_count")

sub_df = pd.merge(sub_df, uni1_fcen_sub_counts, on="Subgrupo", how="left").fillna(0)
sub_df[f"{universidad1_name}_FCEN_count"] = sub_df[f"{universidad1_name}_FCEN_count"].astype(int)
sub_df[f"%FCEN_dentro_{universidad1_name}_Subgrupo"] = (
    sub_df[f"{universidad1_name}_FCEN_count"] / sub_df[f"{universidad1_name}_count"].replace({0: pd.NA}) * 100
).round(2).fillna(0)

# 10 - RESUMEN DE SUPERPOSICIÓN

common_subgrupos = set(uni1_sub_counts["Subgrupo"]).intersection(set(uni2_sub_counts["Subgrupo"]))
only_uni1 = set(uni1_sub_counts["Subgrupo"]) - set(uni2_sub_counts["Subgrupo"])
only_uni2 = set(uni2_sub_counts["Subgrupo"]) - set(uni1_sub_counts["Subgrupo"])

overlap_summary = pd.DataFrame({
    "Category":[f"Subgrupos comunes",f"Solo {universidad1_name}",f"Solo {universidad2_name}"],
    "Count":[len(common_subgrupos),len(only_uni1),len(only_uni2)]
})


# 11 - TOP FORTALEZAS Y DEBILIDADES


top_strengths_sub = sub_df.sort_values(by="Difference_per_1000", ascending=False).head(20)
top_weakness_sub = sub_df.sort_values(by="Difference_per_1000", ascending=True).head(20)
top_areas_uni1 = area_df.sort_values(by=f"{universidad1_name}_per_1000", ascending=False).head(30)


# 12 - EXPORTAR EXCEL FINAL


out_file = os.path.join(os.path.expanduser("~"), "Desktop", f"informe_comparativo_{universidad1_name}_{universidad2_name}.xlsx")

with pd.ExcelWriter(out_file, engine="openpyxl") as writer:
    pd.DataFrame([
        {"Métrica":f"Total papers {universidad1_name}","Valor":n_uni1},
        {"Métrica":f"Total papers {universidad2_name}","Valor":n_uni2},
        {"Métrica":f"Papers {universidad1_name} con ≥1 autor FCEN-{universidad1_name}","Valor":n_uni1_fcen}
    ]).to_excel(writer, sheet_name="Resumen", index=False)

    sub_df.to_excel(writer, sheet_name="Subgrupos", index=False)
    area_df.to_excel(writer, sheet_name="Áreas temáticas", index=False)
    uni1_fcen_sub_counts.to_excel(writer, sheet_name=f"Subgrupos FCEN-{universidad1_name}", index=False)
    overlap_summary.to_excel(writer, sheet_name="Superposición", index=False)
    top_strengths_sub.to_excel(writer, sheet_name="Fortalezas", index=False)
    top_weakness_sub.to_excel(writer, sheet_name="Debilidades", index=False)
    top_areas_uni1.to_excel(writer, sheet_name=f"Top áreas {universidad1_name}", index=False)

print(f"\n✅ Informe generado correctamente en:\n{out_file}")
