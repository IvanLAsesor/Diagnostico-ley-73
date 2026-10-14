import streamlit as st
import re
from datetime import date
from fpdf import FPDF
import unicodedata
#* ==========================================*
#* CONFIGURACIÓN DE PÁGINA*
#* ==========================================*
st.set_page_config(
    page_title="Diagnóstico de Pensión Ley 73",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
#* ==========================================*
#* FIX PARA ERRORES DE REACT*
#* ==========================================*
st.markdown("""
<html lang="en" translate="no">
<meta name="google" content="notranslate" />
""", unsafe_allow_html=True)
#* ==========================================*
#* IDENTIDAD VISUAL*
#* ==========================================*
st.markdown("""
<style>
    :root {
        --navy: #17324F;
        --navy-light: #284968;
        --gold: #B99A55;
        --gold-light: #E8DDBF;
        --bg: #F7F8FA;
        --white: #FFFFFF;
        --text: #25364A;
        --muted: #64748B;
        --border: #E0E6ED;
        --green: #287653;
        --radius: 14px;
        --shadow: 0 3px 12px rgba(23, 50, 79, 0.045);
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1120px;
        padding: 2rem 2rem 3.5rem;
    }

    /* Tipografía: reglas específicas para evitar conflictos de contraste */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: var(--navy);
        letter-spacing: -0.025em;
    }

    .stApp p {
        color: var(--text);
        line-height: 1.7;
    }

    /* Encabezado principal */
    .main-header {
        background: linear-gradient(125deg, #10243B 0%, #193A5C 72%, #254968 100%);
        border: 1px solid rgba(185, 154, 85, 0.55);
        border-radius: 18px;
        padding: 2.2rem 2.3rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(23, 50, 79, 0.10);
    }

    .main-header .eyebrow {
        color: #E8D6A6 !important;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .main-header h1 {
        color: #FFFFFF !important;
        font-size: clamp(1.7rem, 3vw, 2.35rem);
        line-height: 1.22;
        font-weight: 750;
        letter-spacing: -0.035em;
        margin: 0;
    }

    .main-header p {
        color: #E0E8F0 !important;
        font-size: 0.98rem;
        max-width: 660px;
        line-height: 1.75;
        margin: 0.8rem 0 0;
    }

    .header-accent {
        height: 3px;
        width: 76px;
        background: var(--gold);
        margin-top: 1.4rem;
        border-radius: 2px;
    }

    /* Tarjetas informativas */
    .intro-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: var(--shadow);
    }

    .intro-title {
        color: var(--navy) !important;
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .intro-copy {
        color: var(--muted) !important;
        font-size: 0.92rem;
        line-height: 1.75;
    }

    /* Encabezados de sección */
    .section-heading {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        margin: 2rem 0 0.4rem;
    }

    .section-number {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        width: 36px;
        height: 36px;
        border-radius: 11px;
        background: #EAF0F6;
        color: var(--navy) !important;
        font-size: 0.82rem;
        font-weight: 800;
    }

    .section-title {
        color: var(--navy) !important;
        font-size: 1.2rem;
        font-weight: 750;
        line-height: 1.35;
    }

    .section-subtitle {
        color: var(--muted) !important;
        font-size: 0.9rem;
        line-height: 1.65;
        margin: 0.35rem 0 1.1rem 3.2rem;
    }

    /* Etiquetas de los campos */
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] label p,
    div[data-testid="stWidgetLabel"] label span,
    div[data-testid="stWidgetLabel"] > div > p,
    div[data-testid="stWidgetLabel"] > label {
        color: var(--navy) !important;
        font-weight: 600 !important;
        font-size: 0.91rem;
    }

    /* Texto de los campos, incluida la fecha de alta IMSS */
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="input"] input {
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        background-color: #FFFFFF !important;
        opacity: 1 !important;
        caret-color: var(--navy) !important;
    }

    /* El texto de ejemplo/placeholder debe seguir siendo legible */
    div[data-testid="stDateInput"] input::placeholder,
    div[data-baseweb="input"] input::placeholder {
        color: #7A8797 !important;
        -webkit-text-fill-color: #7A8797 !important;
        opacity: 1 !important;
    }

    /* Campos de captura */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: #FFFFFF;
        border-color: #CBD5E1;
        border-radius: 9px;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"]:focus-within {
        border-color: var(--gold);
        box-shadow: 0 0 0 2px rgba(185, 154, 85, 0.17);
    }

    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stCheckbox"] label span {
        color: var(--text) !important;
        font-weight: 500 !important;
    }

    /* Indicadores y resultados */
    .metric-mini {
        min-height: 118px;
        height: 100%;
        background: var(--white);
        border: 1px solid var(--border);
        border-top: 3px solid var(--gold);
        border-radius: var(--radius);
        padding: 1.25rem;
        box-shadow: var(--shadow);
    }

    .metric-mini .label {
        color: var(--muted) !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.045em;
        line-height: 1.5;
        margin-bottom: 0.7rem;
    }

    .metric-mini .value {
        color: var(--navy) !important;
        font-size: clamp(1.3rem, 2.2vw, 1.8rem);
        font-weight: 750;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }

    /* Mensajes informativos */
    .result-banner, .info-banner {
        padding: 1rem 1.15rem;
        margin: 1rem 0;
        border-radius: 11px;
        font-size: 0.91rem;
        line-height: 1.75;
    }

    .result-banner {
        background: #EDF5EF;
        border: 1px solid #D3E5D8;
        color: #285B40 !important;
    }

    .result-banner strong { color: #285B40 !important; }

    .info-banner {
        background: #EEF3F8;
        border: 1px solid #D8E3EF;
        color: #284968 !important;
    }

    .info-banner strong { color: var(--navy) !important; }

    /* Texto auxiliar */
    div[data-testid="stCaptionContainer"] p,
    div[data-testid="stCaptionContainer"] span {
        color: var(--muted) !important;
        font-size: 0.83rem;
        line-height: 1.6;
    }

    /* Desplegables y alertas */
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 11px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] summary {
        color: var(--navy);
        font-weight: 600;
    }

    div[data-testid="stAlert"] {
        border-radius: 11px;
        border-width: 1px;
    }

    /* Botón principal */
    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
        background: var(--navy) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--navy) !important;
        border-radius: 10px !important;
        min-height: 50px !important;
        padding: 0.8rem 1.3rem !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        transition: background 0.2s ease, border-color 0.2s ease;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {
        background: var(--navy-light) !important;
        border-color: var(--gold) !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] p,
    div[data-testid="stButton"] > button[kind="primary"] span,
    div[data-testid="stButton"] > button[kind="primary"] div {
        color: #FFFFFF !important;
    }

    /* Descarga del reporte */
    div[data-testid="stDownloadButton"] > button {
        background: #FFFFFF !important;
        color: var(--navy) !important;
        border: 1px solid var(--gold) !important;
        border-radius: 10px !important;
        min-height: 48px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background: #F1F4F7 !important;
        border-color: var(--navy) !important;
        color: var(--navy) !important;
    }

    div[data-testid="stDownloadButton"] > button p,
    div[data-testid="stDownloadButton"] > button span,
    div[data-testid="stDownloadButton"] > button div {
        color: var(--navy) !important;
    }

    /* Separadores y pie de página */
    hr {
        border-color: var(--border);
        margin: 1.8rem 0;
    }

    .app-footer {
        border-top: 1px solid var(--border);
        padding-top: 1.2rem;
        margin-top: 3rem;
        text-align: center;
        color: var(--muted) !important;
        font-size: 0.82rem;
        line-height: 1.8;
    }

    .app-footer strong { color: var(--navy) !important; }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            transition-duration: 0.01ms !important;
            animation-duration: 0.01ms !important;
        }
    }

    /* Adaptación a celulares */
    @media (max-width: 700px) {
        .block-container { padding: 1rem 0.85rem 2rem; }
        .main-header { padding: 1.45rem 1.2rem; border-radius: 14px; }
        .intro-card { padding: 1.1rem; }
        .section-heading { margin-top: 1.6rem; }
        .section-title { font-size: 1.05rem; }
        .section-subtitle { margin-left: 0; font-size: 0.86rem; }
        .metric-mini { min-height: 100px; padding: 0.9rem; }
        .metric-mini .label { font-size: 0.69rem; }
        .metric-mini .value { font-size: 1.15rem; }
    }
</style>
""", unsafe_allow_html=True)
#* ==========================================*
#* FUNCIONES DE PRESENTACIÓN*
#* ==========================================*
def texto_pdf_seguro(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.encode("latin-1", errors="replace").decode("latin-1")
def metric_mini(label, value):
    st.markdown(f"""
    <div class="metric-mini">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)
def encabezado_seccion(numero, titulo, subtitulo=""):
    st.markdown(f"""
    <div class="section-heading">
        <div class="section-number">{numero}</div>
        <div class="section-title">{titulo}</div>
    </div>
    """, unsafe_allow_html=True)
    if subtitulo:
        st.markdown(
            f'<div class="section-subtitle">{subtitulo}</div>',
            unsafe_allow_html=True
        )
#* ==========================================*
#* CONSTANTES Y TABLAS*
#* ==========================================*
UMA_DIARIA_2026 = 117.31
PMG_MENSUAL_2026 = 10636.54
FACTOR_FOX = 1.11
TOPE_UMA_MOD40 = 25
CUOTA_MOD40 = 0.14438
TABLA_ART167 = [
    (0, 1, 0.80, 0.00563),
    (1.01, 1.25, 0.7711, 0.00814),
    (1.26, 1.50, 0.5518, 0.01178),
    (1.51, 1.75, 0.4923, 0.01430),
    (1.76, 2.00, 0.4267, 0.01615),
    (2.01, 2.25, 0.3765, 0.01756),
    (2.26, 2.50, 0.3368, 0.01868),
    (2.51, 2.75, 0.3048, 0.01958),
    (2.76, 3.00, 0.2783, 0.02033),
    (3.01, 3.25, 0.2560, 0.02096),
    (3.26, 3.50, 0.2370, 0.02149),
    (3.51, 3.75, 0.2207, 0.02195),
    (3.76, 4.00, 0.2065, 0.02235),
    (4.01, 4.25, 0.1939, 0.02271),
    (4.26, 4.50, 0.1829, 0.02302),
    (4.51, 4.75, 0.1730, 0.02330),
    (4.76, 5.00, 0.1641, 0.02355),
    (5.01, 5.25, 0.1561, 0.02377),
    (5.26, 5.50, 0.1488, 0.02398),
    (5.51, 5.75, 0.1422, 0.02416),
    (5.76, 6.00, 0.1362, 0.02433),
    (6.01, 999, 0.1300, 0.02450),
]
TABLA_EDAD = {60: 0.75, 61: 0.80, 62: 0.85, 63: 0.90, 64: 0.95, 65: 1.00}
TABLA_RESIDUO = [(0, 0.0), (13, 0.005), (26.1, 0.01)]
#* ==========================================*
#* ENCABEZADO PRINCIPAL (estilos inline para garantizar visibilidad)*
#* ==========================================*
col_logo, col_titulo = st.columns([0.85, 5.15])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except Exception:
        st.markdown(
            '<div style="font-size:2.6rem;text-align:center;'
            'padding-top:1rem;color:#1E3A5F;">◆</div>',
            unsafe_allow_html=True
        )
with col_titulo:
    st.markdown("""
    <div class="main-header">
        <div class="eyebrow">Planeación patrimonial · Retiro</div>
        <h1>Diagnóstico de Pensión Ley 73</h1>
        <p>Comprende tu escenario de retiro, estima tu pensión y explora alternativas para complementar tus ingresos.</p>
        <div class="header-accent"></div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<div class="intro-card">
    <div class="intro-title">Tu retiro merece una estrategia.</div>
    <div class="intro-copy">
        Captura tu información laboral para construir una estimación
        orientativa. Los resultados dependen de los datos ingresados
        y de los supuestos de esta herramienta.
    </div>
</div>
""", unsafe_allow_html=True)
#* ==========================================*
#* AVISO DE PRIVACIDAD*
#* ==========================================*
with st.expander("CONSULTAR AVISO DE PRIVACIDAD"):
    st.markdown("""
    **Responsable:** Gabril Iván Lenz C, asesor patrimonial independiente.
    **Contacto:** ivanlenz@proton.me
    **Datos que se tratarán:** Esta herramienta no solicita nombre,
    teléfono ni datos de identificación personal. Únicamente captura
    datos laborales y financieros necesarios para el cálculo.
    **Finalidad:** Elaborar un diagnóstico estimado de pensión y generar
    un reporte en PDF. No se usarán para contactarte, ni para fines
    publicitarios, ni se compartirán con terceros.
    **Derechos ARCO:** Puedes solicitar acceso, rectificación,
    cancelación u oposición enviando un correo a ivanlenz@proton.me.
    """)
acepta_privacidad = st.checkbox(
    "He leído el Aviso de Privacidad y autorizo el uso de mis datos "
    "financieros para elaborar mi diagnóstico.",
    value=False
)
if acepta_privacidad:
    #* ==========================================*
    #* FASE 1*
    #* ==========================================*
    encabezado_seccion(
        "01",
        "Identifica tu régimen",
        "El primer paso es confirmar la fecha de tu primera cotización."
    )
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_alta = st.date_input(
            "Fecha de tu primera cotización ante el IMSS",
            value=date(1990, 1, 1),
            min_value=date(1960, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY",
            help="Consulta tu Constancia de Semanas Cotizadas."
        )
        st.caption("Fecha de referencia: 1 de julio de 1997.")
    with col_f2:
        estatus_laboral = st.radio(
            "Estatus actual ante el IMSS",
            ["Vigente (trabajando)", "Dado de baja"],
            horizontal=True
        )
    es_ley73 = fecha_alta < date(1997, 7, 1)
    if not es_ley73:
        st.error(
            "**No aplicas para Ley 73.** Tu primera cotización fue "
            "el 1 de julio de 1997 o después. Te corresponde revisar "
            "el régimen de **Ley 97**."
        )
        st.stop()
    else:
        st.markdown("""
        <div class="result-banner">
            <strong>Régimen identificado:</strong>
            Ley 73, de acuerdo con la fecha ingresada.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    #* ==========================================*
    #* FASE 2*
    #* ==========================================*
    encabezado_seccion(
        "02",
        "Tus datos",
        "Información personal que influye en el escenario de retiro."
    )
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        edad_actual = st.number_input(
            "Edad actual", min_value=18, max_value=80, value=55, step=1
        )
        edad_jubilacion = st.radio(
            "Edad de retiro deseada",
            [60, 61, 62, 63, 64, 65],
            horizontal=True,
            index=0,
            help="El cálculo aplica los porcentajes por edad definidos."
        )
    with col_d2:
        sexo = st.radio("Sexo", ["Hombre", "Mujer"], horizontal=True)
        tiene_conyuge = st.radio(
            "¿Tienes esposa/o?",
            ["No", "Sí"],
            horizontal=True,
            index=1
        )
        num_hijos = st.number_input(
            "Hijos menores o estudiando",
            min_value=0, value=0, step=1
        )
        num_padres = st.number_input(
            "Padres dependientes",
            min_value=0, value=0, step=1
        )
    #* ==========================================*
    #* FASE 3*
    #* ==========================================*
    encabezado_seccion(
        "03",
        "Datos de cotización",
        "Utiliza la información de tu constancia y estado de cuenta."
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        semanas_actuales = st.number_input(
            "Semanas cotizadas actuales",
            min_value=0, value=1255, step=1
        )
        salario_diario = st.number_input(
            "Salario diario promedio (últimas 250 semanas)",
            min_value=0.0, value=1198.98, step=10.0, format="%.2f"
        )
    with col_c2:
        densidad = st.slider(
            "Densidad de cotización futura",
            0.0, 1.0, 0.8, 0.05
        )
        st.caption(
            "Proporción del tiempo que estimas continuar cotizando. "
            "Si ya no trabajarás, selecciona 0%."
        )
    #* ==========================================*
    #* PENSIÓN IDEAL*
    #* ==========================================*
    st.markdown("---")
    encabezado_seccion(
        "04",
        "Tu pensión ideal",
        "Define el ingreso mensual que te gustaría recibir durante el retiro."
    )
    pension_ideal = st.number_input(
        "Monto mensual deseado al retirarte (MXN)",
        min_value=0.0,
        value=round(salario_diario * 30.4, -2),
        step=1000.0,
        format="%.2f"
    )
    #* ==========================================*
    #* FASE 4*
    #* ==========================================*
    st.markdown("---")
    encabezado_seccion(
        "05",
        "Diagnóstico de elegibilidad",
        "Una primera aproximación a tus semanas al momento del retiro."
    )
    anios_hasta_jubilacion = max(0, edad_jubilacion - edad_actual)
    semanas_futuras = int(anios_hasta_jubilacion * 52 * densidad)
    semanas_proyectadas = semanas_actuales + semanas_futuras
    if estatus_laboral == "Dado de baja":
        anios_cotizados = semanas_actuales / 52
        conservacion_anios = max(1, anios_cotizados / 4)
        st.info(
            f"Conservación de derechos orientativa: aproximadamente "
            f"{conservacion_anios:.1f} años después de la baja. "
            f"Esta estimación no determina por sí misma tu derecho "
            f"a pensionarte."
        )
    else:
        st.info(
            "Para tramitar una pensión bajo Ley 73 debes considerar "
            "la baja ante el IMSS y los demás requisitos aplicables."
        )
    if semanas_proyectadas < 500:
        st.error(
            f"No alcanzas el mínimo de 500 semanas con estos datos. "
            f"Tu proyección es de {semanas_proyectadas} semanas."
        )
        st.stop()
    else:
        metric_mini("Semanas proyectadas", f"{semanas_proyectadas:,.0f}")
    #* ==========================================*
    #* BOTÓN DE CÁLCULO*
    #* ==========================================*
    st.markdown("---")
    if st.button("CALCULAR MI PENSIÓN LEY 73", type="primary"):
        with st.spinner("Preparando tu diagnóstico..."):
            vsm = salario_diario / UMA_DIARIA_2026
            pct_cuantia, pct_incremento = 0.13, 0.0245
            for vmin, vmax, c, i in TABLA_ART167:
                if vmin <= vsm <= vmax:
                    pct_cuantia, pct_incremento = c, i
                    break
            cuantia_diaria = salario_diario * pct_cuantia
            cuantia_anual = cuantia_diaria * 365
            incremento_diario = salario_diario * pct_incremento
            incremento_anual_previo = incremento_diario * 365
            semanas_posteriores = max(0, semanas_proyectadas - 500)
            anios_completos = int(semanas_posteriores // 52)
            semanas_residuo = semanas_posteriores - (anios_completos * 52)
            anios_residuo = 0.0
            for umbral, valor in TABLA_RESIDUO:
                if semanas_residuo <= umbral:
                    anios_residuo = valor
                    break
            total_anios = anios_completos + anios_residuo
            incremento_anual = incremento_anual_previo * total_anios
            cuantia_anual_pension = cuantia_anual + incremento_anual
            ayuda_conyuge = cuantia_anual_pension * 0.15 if tiene_conyuge == "Sí" else 0
            ayuda_hijos = cuantia_anual_pension * 0.10 * num_hijos
            if tiene_conyuge == "Sí" or num_hijos > 0:
                ayuda_padres = 0
            else:
                ayuda_padres = cuantia_anual_pension * 0.20 * num_padres
            if tiene_conyuge == "No" and num_hijos == 0 and num_padres == 0:
                ayuda_soledad = cuantia_anual_pension * 0.15
            else:
                ayuda_soledad = 0
            total_ayudas = ayuda_conyuge + ayuda_hijos + ayuda_padres + ayuda_soledad
            pension_ayudas = cuantia_anual_pension + total_ayudas
            pension_vejez_anual = pension_ayudas * FACTOR_FOX
            pct_edad = TABLA_EDAD.get(edad_jubilacion, 1.00)
            pension_final_anual = pension_vejez_anual * pct_edad
            pension_final_mensual = pension_final_anual / 12
            aplica_pmg = pension_final_mensual < PMG_MENSUAL_2026
            if aplica_pmg:
                pension_final_mensual = PMG_MENSUAL_2026
            #* ==========================================*
            #* RESULTADOS*
            #* ==========================================*
            st.markdown("---")
            encabezado_seccion(
                "06",
                "Tu diagnóstico",
                "Este es el escenario estimado con la información ingresada."
            )
            tasa_reemplazo_valor = (
                f"{(pension_final_mensual / (salario_diario * 30.4)) * 100:.1f}%"
                if salario_diario > 0 else "N/D"
            )
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                metric_mini("Pensión mensual estimada", f"${pension_final_mensual:,.0f}")
            with col_b:
                metric_mini("Tasa de reemplazo", tasa_reemplazo_valor)
            with col_c:
                metric_mini("Semanas proyectadas", f"{semanas_proyectadas:,.0f}")
            if aplica_pmg:
                st.info(
                    f"El cálculo aplicó el valor de referencia de "
                    f"PMG configurado para 2026: "
                    f"${PMG_MENSUAL_2026:,.2f} MXN."
                )
            with st.expander("CONSULTAR DESGLOSE DEL CÁLCULO"):
                st.write(f"VSM: {vsm:.4f}")
                st.write(f"Cuantía básica: {pct_cuantia * 100:.2f}%")
                st.write(f"Incremento anual: {pct_incremento * 100:.3f}%")
                st.write(f"Cuantía anual: ${cuantia_anual:,.2f}")
                st.write(f"Años posteriores a 500 semanas: {total_anios:.2f}")
                st.write(f"Incremento total: ${incremento_anual:,.2f}")
                st.write(f"Cuantía anual de pensión: ${cuantia_anual_pension:,.2f}")
                st.write(f"Total de ayudas: ${total_ayudas:,.2f}")
                st.write(f"Factor Fox (11%): +${pension_vejez_anual - pension_ayudas:,.2f}")
                st.write(f"Porcentaje por edad: {pct_edad * 100:.0f}%")
                st.write(f"Pensión final mensual: ${pension_final_mensual:,.2f}")
            #* ==========================================*
            #* AHORRO COMPLEMENTARIO*
            #* ==========================================*
            st.markdown("---")
            encabezado_seccion(
                "07",
                "Complemento con ahorro mensual",
                "Explora cómo un ahorro adicional podría complementar "
                "el ingreso estimado de tu pensión."
            )
            brecha_mensual = max(0.0, pension_ideal - pension_final_mensual)
            if brecha_mensual > 0:
                st.markdown(
                    f"""
                    <div class="info-banner">
                        <strong>Brecha mensual estimada</strong><br>
                        Pensión ideal: <strong>${pension_ideal:,.2f}</strong><br>
                        Pensión Ley 73: <strong>${pension_final_mensual:,.2f}</strong><br>
                        Diferencia: <strong>${brecha_mensual:,.2f} MXN</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col_ppr1, col_ppr2 = st.columns([2, 1])
                with col_ppr1:
                    aportacion_ppr = st.number_input(
                        "Aportación mensual al ahorro complementario (MXN)",
                        min_value=2000.0,
                        value=max(2000.0, round(brecha_mensual * 0.3, -2)),
                        step=500.0,
                        format="%.2f"
                    )
                with col_ppr2:
                    st.markdown("""
                    <div class="metric-mini">
                        <div class="label">Rendimiento referencial</div>
                        <div class="value">11%</div>
                        <div style="font-size:.76rem;color:#5A6B82;margin-top:.4rem;">
                            Portafolio indexado
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with st.expander("CONFIGURACIÓN AVANZADA · SOLO ASESOR"):
                    tasa_retorno = st.slider(
                        "Ajustar rendimiento anual estimado (%)",
                        min_value=5.0, max_value=12.0, value=11.0, step=0.5
                    ) / 100
                if "tasa_retorno" not in dir():
                    tasa_retorno = 0.11
                tasa_diaria = (1 + tasa_retorno) ** (1 / 365) - 1
                dias_restantes = max(1, anios_hasta_jubilacion * 365)
                aportacion_diaria = aportacion_ppr / 30.4
                if tasa_diaria > 0:
                    factor_diario = ((1 + tasa_diaria) ** dias_restantes - 1) / tasa_diaria
                    capital_acumulado = aportacion_diaria * factor_diario
                else:
                    capital_acumulado = aportacion_diaria * dias_restantes
                ae_edad = {
                    60: 17.2, 61: 16.8, 62: 16.4,
                    63: 16.0, 64: 15.6, 65: 15.2
                }.get(edad_jubilacion, 15.2)
                complemento_mensual = (capital_acumulado / (ae_edad * (1 + 0.02))) / 12
                pension_total = pension_final_mensual + complemento_mensual
                brecha_restante = max(0.0, pension_ideal - pension_total)
                st.markdown("---")
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    metric_mini("Aportación mensual", f"${aportacion_ppr:,.0f}")
                with col_r2:
                    metric_mini("Complemento estimado", f"${complemento_mensual:,.0f}")
                with col_r3:
                    metric_mini("Pensión total estimada", f"${pension_total:,.0f}")
                if brecha_restante > 0:
                    st.info(
                        f"Con esta aportación todavía quedaría una "
                        f"diferencia estimada de "
                        f"${brecha_restante:,.2f} MXN al mes."
                    )
                else:
                    st.success("La proyección alcanza o supera tu pensión ideal.")
                st.caption(
                    f"Proyección con capitalización diaria al "
                    f"{tasa_retorno * 100:.1f}% anual. "
                    f"Rendimiento hipotético, no garantizado."
                )
            else:
                st.success(
                    "La pensión estimada cubre o supera el monto "
                    "mensual que definiste como ideal."
                )
            #* ==========================================*
            #* MODALIDAD 40*
            #* ==========================================*
            if estatus_laboral == "Dado de baja":
                st.markdown("---")
                encabezado_seccion(
                    "08",
                    "Simulador de Modalidad 40",
                    "Explora el costo mensual estimado con el salario "
                    "base de cotización que selecciones."
                )
                st.caption(
                    "Cuota de referencia configurada para 2026: "
                    "14.438% del SBC mensual."
                )
                sbc_elegido = st.number_input(
                    "SBC mensual que elegirías",
                    min_value=salario_diario * 30.4,
                    max_value=UMA_DIARIA_2026 * TOPE_UMA_MOD40 * 30.4,
                    value=UMA_DIARIA_2026 * TOPE_UMA_MOD40 * 30.4,
                    step=1000.0,
                    format="%.2f"
                )
                cuota_mensual = sbc_elegido * CUOTA_MOD40
                sbc_diario_elevado = sbc_elegido / 30.4
                vsm_elevado = sbc_diario_elevado / UMA_DIARIA_2026
                pct_cuantia_elevado = 0.13
                pct_incremento_elevado = 0.0245
                for vmin, vmax, c, i in TABLA_ART167:
                    if vmin <= vsm_elevado <= vmax:
                        pct_cuantia_elevado = c
                        pct_incremento_elevado = i
                        break
                cuantia_diaria_elevada = sbc_diario_elevado * pct_cuantia_elevado
                cuantia_anual_elevada = cuantia_diaria_elevada * 365
                incremento_diario_elevado = sbc_diario_elevado * pct_incremento_elevado
                incremento_anual_previo_elevado = incremento_diario_elevado * 365
                incremento_anual_elevado = incremento_anual_previo_elevado * total_anios
                cuantia_anual_pension_elevada = cuantia_anual_elevada + incremento_anual_elevado
                ayuda_conyuge_elevado = cuantia_anual_pension_elevada * 0.15 if tiene_conyuge == "Sí" else 0
                ayuda_hijos_elevado = cuantia_anual_pension_elevada * 0.10 * num_hijos
                if tiene_conyuge == "Sí" or num_hijos > 0:
                    ayuda_padres_elevado = 0
                else:
                    ayuda_padres_elevado = cuantia_anual_pension_elevada * 0.20 * num_padres
                if tiene_conyuge == "No" and num_hijos == 0 and num_padres == 0:
                    ayuda_soledad_elevado = cuantia_anual_pension_elevada * 0.15
                else:
                    ayuda_soledad_elevado = 0
                total_ayudas_elevado = ayuda_conyuge_elevado + ayuda_hijos_elevado + ayuda_padres_elevado + ayuda_soledad_elevado
                pension_ayudas_elevada = cuantia_anual_pension_elevada + total_ayudas_elevado
                pension_vejez_anual_elevada = pension_ayudas_elevada * FACTOR_FOX
                pension_final_mensual_elevada = (pension_vejez_anual_elevada * pct_edad) / 12
                if pension_final_mensual_elevada < PMG_MENSUAL_2026:
                    pension_final_mensual_elevada = PMG_MENSUAL_2026
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    metric_mini("Cuota mensual estimada", f"${cuota_mensual:,.0f}")
                with col_m2:
                    aumento = pension_final_mensual_elevada - pension_final_mensual
                    metric_mini("Aumento estimado de pensión", f"+${aumento:,.0f}")
            #* ==========================================*
            #* PDF*
            #* ==========================================*
            st.markdown("---")
            encabezado_seccion(
                "09",
                "Tu reporte",
                "Descarga un resumen de los resultados calculados."
            )
            class PDF(FPDF):
                def header(self):
                    self.set_fill_color(15, 43, 76)
                    self.rect(0, 0, 210, 25, "F")
                    self.set_fill_color(201, 169, 97)
                    self.rect(0, 25, 210, 1.2, "F")
                    try:
                        self.image("logo.png", x=12, y=5, w=15)
                    except Exception:
                        pass
                    self.set_text_color(255, 255, 255)
                    self.set_font("Helvetica", "B", 12)
                    self.set_xy(32, 7)
                    self.cell(165, 6, "DIAGNOSTICO DE PENSION LEY 73", ln=True, align="L")
                    self.set_font("Helvetica", "", 8)
                    self.set_text_color(220, 228, 237)
                    self.set_x(32)
                    self.cell(165, 5, "PLANEACION PATRIMONIAL | REPORTE INFORMATIVO", ln=True, align="L")
                    self.set_text_color(15, 43, 76)
                    self.set_y(34)
                def footer(self):
                    self.set_y(-17)
                    self.set_draw_color(216, 222, 231)
                    self.line(12, self.get_y(), 198, self.get_y())
                    self.set_y(-14)
                    self.set_font("Helvetica", "", 7)
                    self.set_text_color(90, 107, 130)
                    self.cell(0, 5, texto_pdf_seguro(f"Pagina {self.page_no()} | Ivan Lenz - Asesor Patrimonial"), align="C")
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=22)
            pdf.set_margins(14, 34, 14)
            pdf.add_page()
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(15, 43, 76)
            def titulo_pdf(titulo):
                pdf.ln(2)
                pdf.set_fill_color(235, 240, 247)
                pdf.set_text_color(15, 43, 76)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 8, texto_pdf_seguro(titulo), ln=True, fill=True)
                pdf.set_text_color(15, 43, 76)
                pdf.set_font("Helvetica", size=9)
                pdf.ln(2)
            def linea_pdf(etiqueta, valor):
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(67, 6, texto_pdf_seguro(etiqueta))
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(0, 6, texto_pdf_seguro(valor), ln=True)
            titulo_pdf("1. DATOS DEL CALCULO")
            linea_pdf("Semanas proyectadas:", f"{semanas_proyectadas:.0f}")
            linea_pdf("Salario diario promedio:", f"${salario_diario:,.2f} MXN")
            linea_pdf("Edad de retiro:", f"{edad_jubilacion} anos")
            linea_pdf("VSM:", f"{vsm:.4f}")
            linea_pdf("Estatus laboral:", estatus_laboral)
            pdf.ln(3)
            titulo_pdf("2. RESULTADO DE LA PENSION")
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(15, 43, 76)
            pdf.cell(0, 9, texto_pdf_seguro(f"PENSION MENSUAL ESTIMADA: ${pension_final_mensual:,.2f} MXN"), ln=True)
            pdf.set_text_color(15, 43, 76)
            pdf.set_font("Helvetica", size=9)
            linea_pdf("Tasa de reemplazo:", tasa_reemplazo_valor)
            if aplica_pmg:
                linea_pdf("Referencia PMG:", f"${PMG_MENSUAL_2026:,.2f} MXN")
            pdf.ln(3)
            if brecha_mensual > 0:
                titulo_pdf("3. COMPLEMENTO CON AHORRO")
                linea_pdf("Pension ideal:", f"${pension_ideal:,.2f} MXN")
                linea_pdf("Brecha mensual:", f"${brecha_mensual:,.2f} MXN")
                linea_pdf("Aportacion mensual:", f"${aportacion_ppr:,.2f} MXN")
                linea_pdf("Complemento estimado:", f"${complemento_mensual:,.2f} MXN")
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 7, texto_pdf_seguro(f"PENSION TOTAL ESTIMADA: ${pension_total:,.2f} MXN"), ln=True)
                pdf.set_font("Helvetica", size=9)
                pdf.ln(3)
            if estatus_laboral == "Dado de baja":
                titulo_pdf("4. ESCENARIO MODALIDAD 40")
                linea_pdf("SBC mensual seleccionado:", f"${sbc_elegido:,.2f} MXN")
                linea_pdf("Cuota mensual estimada:", f"${cuota_mensual:,.2f} MXN")
                linea_pdf("Aumento estimado de pension:", f"${aumento:,.2f} MXN")
                pdf.ln(3)
            titulo_pdf("NOTAS IMPORTANTES")
            pdf.set_font("Helvetica", "", 8)
            pdf.multi_cell(
                0, 4.5,
                texto_pdf_seguro(
                    "Este documento es una estimacion informativa "
                    "basada en los datos proporcionados y los supuestos "
                    "de la herramienta. No constituye una resolucion "
                    "oficial ni garantiza el monto de una pension. "
                    "La procedencia y cuantia de la pension, las "
                    "asignaciones familiares, la conservacion de "
                    "derechos y las condiciones de Modalidad 40 deben "
                    "confirmarse conforme a la normativa aplicable "
                    "y ante el IMSS."
                )
            )
            pdf_output = bytes(pdf.output())
            st.download_button(
                label="DESCARGAR MI REPORTE PDF",
                data=pdf_output,
                file_name=f"Diagnostico_Ley73_{date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.caption(
                "Estimación informativa. El IMSS es la autoridad "
                "competente para determinar el derecho y el monto "
                "de la pensión."
            )
else:
    st.markdown("""
    <div class="intro-card">
        <div class="intro-title">Comienza tu diagnóstico</div>
        <div class="intro-copy">
            Para continuar, consulta el Aviso de Privacidad y marca
            la casilla de autorización. Después podrás ingresar tus
            datos y generar una estimación orientativa.
        </div>
    </div>
    """, unsafe_allow_html=True)
#* ==========================================*
#* PIE DE PÁGINA*
#* ==========================================*
st.markdown("""
<div class="app-footer">
    <strong>Diagnóstico de Pensión Ley 73</strong><br>
    Herramienta de orientación y planeación patrimonial.<br>
    Los resultados son hipotéticos y no sustituyen una resolución del IMSS.
</div>
""", unsafe_allow_html=True)
