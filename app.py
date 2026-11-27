
import streamlit as st
import pandas as pd
import html

# -----------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------

st.set_page_config(
    page_title="MoodMusic | Tu música, tu estado de ánimo",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# DISEÑO CSS: NEGRO Y MORADO NEÓN
# -----------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #090611, #140b25, #090611);
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background: #10091d;
    border-right: 1px solid #6525a8;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

h1, h2, h3 {
    color: #d8a7ff !important;
}

p, label {
    color: #e6dcf5;
}

.neon-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    color: #d9a5ff;
    text-shadow: 0 0 10px #a855f7,
                 0 0 25px #9333ea;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #c8b4df;
    font-size: 17px;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(145deg, #211333, #120b20);
    border: 1px solid #923bdb;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 12px #6925a555;
    min-height: 125px;
}

.metric-label {
    color: #c9a7e9;
    font-size: 14px;
}

.metric-value {
    color: #ffffff;
    font-size: 25px;
    font-weight: bold;
    margin-top: 10px;
    overflow-wrap: anywhere;
}

.section-card {
    background: #170e25;
    border: 1px solid #632a91;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #7027b9, #a855f7);
    color: white;
    border: 1px solid #c084fc;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border: 1px solid white;
    box-shadow: 0 0 14px #a855f7;
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: #211333;
    border-color: #923bdb;
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid #632a91;
    border-radius: 10px;
}

hr {
    border-color: #632a91;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# CARGAR ARCHIVO CSV
# -----------------------------------------

@st.cache_data
def cargar_datos():
    return pd.read_csv("moodmusic_dataset.csv")


try:
    df = cargar_datos()

except FileNotFoundError:
    st.error(
        "No se encontró moodmusic_dataset.csv. "
        "Verifica que esté en la raíz del repositorio."
    )
    st.stop()

except Exception as e:
    st.error(f"No se pudo cargar el archivo: {e}")
    st.stop()


# -----------------------------------------
# VALIDAR COLUMNAS
# -----------------------------------------

columnas_necesarias = [
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

faltantes = [
    columna for columna in columnas_necesarias
    if columna not in df.columns
]

if faltantes:
    st.error(f"Faltan columnas en el CSV: {faltantes}")
    st.stop()

df = df.copy()

# Eliminar filas sin datos esenciales
df = df.dropna(
    subset=["cancion", "artista", "estado_animo"]
)

df["estado_animo"] = df["estado_animo"].astype(str)
df["genero"] = df["genero"].fillna("Por identificar")


# -----------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------

def tarjeta(titulo, valor):
    titulo_seguro = html.escape(str(titulo))
    valor_seguro = html.escape(str(valor))

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{titulo_seguro}</div>
        <div class="metric-value">{valor_seguro}</div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------
# MENÚ LATERAL
# -----------------------------------------

with st.sidebar:

    st.markdown("## 🎧 MoodMusic")

    st.caption("Tu música, tu estado de ánimo")

    st.divider()

    pagina = st.radio(
        "MENÚ PRINCIPAL",
        [
            "🏠 Inicio",
            "🎵 Playlists",
            "📚 Catálogo"
        ]
    )

    st.divider()

    st.markdown("### 💜 Sobre el proyecto")

    st.write(
        "MoodMusic organiza canciones según "
        "el estado de ánimo seleccionado por el usuario."
    )

    st.caption("Proyecto de Ciencia de Datos")


# -----------------------------------------
# ENCABEZADO
# -----------------------------------------

st.markdown(
    '<div class="neon-title">MOODMUSIC</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Encuentra la música que conecta con tu momento'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------------------
# PÁGINA DE INICIO
# -----------------------------------------

if pagina == "🏠 Inicio":

    st.markdown("## ✨ Tu espacio musical")

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

    # Tarjetas de indicadores

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        tarjeta("🎵 Total de canciones", total)

    with col2:
        tarjeta("💜 Estado predominante", estado_principal)

    with col3:
        tarjeta("🎼 Género más frecuente", genero_principal)

    with col4:
        tarjeta("% de Melancolía", f"{porcentaje_melancolia:.1f}%")

    st.divider()

    # Gráficas

    izquierda, derecha = st.columns(2)

    with izquierda:

        st.markdown("### 💜 Canciones por estado de ánimo")

        conteo_animo = (
            df["estado_animo"]
            .value_counts()
            .rename_axis("Estado de ánimo")
            .to_frame("Canciones")
        )

        st.bar_chart(
            conteo_animo,
            color="#a855f7"
        )

    with derecha:

        st.markdown("### 🎼 Géneros musicales")

        conteo_generos = (
            df["genero"]
            .value_counts()
            .head(10)
            .rename_axis("Género")
            .to_frame("Canciones")
        )

        st.bar_chart(
            conteo_generos,
            color="#c084fc"
        )

    st.divider()

    st.markdown("### 🎧 Explora MoodMusic")

    st.write(
        "Entra a Playlists para encontrar canciones "
        "según el estado de ánimo que quieras explorar."
    )

    st.info(
        "Selecciona una categoría en el menú lateral "
        "para comenzar."
    )


# -----------------------------------------
# PÁGINA DE PLAYLISTS
# -----------------------------------------

elif pagina == "🎵 Playlists":

    st.markdown("## 🎧 Encuentra tu playlist")

    st.write(
        "Selecciona un estado de ánimo y descubre "
        "las canciones disponibles en el catálogo."
    )

    estados = sorted(
        df["estado_animo"].dropna().unique().tolist()
    )

    if not estados:
        st.warning("No hay estados de ánimo disponibles.")
        st.stop()

    seleccion = st.selectbox(
        "💜 ¿Qué estado de ánimo deseas explorar?",
        estados
    )

    canciones = df[
        df["estado_animo"] == seleccion
    ].copy()

    st.markdown(
        f"### ✨ Playlist: {seleccion}"
    )

    st.success(
        f"Encontramos {len(canciones)} canciones para esta categoría."
    )

    # Buscador

    busqueda = st.text_input(
        "🔎 Buscar canción o artista",
        placeholder="Escribe el nombre de una canción o artista..."
    )

    canciones_mostrar = canciones.copy()

    if busqueda:
        coincidencias = (
            canciones_mostrar["cancion"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
            |
            canciones_mostrar["artista"].astype(str).str.contains(
                busqueda, case=False, na=False
            )
        )

        canciones_mostrar = canciones_mostrar[
            coincidencias
        ]

    st.dataframe(
        canciones_mostrar[
            ["cancion", "artista", "genero"]
        ],
        use_container_width=True,
        hide_index=True
    )

    # Descargar playlist

    archivo_playlist = canciones_mostrar.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Descargar esta playlist",
        data=archivo_playlist,
        file_name=f"playlist_{seleccion}.csv",
        mime="text/csv"
    )


# -----------------------------------------
# PÁGINA DE CATÁLOGO
# -----------------------------------------

elif pagina == "📚 Catálogo":

    st.markdown("## 📚 Catálogo musical")

    st.write(
        "Consulta las canciones que forman parte "
        "de la base de datos de MoodMusic."
    )

    st.markdown(
        f"### 🎵 {len(df)} canciones registradas"
    )

    # Búsqueda general

    busqueda_catalogo = st.text_input(
        "🔎 Buscar en todo el catálogo",
        placeholder="Canción, artista o género..."
    )

    catalogo = df.copy()

    if busqueda_catalogo:

        coincidencias = (
            catalogo["cancion"].astype(str).str.contains(
                busqueda_catalogo, case=False, na=False
            )
            |
            catalogo["artista"].astype(str).str.contains(
                busqueda_catalogo, case=False, na=False
            )
            |
            catalogo["genero"].astype(str).str.contains(
                busqueda_catalogo, case=False, na=False
            )
        )

        catalogo = catalogo[coincidencias]

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

    # Descargar catálogo completo

    archivo_catalogo = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Descargar catálogo completo",
        data=archivo_catalogo,
        file_name="moodmusic_catalogo.csv",
        mime="text/csv"
    )


# -----------------------------------------
# PIE DE PÁGINA
# -----------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#b99bd8;">
        🎧 MOODMUSIC | Recomendador de Playlist
        <br>
        Proyecto de Ciencia de Datos
    </div>
    """,
    unsafe_allow_html=True
)
