import streamlit as st
import pandas as pd
import html
# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="MoodMusic",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================
# ESTILOS: MORADO, ROSA Y NEGRO
# ==========================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #100b18, #191025, #100b18);
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #171020;
    border-right: 1px solid #75408f;
}
[data-testid="stSidebar"] * {
    color: #ffffff;
}
h1, h2, h3 {
    color: #f1c5ff !important;
}
p, label {
    color: #e8dced;
}
/* Encabezado */
.hero {
    background: linear-gradient(110deg, #54217d, #9b3d85, #d45b91);
    padding: 35px 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 5px 25px #a33b9b44;
}
.hero h1 {
    color: white !important;
    font-size: 43px;
    font-weight: 900;
    margin: 0;
}
.hero p {
    color: #fff0fa;
    font-size: 17px;
    margin-bottom: 0;
}
/* Tarjetas */
.metric-card {
    background: linear-gradient(145deg, #291936, #1a1125);
    border: 1px solid #8c4c9d;
    border-radius: 17px;
    padding: 22px 15px;
    min-height: 125px;
    box-shadow: 0 4px 18px #a34b9630;
}
.metric-label {
    color: #e8b9ed;
    font-size: 14px;
}
.metric-value {
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    margin-top: 12px;
    overflow-wrap: anywhere;
}
/* Secciones */
.section-box {
    background: #21152d;
    border: 1px solid #704080;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}
/* Botones */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #8238a8, #d35b9b);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    transition: 0.2s;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    box-shadow: 0 0 15px #d35b9b99;
    color: white;
    border: 1px solid #f4b5dc;
}
/* Selectores */
div[data-baseweb="select"] > div {
    background-color: #291936;
    border-color: #a34b96;
    color: white;
}
/* Entradas */
.stTextInput input {
    background-color: #25182e;
    color: white;
    border: 1px solid #965b9d;
    border-radius: 10px;
}
/* Tablas */
[data-testid="stDataFrame"] {
    border: 1px solid #75408f;
    border-radius: 12px;
}
/* Separadores */
hr {
    border-color: #75408f;
}
</style>
""", unsafe_allow_html=True)
# ==========================================
# CARGAR DATASET
# ==========================================
@st.cache_data
def cargar_datos():
    return pd.read_csv("moodmusic_dataset.csv")
try:
    df = cargar_datos()
except FileNotFoundError:
    st.error(
        "No se encontró moodmusic_dataset.csv. "
        "Comprueba que esté en la raíz del repositorio."
    )
    st.stop()
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()
# ==========================================
# VALIDAR INFORMACIÓN
# ==========================================
columnas = [
    "id",
    "cancion",
    "artista",
    "genero",
    "estado_animo",
    "energia_0_1",
    "valence_0_1",
    "tempo_bpm",
    "observaciones"
]
faltantes = [c for c in columnas if c not in df.columns]
if faltantes:
    st.error(f"Faltan estas columnas: {faltantes}")
    st.stop()
df = df.dropna(
    subset=["cancion", "artista", "estado_animo"]
).copy()
df["estado_animo"] = df["estado_animo"].astype(str)
df["genero"] = df["genero"].fillna("Por identificar")
# ==========================================
# FUNCIONES
# ==========================================
def tarjeta(titulo, valor):
    titulo = html.escape(str(titulo))
    valor = html.escape(str(valor))
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{titulo}</div>
        <div class="metric-value">{valor}</div>
    </div>
    """, unsafe_allow_html=True)
iconos = {
    "Alegría": "😊",
    "Energía": "⚡",
    "Melancolía": "🌙",
    "Tranquilidad": "🌸"
}
# ==========================================
# MENÚ LATERAL
# ==========================================
with st.sidebar:
    st.markdown("# 🎧 MoodMusic")
    st.caption("Tu música, tu momento")
    st.divider()
    pagina = st.radio(
        "EXPLORAR",
        [
            "🏠 Inicio",
            "💜 Playlists",
            "🎵 Catálogo",
            "📊 Estadísticas"
        ]
    )
    st.divider()
    st.markdown("### Acerca de MoodMusic")
    st.write(
        "Un proyecto de Ciencia de Datos "
        "que organiza canciones según "
        "nuestro estado de anímo que escojamos"
    )
    st.caption("Proyecto Final")
# ==========================================
# ENCABEZADO GENERAL
# ==========================================
st.markdown("""
<div class="hero">
    <h1>🎧 MOODMUSIC</h1>
    <p>Descubre diferentes canciones que te pueden gustar</p>
</div>
""", unsafe_allow_html=True)
# ==========================================
# INICIO
# ==========================================
if pagina == "🏠 Inicio":
    st.markdown("## ✨ Bienvenido a tu espacio musical")
    total = len(df)
    estado_principal = (
        df["estado_animo"].mode().iloc[0]
        if not df["estado_animo"].mode().empty
        else "Sin datos"
    )
    genero_principal = (
        df["genero"].mode().iloc[0]
        if not df["genero"].mode().empty
        else "Sin datos"
    )
    porcentaje_melancolia = (
        (df["estado_animo"] == "Melancolía").mean() * 100
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tarjeta("🎵 Canciones", total)
    with c2:
        tarjeta("💜 Estado predominante", estado_principal)
    with c3:
        tarjeta("🎼 Género principal", genero_principal)
    with c4:
        tarjeta("% Melancolía", f"{porcentaje_melancolia:.1f}%")
    st.divider()
    izquierda, derecha = st.columns(2)
    with izquierda:
        st.markdown("### 💜 Estados de ánimo")
        animo = (
            df["estado_animo"]
            .value_counts()
            .rename_axis("Estado de ánimo")
            .to_frame("Canciones")
        )
        st.bar_chart(animo, color="#c084fc")
    with derecha:
        st.markdown("### 🎼 Géneros musicales")
        generos = (
            df["genero"]
            .value_counts()
            .head(10)
            .rename_axis("Género")
            .to_frame("Canciones")
        )
        st.bar_chart(generos, color="#e879b9")
    st.divider()
    st.markdown("### 🌷 Explora tu música")
    st.write(
        "Entra a Playlists y selecciona el estado "
        "de ánimo que deseas explorar."
    )
# ==========================================
# PLAYLISTS
# ==========================================
elif pagina == "💜 Playlists":
    st.markdown("## 🎧 Encuentra tu playlist")
    st.write(
        "Selecciona cómo te sientes o qué tipo "
        "de música quieres explorar."
    )

    estados = sorted(df["estado_animo"].unique())

    if not estados:
        st.warning("No hay estados de ánimo disponibles.")
        st.stop()
    seleccion = st.selectbox(
        "¿Qué estado de ánimo deseas explorar?",
        estados,
        format_func=lambda x: f"{iconos.get(x, '🎵')} {x}"
    )
    canciones = df[
        df["estado_animo"] == seleccion
    ].copy()
    st.markdown(
        f"### {iconos.get(seleccion, '🎵')} Playlist: {seleccion}"
    )
    st.success(
        f"Hay {len(canciones)} canciones en esta categoría."
    )
    busqueda = st.text_input(
        "🔎 Buscar canción o artista",
        placeholder="Escribe aquí..."
    )
    resultado = canciones.copy()
    if busqueda:
        filtro = (
            resultado["cancion"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
            |
            resultado["artista"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
        )
        resultado = resultado[filtro]
    st.dataframe(
        resultado[["cancion", "artista", "genero"]],
        use_container_width=True,
        hide_index=True
    )
    archivo = resultado.to_csv(
        index=False
    ).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar playlist",
        data=archivo,
        file_name=f"playlist_{seleccion}.csv",
        mime="text/csv"
    )
# ==========================================
# CATÁLOGO
# ==========================================
elif pagina == "🎵 Catálogo":
    st.markdown("## 🎼 Nuestro catálogo musical")
    st.write(f"Actualmente hay {len(df)} canciones registradas.")
    busqueda = st.text_input(
        "🔎 Buscar en el catálogo",
        placeholder="Canción, artista o género..."
    )
    catalogo = df.copy()
    if busqueda:
        filtro = (
            catalogo["cancion"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
            |
            catalogo["artista"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
            |
            catalogo["genero"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
        )
        catalogo = catalogo[filtro]
    st.dataframe(
        catalogo[
            [
                "id",
                "cancion",
                "artista",
                "genero",
                "estado_animo"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
    archivo = df.to_csv(
        index=False
    ).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar catálogo completo",
        data=archivo,
        file_name="moodmusic_catalogo.csv",
        mime="text/csv"
    )
# ==========================================
# ESTADÍSTICAS
# ==========================================
elif pagina == "📊 Estadísticas":
    st.markdown("## 📊 Análisis musical")
    st.markdown("### Distribución por estado de ánimo")
    conteo = df["estado_animo"].value_counts()
    st.bar_chart(
        conteo,
        color="#d879b5"
    )
    st.markdown("### Distribución por género")
    generos = df["genero"].value_counts()
    st.bar_chart(
        generos,
        color="#a78bfa"
    )
    st.markdown("### Resumen de canciones por estado")
    resumen = (
        df.groupby("estado_animo")
        .agg(
            Total_canciones=("id", "count"),
            Generos_diferentes=("genero", "nunique")
        )
        .reset_index()
    )
    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )
# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.markdown("""
<div style="
    text-align:center;
    color:#e8b9ed;
    padding:15px;
">
    🎧 <b>MOODMUSIC</b>
    <br>
    Tu música, tu momento 💜
    <br>
    <small>Proyecto de Ciencia de Datos</small>
</div>
""", unsafe_allow_html=True)
