
import streamlit as st
import pandas as pd

# Configuración de la aplicación
st.set_page_config(
    page_title="MoodMusic",
    page_icon="🎵",
    layout="wide"
)

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("moodmusic_dataset.csv")

try:
    df = cargar_datos()

    # Encabezado
    st.title("🎵 MoodMusic")
    st.subheader("Recomendador de Playlist según el Estado de Ánimo")
    st.write(
        "Descubre canciones de acuerdo con el estado de ánimo que selecciones."
    )

    # Indicadores
    total = len(df)
    estado_principal = df["estado_animo"].value_counts().idxmax()
    genero_principal = df["genero"].value_counts().idxmax()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total de canciones", total)
    col2.metric("Estado predominante", estado_principal)
    col3.metric("Género más frecuente", genero_principal)

    st.divider()

    # Gráfica por estado de ánimo
    st.subheader("Distribución de canciones por estado de ánimo")

    conteo_animo = df["estado_animo"].value_counts()
    st.bar_chart(conteo_animo)

    # Gráfica por género
    st.subheader("Top 10 de géneros musicales")

    conteo_generos = df["genero"].value_counts().head(10)
    st.bar_chart(conteo_generos)

    st.divider()

    # Filtro interactivo
    st.subheader("🎧 Encuentra tu playlist")

    estados = sorted(df["estado_animo"].dropna().unique())

    seleccion = st.selectbox(
        "¿Qué estado de ánimo deseas explorar?",
        estados
    )

    canciones = df[df["estado_animo"] == seleccion]

    st.write("Canciones encontradas:", len(canciones))

    st.dataframe(
        canciones[["cancion", "artista", "genero"]],
        use_container_width=True,
        hide_index=True
    )

    # Catálogo completo
    with st.expander("Consultar catálogo completo"):
        st.dataframe(
            df[["cancion", "artista", "genero", "estado_animo"]],
            use_container_width=True,
            hide_index=True
        )

except FileNotFoundError:
    st.error(
        "No se encontró moodmusic_dataset.csv. "
        "Verifica que esté dentro del repositorio."
    )

except Exception as e:
    st.error(f"Ocurrió un error al cargar la aplicación: {e}")
