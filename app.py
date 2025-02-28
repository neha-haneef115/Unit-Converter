import streamlit as st
from pint import UnitRegistry

st.set_page_config(page_title="Unit Converter", layout="wide")

ureg = UnitRegistry()

st.markdown(
    """
    <style>
    .stApp {
        background-color: #192436;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #04B6D2;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 28px;
        text-align: center;
        color: #E0E0E0;
    }
    .stButton>button {
        margin-top: 24px;
        background-color: #04B6D2;
        color: white;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #0396A6;
        color:rgb(231, 224, 224);
        transform: scale(1.05);
    }
    .custom-success {
        background-color: #F1E3D3;
        color: black;
        font-size: 18px;
        font-weight:600;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        margin-top: 20px;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #4A90E2;
        margin-bottom: 10px;
    }
    .sidebar-history {
        background-color: #2F3949;
        color: white;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 5px;
        text-align: center;
        border-left: 5px solid #04B6D2;
    }
    [data-testid="stSidebar"] {
        background-color: #2F3949;
        border-right: 1px solid #4A90E2;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label {
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sidebar-title">Conversion History</div>', unsafe_allow_html=True)
if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Clear History"):
    st.session_state.history = []

st.markdown('<div class="main-title">Unit Converter</div>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart, Simple, and Hassle-Free Unit Conversion.</p>', unsafe_allow_html=True)

categories = {
    "Length": ["meter", "centimeter", "millimeter", "kilometer", "inch", "foot", "yard", "mile"],
    "Mass": ["kilogram", "gram", "milligram", "pound", "ounce"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day"]
}

category = st.selectbox("Category", list(categories.keys()))
value = st.number_input("Enter Value", min_value=0.0, format="%.2f")
col1, col2, col3 = st.columns([1, 0.2, 1])

to_unit = col1.selectbox("To", categories[category], key="to_unit")
from_unit = col3.selectbox("From", categories[category], key="from_unit")

def swap_units():
    st.session_state.to_unit, st.session_state.from_unit = st.session_state.from_unit, st.session_state.to_unit

col2.button("⇄", on_click=swap_units, key="swap")

if st.button("Convert", key="convert_button"):
    try:
        if category == "Temperature":
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value
        else:
            result = ureg.Quantity(value, from_unit).to(to_unit).magnitude
        
        st.markdown(
            f"""
            <div class="custom-success">
                 {value} {to_unit} = {result:.2f} {from_unit}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.history.append(f"{value} {to_unit} = {result:.2f} {from_unit}")

    except Exception as e:
        st.error("Invalid conversion")

if st.session_state.history:
    st.sidebar.markdown("### Past Conversions:")
    for entry in st.session_state.history[-5:]:
        st.sidebar.markdown(f'<div class="sidebar-history">{entry}</div>', unsafe_allow_html=True)
