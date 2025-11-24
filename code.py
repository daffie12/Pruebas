import streamlit as st

st.set_page_config(page_title="Ruta de decisión estadística", layout="wide")

st.title("🔍 Ruta de decisión para seleccionar la prueba estadística adecuada")
st.write("Responde las siguientes preguntas para recibir una recomendación de prueba.")

# ------------------------- DECISION QUESTIONS ---------------------------- #

tipo_objetivo = st.selectbox(
    "1️⃣ ¿Cuál es tu objetivo estadístico?",
    [
        "Comparar grupos",
        "Analizar relación/correlación",
        "Predecir una variable"
    ]
)

# ------------------------- COMPARAR GRUPOS ------------------------------ #
if tipo_objetivo == "Comparar grupos":

    n_grupos = st.selectbox(
        "2️⃣ ¿Cuántos grupos quieres comparar?",
        ["2 grupos", "3 o más grupos"]
    )

    dependientes = st.selectbox(
        "3️⃣ ¿Las mediciones provienen de los mismos sujetos?",
        ["No, son grupos independientes", "Sí, son mediciones relacionadas/pareadas"]
    )

    tipo_variable = st.selectbox(
        "4️⃣ ¿Qué tipo de variable dependiente tienes?",
        ["Continua", "Ordinal", "Categórica"]
    )

    normalidad = st.selectbox(
        "5️⃣ ¿Los datos cumplen normalidad?",
        ["Sí", "No", "No estoy segura/o"]
    )

    # ------- DECISIONES ------- #

    # Caso 1: Comparar 2 grupos independientes
    if n_grupos == "2 grupos" and dependientes == "No, son grupos independientes":

        if tipo_variable == "Categórica":
            prueba = "Chi-cuadrada"
        elif tipo_variable == "Continua" and normalidad == "Sí":
            prueba = "t de Student para muestras independientes"
        else:
            prueba = "U de Mann-Whitney"

    # Caso 2: Comparar 2 mediciones relacionadas
    elif n_grupos == "2 grupos" and dependientes == "Sí, son mediciones relacionadas/pareadas":

        if tipo_variable == "Continua" and normalidad == "Sí":
            prueba = "t de Student para muestras relacionadas"
        else:
            prueba = "Wilcoxon"

    # Caso 3: Comparar +3 grupos independientes
    elif n_grupos == "3 o más grupos" and dependientes == "No, son grupos independientes":

        if tipo_variable == "Categórica":
            prueba = "Chi-cuadrada"
        elif tipo_variable == "Continua" and normalidad == "Sí":
            prueba = "ANOVA de un factor"
        else:
            prueba = "Kruskal-Wallis"
    
    # Caso 4: Comparar +3 mediciones relacionadas
    else:
        prueba = "Friedman (no incluida en tu tabla pero es la correcta)"

# ------------------------- RELACIÓN ENTRE VARIABLES ------------------------------ #
elif tipo_objetivo == "Analizar relación/correlación":

    tipo_variable = st.selectbox(
        "2️⃣ ¿Qué tipo de variables vas a relacionar?",
        ["Ambas continuas", "Al menos una ordinal", "Ambas categóricas"]
    )

    if tipo_variable == "Ambas categóricas":
        prueba = "Chi-cuadrada"

    elif tipo_variable == "Ambas continuas":
        normalidad = st.selectbox("¿Las variables cumplen normalidad bivariada?", ["Sí", "No", "No sé"])

        if normalidad == "Sí":
            prueba = "Correlación de Pearson"
        else:
            prueba = "Correlación de Spearman"

    else:
        prueba = "Correlación de Spearman"

# ------------------------- PREDICCIÓN ------------------------------------ #
else:
    prueba = "Regresión lineal simple"

# ------------------------- RESULTADOS DE LA PRUEBA ---------------------------- #

st.subheader("📌 Prueba recomendada:")
st.success(f"La prueba estadística sugerida es: **{prueba}**")

# Información detallada
info = {
    "t de Student para muestras independientes":{
        "tipo":"Paramétrica",
        "objetivo":"Comparar medias entre dos grupos independientes.",
        "características":[
            "Variable dependiente continua",
            "Grupos independientes"
        ],
        "supuestos":[
            "Normalidad por grupo",
            "Homogeneidad de varianzas",
            "Ausencia de outliers"
        ]
    },
    "U de Mann-Whitney":{
        "tipo":"No paramétrica",
        "objetivo":"Comparar dos grupos independientes cuando no hay normalidad.",
        "características":[
            "Usa rangos",
            "Alternativa de t independiente"
        ],
        "supuestos":[
            "Datos ordinales o continuos no normales",
            "Distribuciones con forma similar"
        ]
    },
    "Chi-cuadrada":{
        "tipo":"No paramétrica",
        "objetivo":"Analizar asociación entre variables categóricas.",
        "características":[
            "Tablas de contingencia"
        ],
        "supuestos":[
            "Frecuencias esperadas ≥ 5 en 80% de celdas",
            "Muestra grande"
        ]
    },
    "t de Student para muestras relacionadas":{
        "tipo":"Paramétrica",
        "objetivo":"Comparar dos mediciones en el mismo grupo.",
        "características":[
            "Mediciones emparejadas"
        ],
        "supuestos":[
            "Diferencias con distribución normal"
        ]
    },
    "Wilcoxon":{
        "tipo":"No paramétrica",
        "objetivo":"Comparar dos mediciones relacionadas sin normalidad.",
        "características":[
            "Usa rangos de diferencias"
        ],
        "supuestos":[
            "Datos ordinales o continuos no normales",
            "Distribución simétrica de diferencias"
        ]
    },
    "ANOVA de un factor":{
        "tipo":"Paramétrica",
        "objetivo":"Comparar medias de tres o más grupos independientes.",
        "características":[
            "Factor con ≥ 3 niveles"
        ],
        "supuestos":[
            "Normalidad por grupo",
            "Homogeneidad de varianzas",
            "Sin outliers"
        ]
    },
    "Kruskal-Wallis":{
        "tipo":"No paramétrica",
        "objetivo":"Comparar ≥3 grupos sin normalidad.",
        "características":[
            "Usa rangos"
        ],
        "supuestos":[
            "Distribuciones con forma similar"
        ]
    },
    "Correlación de Pearson":{
        "tipo":"Paramétrica",
        "objetivo":"Medir relación lineal entre variables continuas.",
        "características":[
            "Coeficiente entre -1 y +1"
        ],
        "supuestos":[
            "Normalidad bivariada",
            "Linealidad",
            "Homocedasticidad"
        ]
    },
    "Correlación de Spearman":{
        "tipo":"No paramétrica",
        "objetivo":"Medir relación monotónica entre variables.",
        "características":[
            "Basada en rangos",
            "Relación monotónica"
        ],
        "supuestos":[
            "Variables ordinales o continuas",
            "Relación monotónica"
        ]
    },
    "Regresión lineal simple":{
        "tipo":"Paramétrica",
        "objetivo":"Predecir Y a partir de X.",
        "características":[
            "Ecuación Y = b0 + b1X"
        ],
        "supuestos":[
            "Linealidad",
            "Normalidad de residuales",
            "Homoscedasticidad",
            "Sin outliers"
        ]
    }
}

detalles = info.get(prueba, None)

if detalles:
    st.markdown(f"### 📘 Tipo: **{detalles['tipo']}**")
    st.markdown(f"### 🎯 Objetivo: {detalles['objetivo']}")

    st.markdown("### 🔹 Características principales:")
    for c in detalles["características"]:
        st.markdown(f"- {c}")

    st.markdown("### 📏 Supuestos:")
    for s in detalles["supuestos"]:
        st.markdown(f"- {s}")

