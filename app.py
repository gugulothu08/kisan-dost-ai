import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from pathlib import Path
import json
import base64
import random


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Kisan Dost",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# FOLDERS
# =========================================================

BASE = Path(__file__).parent

ASSET = BASE / "assets" / "farm_background.jpg"

if not ASSET.exists():
    png_file = BASE / "assets" / "farm_background.png"
    if png_file.exists():
        ASSET = png_file

DATA = BASE / "data"
UPLOADS = BASE / "uploads"

DATA.mkdir(exist_ok=True)
UPLOADS.mkdir(exist_ok=True)


# =========================================================
# BACKGROUND IMAGE
# =========================================================

def image_to_base64(path):

    if not path.exists():
        return ""

    extension = path.suffix.lower().replace(".", "")

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode()

    return f"data:image/{extension};base64,{encoded}"


BACKGROUND_IMAGE = image_to_base64(ASSET)


# =========================================================
# CSS
# =========================================================

CSS = """
<style>

/* Remove Streamlit default elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
}


/* Main application */

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1400px !important;
}


/* Login page */

.login-title {
    text-align: center;
    color: #075c3b;
    font-size: 34px;
    font-weight: 900;
    margin-bottom: 0px;
}

.login-subtitle {
    text-align: center;
    color: #66786f;
    font-size: 14px;
    margin-bottom: 15px;
}

.login-icons {
    text-align: center;
    font-size: 38px;
    margin-bottom: 4px;
}

.login-badge {
    background: #eaf8ef;
    color: #087447;
    padding: 9px;
    border-radius: 15px;
    text-align: center;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 10px;
}


/* Top bar */

.top-header {
    background: rgba(255,255,255,0.97);
    border-radius: 0 0 20px 20px;
    padding: 10px 20px;
    margin-bottom: 10px;
    box-shadow: 0 4px 18px rgba(0,70,40,0.10);
}

.logo {
    font-size: 28px;
    font-weight: 900;
    color: #075c3b;
}

.tagline {
    color: #698078;
    font-size: 12px;
}


/* Cards */

.card {
    background: white;
    border: 1px solid #dcece3;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 7px 22px rgba(0,70,40,0.07);
}

.section-title {
    color: #075c3b;
    font-size: 23px;
    font-weight: 900;
    margin-top: 15px;
    margin-bottom: 12px;
}


/* Hero */

.hero {
    background: linear-gradient(
        135deg,
        #075c3b,
        #0a8b55
    );

    color: white;

    border-radius: 22px;

    padding: 25px;

    margin-bottom: 15px;

    box-shadow:
        0 12px 30px rgba(0,70,40,0.20);
}


/* Metric cards */

.metric-card {
    background: #f1faf4;
    border: 1px solid #d8ede0;
    border-radius: 18px;
    padding: 15px;
    text-align: center;
    min-height: 120px;
}


/* Marketplace cards */

.market-card {
    background: white;
    border: 1px solid #dcece3;
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 10px;
    box-shadow: 0 5px 18px rgba(0,60,30,0.06);
}


/* Alerts */

.alert-good {
    background: #eaf8ef;
    border-left: 5px solid #0b955a;
    border-radius: 12px;
    padding: 13px;
}

.alert-warning {
    background: #fff7df;
    border-left: 5px solid #e4a600;
    border-radius: 12px;
    padding: 13px;
}

.alert-danger {
    background: #fff0ef;
    border-left: 5px solid #d64b43;
    border-radius: 12px;
    padding: 13px;
}


/* Navigation */

[data-testid="stRadio"] > div {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
}

[data-testid="stRadio"] label {
    background: #f3faf6;
    border: 1px solid #d7e9df;
    border-radius: 13px;
    padding: 7px 11px;
    color: #075c3b;
    font-weight: 700;
}

[data-testid="stRadio"] label:hover {
    background: #e1f4e8;
}


/* Buttons */

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
}


/* Footer */

.app-footer {
    text-align: center;
    color: #718078;
    font-size: 11px;
    padding: 15px;
}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# BACKGROUND STYLE
# =========================================================

if BACKGROUND_IMAGE:

    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:

                linear-gradient(
                    rgba(0,45,25,0.25),
                    rgba(0,45,25,0.25)
                ),

                url("{BACKGROUND_IMAGE}");

            background-size: cover;

            background-position: center;

            background-attachment: fixed;

            min-height: 100vh;

        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = [
    "English",
    "తెలుగు",
    "हिन्दी",
    "தமிழ்",
    "ಕನ್ನಡ",
    "मराठी",
    "বাংলা",
    "ਪੰਜਾਬੀ",
    "ગુજરાતી",
    "অসমীয়া",
    "ଓଡ଼ିଆ",
    "മലയാളം"
]


# =========================================================
# NAVIGATION
# =========================================================

SERVICES = [

    "Home",
    "Farm Setup",
    "Weather",
    "Mandi Prices",
    "Crop Advice",
    "Soil Health",
    "Plant Doctor",
    "Crop Protection",
    "Irrigation",
    "Cost & Profit",
    "Crop Diary",
    "Crop Rotation",
    "What-If",
    "Buy & Sell",
    "Agri Store",
    "Dealers",
    "Kisan Forum",
    "Schemes & News"

]


TELUGU_NAV = {

    "Home": "హోమ్",
    "Farm Setup": "ఫారం వివరాలు",
    "Weather": "వాతావరణం",
    "Mandi Prices": "మార్కెట్ ధరలు",
    "Crop Advice": "పంట సలహా",
    "Soil Health": "నేల ఆరోగ్యం",
    "Plant Doctor": "మొక్కల డాక్టర్",
    "Crop Protection": "పంట రక్షణ",
    "Irrigation": "నీటిపారుదల",
    "Cost & Profit": "ఖర్చు & లాభం",
    "Crop Diary": "పంట డైరీ",
    "Crop Rotation": "పంట మార్పిడి",
    "What-If": "ఏమైతే?",
    "Buy & Sell": "కొనండి & అమ్మండి",
    "Agri Store": "వ్యవసాయ స్టోర్",
    "Dealers": "డీలర్లు",
    "Kisan Forum": "రైతు వేదిక",
    "Schemes & News": "పథకాలు & వార్తలు"

}


def translate(text):

    if st.session_state.language == "తెలుగు":

        return TELUGU_NAV.get(text, text)

    return text


# =========================================================
# CROPS
# =========================================================

CROPS = [

    "Rice",
    "Cotton",
    "Maize",
    "Chilli",
    "Tomato",
    "Groundnut",
    "Turmeric",
    "Paddy",
    "Wheat",
    "Soybean"

]


MARKETS = [

    "Warangal",
    "Hyderabad",
    "Karimnagar",
    "Nizamabad",
    "Khammam"

]


# =========================================================
# MANDI DATA
# =========================================================

MARKET_PRICES = {

    "Rice": [2650, 2780, 2920],

    "Cotton": [6900, 7350, 7800],

    "Maize": [2100, 2280, 2450],

    "Chilli": [12500, 14200, 16500],

    "Tomato": [1800, 2300, 3100],

    "Groundnut": [5600, 6100, 6800],

    "Turmeric": [10800, 12100, 13600],

    "Paddy": [2550, 2720, 2890],

    "Wheat": [2350, 2490, 2650],

    "Soybean": [4200, 4550, 4900]

}


# =========================================================
# DISEASE DATA
# =========================================================

DISEASES = {

    "Rice": (
        "Rice Leaf Blast",
        91,
        "Brown or grey lesions may appear on leaves.",
        "Maintain field hygiene, improve airflow and confirm treatment with a local agriculture expert."
    ),

    "Cotton": (
        "Cotton Leaf Spot",
        88,
        "Spots and yellowing may appear on leaves.",
        "Remove badly affected foliage and follow locally approved crop protection guidance."
    ),

    "Tomato": (
        "Tomato Early Blight",
        93,
        "Dark circular spots with yellowing.",
        "Improve airflow, avoid unnecessary leaf wetting and confirm diagnosis."
    ),

    "Chilli": (
        "Chilli Leaf Curl Risk",
        86,
        "Curling or distortion of young leaves.",
        "Monitor affected plants and consult an agriculture officer."
    ),

    "Maize": (
        "Maize Leaf Spot",
        89,
        "Brown elongated lesions may occur.",
        "Scout regularly and use locally approved management practices."
    )

}


# =========================================================
# OTHER DATA
# =========================================================

PESTS = [

    "Aphids",
    "Stem Borer",
    "Whitefly",
    "Fruit Borer",
    "Thrips",
    "Leaf Miner"

]


PRODUCTS = [

    ("🌱 Organic Compost", "Soil", "₹450 / 25 kg"),

    ("💧 Drip Kit", "Irrigation", "₹2,800"),

    ("🌾 Seed Pack", "Seeds", "₹320"),

    ("🧪 Soil Test Kit", "Soil", "₹650"),

    ("🧤 Farm Gloves", "Tools", "₹180"),

    ("🌿 Bio Fertilizer", "Fertilizer", "₹520")

]


DEALERS = [

    ("Sri Sai Agri Centre", "Seeds & fertilizers", 17.385, 78.486, "2.1 km"),

    ("Rythu Mitra Store", "Irrigation & tools", 17.402, 78.475, "3.4 km"),

    ("Green Crop Solutions", "Plant protection", 17.365, 78.505, "4.8 km")

]


SCHEMES = [

    (
        "PM-KISAN",
        "Income support for eligible farmer families."
    ),

    (
        "PMFBY",
        "Crop insurance support against eligible risks."
    ),

    (
        "Soil Health Card",
        "Soil testing and nutrient guidance."
    )

]


# =========================================================
# LOCAL STORAGE
# =========================================================

def load_json(filename, default):

    file = DATA / filename

    if file.exists():

        try:

            return json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return default

    return default


def save_json(filename, data):

    file = DATA / filename

    file.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "profile_complete" not in st.session_state:

    st.session_state.profile_complete = False


if "language" not in st.session_state:

    st.session_state.language = "English"


if "service" not in st.session_state:

    st.session_state.service = "Home"


if "profile" not in st.session_state:

    st.session_state.profile = {}


if "listings" not in st.session_state:

    st.session_state.listings = load_json(
        "marketplace.json",
        [
            {
                "id": 1,
                "crop": "Rice",
                "variety": "BPT 5204",
                "grade": "A",
                "quantity": 25,
                "price": 2850,
                "village": "Warangal",
                "seller": "Ramesh Farmer",
                "verified": True,
                "status": "Available"
            },
            {
                "id": 2,
                "crop": "Chilli",
                "variety": "Teja",
                "grade": "A",
                "quantity": 8,
                "price": 14800,
                "village": "Khammam",
                "seller": "Lakshmi Farmer",
                "verified": True,
                "status": "Available"
            }
        ]
    )


if "expenses" not in st.session_state:

    st.session_state.expenses = load_json(
        "expenses.json",
        []
    )


if "cart" not in st.session_state:

    st.session_state.cart = []


if "forum" not in st.session_state:

    st.session_state.forum = [

        {
            "farmer": "Ravi",
            "question": "Leaves are turning yellow. What should I check first?",
            "likes": 12,
            "expert": True
        },

        {
            "farmer": "Anitha",
            "question": "What is the best time to sell cotton?",
            "likes": 8,
            "expert": False
        }

    ]


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    # Empty space above the centered login card

    st.markdown(
        """
        <div style="height:3vh;"></div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1.25, 2.0, 1.25]
    )

    with center:

        # REAL STREAMLIT CONTAINER
        # This prevents HTML from appearing as code.

        with st.container(border=True):

            st.markdown(
                '<div class="login-icons">🌱 👨‍🌾 🌾</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-title">Kisan Dost</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-subtitle">'
                'Smart Farming • Better Tomorrow'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<h3 style="text-align:center;color:#075c3b;">'
                '👨‍🌾 Farmer Login'
                '</h3>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-subtitle">'
                'Simple • Local Language • Voice Friendly'
                '</div>',
                unsafe_allow_html=True
            )


            # LANGUAGE

            language = st.selectbox(
                "🌐 Choose your language",
                LANGUAGES,
                index=LANGUAGES.index(
                    st.session_state.language
                )
            )

            st.session_state.language = language


            # LOGIN METHOD

            login_method = st.radio(
                "🔐 Login method",
                [
                    "📱 Mobile OTP",
                    "🪪 Registration ID"
                ],
                horizontal=True
            )


            # MOBILE OTP

            if login_method == "📱 Mobile OTP":

                mobile = st.text_input(
                    "📱 Mobile Number",
                    placeholder="Enter 10-digit mobile number"
                )

                farmer_name = st.text_input(
                    "👤 Farmer Name",
                    placeholder="e.g. Ramesh Kumar"
                )

                otp = st.text_input(
                    "🔒 Enter OTP",
                    placeholder="123456",
                    type="password"
                )

                st.info(
                    "Demo OTP: 123456"
                )


                if st.button(
                    "🚜 Login with OTP",
                    use_container_width=True,
                    type="primary"
                ):

                    if (
                        len(mobile) == 10
                        and mobile.isdigit()
                        and otp == "123456"
                    ):

                        st.session_state.logged_in = True

                        st.session_state.profile = {

                            "name":
                                farmer_name
                                or "Farmer",

                            "mobile":
                                mobile

                        }

                        st.session_state.profile_complete = False

                        st.session_state.service = "Farm Setup"

                        st.rerun()

                    else:

                        st.error(
                            "Enter a valid 10-digit mobile number "
                            "and OTP 123456."
                        )


            # REGISTRATION ID

            else:

                registration_id = st.text_input(
                    "🪪 Registration ID",
                    placeholder="Example: KD1001"
                )

                pin = st.text_input(
                    "🔒 PIN",
                    type="password"
                )


                if st.button(
                    "🚜 Login with Registration ID",
                    use_container_width=True,
                    type="primary"
                ):

                    if registration_id and pin:

                        st.session_state.logged_in = True

                        st.session_state.profile = {

                            "name":
                                "Registered Farmer",

                            "registration_id":
                                registration_id

                        }

                        st.session_state.profile_complete = False

                        st.session_state.service = "Farm Setup"

                        st.rerun()

                    else:

                        st.error(
                            "Enter Registration ID and PIN."
                        )


            st.markdown(
                '<div class="login-badge">'
                '🎙️ Voice + Text • 12 Languages • Farmer Friendly'
                '</div>',
                unsafe_allow_html=True
            )


            # VOICE

            if hasattr(st, "audio_input"):

                voice = st.audio_input(
                    "🎙️ Optional: Record your details"
                )

                if voice:

                    st.success(
                        "Voice recording captured."
                    )


            st.caption(
                "Demo application. Do not enter Aadhaar, "
                "bank passwords or other sensitive information."
            )

            st.markdown(
                '<div style="text-align:center;'
                'color:#6d7c74;font-size:11px;">'
                '🌱 Better Information • Smarter Decisions • Bigger Harvests'
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# TOP HEADER
# =========================================================

def top_header():

    st.markdown(
        """
        <div class="top-header">
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(
        [1.3, 5.5, 1.2]
    )


    with c1:

        st.markdown(
            '<div class="logo">🌱 Kisan Dost</div>'
            '<div class="tagline">'
            'Smart Farming • Better Tomorrow'
            '</div>',
            unsafe_allow_html=True
        )


    with c2:

        current = st.radio(
            "Services",
            SERVICES,
            index=SERVICES.index(
                st.session_state.service
            ),
            format_func=translate,
            horizontal=True,
            label_visibility="collapsed"
        )

        st.session_state.service = current


    with c3:

        language = st.selectbox(
            "Language",
            LANGUAGES,
            index=LANGUAGES.index(
                st.session_state.language
            ),
            key="top_language"
        )

        st.session_state.language = language


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# FARM SETUP
# =========================================================

def farm_setup():

    st.markdown(
        """
        <div class="hero">

        <h1>🌾 Farmer & Farm Setup</h1>

        <p>
        Tell Kisan Dost about your farm.
        You can use text or voice.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if hasattr(st, "audio_input"):

        voice = st.audio_input(
            "🎙️ Record your farm details"
        )

        if voice:

            st.success(
                "Voice recording captured."
            )


    with st.form("farm_profile_form"):

        profile = st.session_state.profile

        c1, c2, c3 = st.columns(3)


        with c1:

            name = st.text_input(
                "Farmer Name",
                profile.get(
                    "name",
                    ""
                )
            )

            mobile = st.text_input(
                "Mobile Number",
                profile.get(
                    "mobile",
                    ""
                )
            )

            state = st.selectbox(
                "State",
                [
                    "Telangana",
                    "Andhra Pradesh",
                    "Karnataka",
                    "Maharashtra",
                    "Tamil Nadu"
                ]
            )

            district = st.text_input(
                "District"
            )


        with c2:

            mandal = st.text_input(
                "Mandal"
            )

            village = st.text_input(
                "Village"
            )

            acres = st.number_input(
                "Farm Area (acres)",
                0.1,
                10000.0,
                2.0
            )

            soil = st.selectbox(
                "Soil Type",
                [
                    "Red Soil",
                    "Black Soil",
                    "Alluvial",
                    "Sandy",
                    "Loamy"
                ]
            )


        with c3:

            water = st.selectbox(
                "Water Source",
                [
                    "Borewell",
                    "Canal",
                    "Rainfed",
                    "Farm Pond",
                    "Drip"
                ]
            )

            crop = st.selectbox(
                "Main Crop",
                CROPS
            )

            latitude = st.number_input(
                "Latitude",
                15.0,
                20.0,
                17.385
            )

            longitude = st.number_input(
                "Longitude",
                74.0,
                82.0,
                78.486
            )


        voice_text = st.text_area(
            "📝 Voice Transcript / Additional Details"
        )


        submitted = st.form_submit_button(
            "💾 Save Farm Profile & Continue",
            use_container_width=True,
            type="primary"
        )


        if submitted:

            st.session_state.profile = {

                "name": name or "Farmer",

                "mobile": mobile,

                "state": state,

                "district": district,

                "mandal": mandal,

                "village": village,

                "acres": acres,

                "soil": soil,

                "water": water,

                "crop": crop,

                "latitude": latitude,

                "longitude": longitude,

                "voice_text": voice_text

            }


            save_json(
                "profile.json",
                st.session_state.profile
            )


            st.session_state.profile_complete = True

            st.session_state.service = "Home"

            st.success(
                "Farm profile saved successfully."
            )

            st.rerun()


# =========================================================
# HOME
# =========================================================

def home():

    profile = st.session_state.profile

    farmer = profile.get(
        "name",
        "Farmer"
    )

    crop = profile.get(
        "crop",
        "Rice"
    )


    st.markdown(
        f"""
        <div class="hero">

        <h1>
        Namaste, {farmer} 👋
        </h1>

        <p>
        Your Kisan Dost farming dashboard for
        <b>{crop}</b>.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    values = [

        ("🌡️", "Temperature", "29°C"),

        ("💧", "Humidity", "68%"),

        ("🛡️", "Crop Risk", "Low"),

        ("📈", "Mandi Price",
         f"₹{MARKET_PRICES[crop][1]}")

    ]


    cols = st.columns(4)


    for col, item in zip(
        cols,
        values
    ):

        icon, title, value = item

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                <div style="font-size:30px;">
                {icon}
                </div>

                <b>{title}</b>

                <h2>
                {value}
                </h2>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        '<div class="section-title">'
        '🚨 Today\'s Farm Alerts'
        '</div>',
        unsafe_allow_html=True
    )


    a, b, c = st.columns(3)


    with a:

        st.markdown(
            """
            <div class="alert-warning">

            <b>🌧️ Rain Alert</b>

            <br>

            Check rainfall before irrigation.

            </div>
            """,
            unsafe_allow_html=True
        )


    with b:

        st.markdown(
            """
            <div class="alert-good">

            <b>🌱 Crop Tip</b>

            <br>

            Inspect leaves regularly for early symptoms.

            </div>
            """,
            unsafe_allow_html=True
        )


    with c:

        st.markdown(
            """
            <div class="alert-danger">

            <b>📈 Price Watch</b>

            <br>

            Compare nearby mandis before selling.

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">'
        '✨ Quick Services'
        '</div>',
        unsafe_allow_html=True
    )


    quick = [

        ("🌦️", "Weather"),

        ("📈", "Mandi Prices"),

        ("🌱", "Crop Advice"),

        ("🩺", "Plant Doctor"),

        ("💧", "Irrigation"),

        ("💰", "Cost & Profit"),

        ("🛒", "Buy & Sell"),

        ("🧪", "Soil Health")

    ]


    cols = st.columns(4)


    for i, (icon, name) in enumerate(quick):

        with cols[i % 4]:

            if st.button(
                f"{icon} {translate(name)}",
                key=f"quick_{i}",
                use_container_width=True
            ):

                st.session_state.service = name

                st.rerun()


# =========================================================
# WEATHER
# =========================================================

def weather():

    st.markdown(
        '<div class="section-title">'
        '🌦️ Weather & Crop Risk'
        '</div>',
        unsafe_allow_html=True
    )


    times = [
        "Now",
        "10 AM",
        "12 PM",
        "2 PM",
        "4 PM",
        "6 PM"
    ]


    temperatures = [
        29,
        31,
        33,
        34,
        32,
        29
    ]


    df = pd.DataFrame(
        {
            "Time": times,
            "Temperature": temperatures
        }
    )


    st.plotly_chart(
        px.line(
            df,
            x="Time",
            y="Temperature",
            markers=True,
            title="Today's Temperature"
        ),
        use_container_width=True
    )


    cols = st.columns(4)


    metrics = [

        ("Humidity", "68%"),

        ("Rain Chance", "35%"),

        ("Wind", "14 km/h"),

        ("UV", "6")

    ]


    for col, (name, value) in zip(
        cols,
        metrics
    ):

        col.metric(
            name,
            value
        )


    st.markdown(
        """
        <div class="alert-warning">

        🌧️ <b>Crop Warning:</b>

        If rain arrives, postpone unnecessary irrigation
        and monitor fungal symptoms.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MANDI
# =========================================================

def mandi():

    st.markdown(
        '<div class="section-title">'
        '📈 Mandi Prices'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    with c1:

        crop = st.selectbox(
            "Crop",
            CROPS
        )


    with c2:

        market = st.selectbox(
            "Market",
            MARKETS
        )


    minimum, average, maximum = MARKET_PRICES[crop]


    a, b, c = st.columns(3)


    a.metric(
        "Minimum",
        f"₹{minimum}/q"
    )


    b.metric(
        "Average",
        f"₹{average}/q",
        "+2.4%"
    )


    c.metric(
        "Maximum",
        f"₹{maximum}/q"
    )


    prices = [

        average - 100,
        average - 60,
        average - 20,
        average,
        average + 30,
        average + 70

    ]


    chart = pd.DataFrame(
        {
            "Day": [
                "-5",
                "-4",
                "-3",
                "-2",
                "-1",
                "Today"
            ],
            "Price": prices
        }
    )


    st.plotly_chart(
        px.line(
            chart,
            x="Day",
            y="Price",
            markers=True,
            title=f"{crop} Price Trend - {market}"
        ),
        use_container_width=True
    )


    st.success(
        "💡 Compare 2–3 nearby markets before selling."
    )


# =========================================================
# CROP ADVICE
# =========================================================

def crop_advice():

    st.markdown(
        '<div class="section-title">'
        '🌱 AI Crop Advice'
        '</div>',
        unsafe_allow_html=True
    )


    current = st.session_state.profile.get(
        "crop",
        "Rice"
    )


    crop = st.selectbox(
        "Choose Crop",
        CROPS,
        index=CROPS.index(current)
    )


    scores = {

        "Rice": 88,
        "Cotton": 82,
        "Maize": 91,
        "Chilli": 86,
        "Tomato": 79,
        "Groundnut": 84,
        "Turmeric": 81,
        "Paddy": 89,
        "Wheat": 72,
        "Soybean": 80

    }


    score = scores[crop]


    st.markdown(
        f"""
        <div class="hero">

        <h1>
        🌱 {crop}
        </h1>

        <h2>
        AI Match Score: {score}%
        </h2>

        <p>
        Based on soil, water, season,
        market trend and risk.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    cols = st.columns(4)


    data = [

        ("Expected Profit", "₹38,000/acre"),

        ("Water Need", "Medium"),

        ("Risk", "Low"),

        ("Market", "Positive")

    ]


    for col, (name, value) in zip(
        cols,
        data
    ):

        col.metric(
            name,
            value
        )


    st.subheader(
        "🔎 Why this crop?"
    )


    factor_df = pd.DataFrame(
        {
            "Factor": [
                "Soil",
                "Water",
                "Season",
                "Market",
                "Risk"
            ],
            "Score": [
                90,
                82,
                86,
                84,
                80
            ]
        }
    )


    st.plotly_chart(
        px.bar(
            factor_df,
            x="Factor",
            y="Score",
            range_y=[0, 100]
        ),
        use_container_width=True
    )


    st.info(
        "This is a demo explainable-AI score. "
        "Replace the rule-based function with your trained model."
    )


# =========================================================
# SOIL HEALTH
# =========================================================

def soil_health():

    st.markdown(
        '<div class="section-title">'
        '🧪 Soil Health'
        '</div>',
        unsafe_allow_html=True
    )


    values = [

        ("pH", "6.8", "Good"),

        ("Nitrogen", "Medium", "Monitor"),

        ("Phosphorus", "Good", "Good"),

        ("Potassium", "Medium", "Monitor"),

        ("Organic Carbon", "0.72%", "Good")

    ]


    cols = st.columns(5)


    for col, (name, value, delta) in zip(
        cols,
        values
    ):

        col.metric(
            name,
            value,
            delta
        )


    st.info(
        "Use a soil test report before making "
        "fertilizer decisions."
    )


    st.subheader(
        "Past Soil Reports"
    )


    report = pd.DataFrame(
        {
            "Date": [
                "2026-08-12",
                "2026-04-08"
            ],
            "pH": [
                6.8,
                6.6
            ],
            "Organic Carbon": [
                "0.72%",
                "0.68%"
            ],
            "Status": [
                "Good",
                "Good"
            ]
        }
    )


    st.dataframe(
        report,
        use_container_width=True
    )


# =========================================================
# PLANT DOCTOR
# =========================================================

def plant_doctor():

    st.markdown(
        '<div class="section-title">'
        '🩺 Plant Doctor'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    with c1:

        camera = st.camera_input(
            "📷 Take Leaf Photo"
        )


    with c2:

        upload = st.file_uploader(
            "🖼️ Upload Leaf Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )


    image = camera or upload


    if image:

        st.image(
            image,
            width=420
        )


        crop = st.selectbox(
            "Crop",
            CROPS
        )


        if st.button(
            "🔍 Analyze Leaf",
            type="primary"
        ):

            result = DISEASES.get(
                crop,
                (
                    "Healthy / Unknown",
                    84,
                    "No clear symptom.",
                    "Monitor and confirm with an expert."
                )
            )


            disease, confidence, symptoms, advice = result


            st.success(
                f"Prediction: {disease} "
                f"— {confidence}% confidence"
            )


            st.write(
                "**Symptoms:**",
                symptoms
            )


            st.write(
                "**Control guidance:**",
                advice
            )


            st.warning(
                "Demo classifier only. "
                "Confirm diagnosis locally before applying treatment."
            )


# =========================================================
# CROP PROTECTION
# =========================================================

def crop_protection():

    st.markdown(
        '<div class="section-title">'
        '🛡️ Crop Protection'
        '</div>',
        unsafe_allow_html=True
    )


    crop = st.selectbox(
        "Crop",
        CROPS
    )


    stage = st.selectbox(
        "Growth Stage",
        [
            "Seedling",
            "Vegetative",
            "Flowering",
            "Fruiting",
            "Harvest"
        ]
    )


    st.write(
        f"Current stage: **{stage}**"
    )


    selected = random.sample(
        PESTS,
        3
    )


    for pest in selected:

        st.markdown(
            f"""
            <div class="market-card">

            <h3>🐛 {pest}</h3>

            <p>
            Check leaves, new shoots and damaged fruits/stems.
            </p>

            <b>Management:</b>

            Scout regularly, maintain field hygiene
            and use only locally approved products
            according to their labels.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# IRRIGATION
# =========================================================

def irrigation():

    st.markdown(
        '<div class="section-title">'
        '💧 Smart Irrigation'
        '</div>',
        unsafe_allow_html=True
    )


    rainfall = st.slider(
        "Expected rainfall in next 3 days (mm)",
        0,
        100,
        25
    )


    water_source = st.session_state.profile.get(
        "water",
        "Borewell"
    )


    irrigation_need = max(
        0,
        18 - rainfall * 0.35
    )


    st.metric(
        "Recommended Irrigation Need",
        f"{irrigation_need:.1f} mm"
    )


    st.write(
        f"Water Source: **{water_source}**"
    )


    if rainfall > 35:

        st.success(
            "🌧️ Rain may reduce irrigation need."
        )

    else:

        st.info(
            "💧 Check soil moisture before irrigation."
        )


# =========================================================
# COST & PROFIT
# =========================================================

def cost_profit():

    st.markdown(
        '<div class="section-title">'
        '💰 Cost & Profit Calculator'
        '</div>',
        unsafe_allow_html=True
    )


    c = st.columns(4)


    seed = c[0].number_input(
        "Seed Cost",
        0,
        100000,
        3500
    )


    fertilizer = c[1].number_input(
        "Fertilizer Cost",
        0,
        100000,
        7000
    )


    labour = c[2].number_input(
        "Labour Cost",
        0,
        200000,
        12000
    )


    other = c[3].number_input(
        "Other Cost",
        0,
        200000,
        6000
    )


    yield_q = st.slider(
        "Expected Yield (quintal/acre)",
        1,
        100,
        25
    )


    price = st.slider(
        "Selling Price (₹/quintal)",
        500,
        20000,
        2800,
        100
    )


    total_cost = (
        seed
        + fertilizer
        + labour
        + other
    )


    revenue = yield_q * price

    profit = revenue - total_cost


    a, b, c = st.columns(3)


    a.metric(
        "Total Cost",
        f"₹{total_cost:,}"
    )


    b.metric(
        "Revenue",
        f"₹{revenue:,}"
    )


    c.metric(
        "Estimated Profit",
        f"₹{profit:,}"
    )


    st.progress(
        min(
            1,
            max(
                0,
                profit / max(revenue, 1)
            )
        )
    )


    st.caption(
        "Break-even price = Total Cost / Expected Yield."
    )


# =========================================================
# CROP DIARY
# =========================================================

def crop_diary():

    st.markdown(
        '<div class="section-title">'
        '📔 Crop Diary'
        '</div>',
        unsafe_allow_html=True
    )


    expenses = st.session_state.expenses


    total = sum(
        item["amount"]
        for item in expenses
    )


    st.metric(
        "Recorded Expenses",
        f"₹{total:,.0f}"
    )


    with st.form("expense_form"):

        expense_date = st.date_input(
            "Date",
            date.today()
        )


        category = st.selectbox(
            "Category",
            [
                "Seed",
                "Fertilizer",
                "Labour",
                "Water",
                "Transport",
                "Other"
            ]
        )


        amount = st.number_input(
            "Amount",
            0.0,
            1000000.0,
            500.0
        )


        note = st.text_input(
            "Note"
        )


        submitted = st.form_submit_button(
            "➕ Add Expense"
        )


        if submitted:

            expenses.append(
                {
                    "date":
                        str(expense_date),

                    "category":
                        category,

                    "amount":
                        amount,

                    "note":
                        note
                }
            )


            st.session_state.expenses = expenses


            save_json(
                "expenses.json",
                expenses
            )


            st.success(
                "Expense added."
            )

            st.rerun()


    if expenses:

        st.dataframe(
            pd.DataFrame(expenses),
            use_container_width=True
        )


# =========================================================
# CROP ROTATION
# =========================================================

def crop_rotation():

    st.markdown(
        '<div class="section-title">'
        '🔄 Crop Rotation'
        '</div>',
        unsafe_allow_html=True
    )


    current = st.selectbox(
        "Current Crop",
        CROPS
    )


    suggestions = {

        "Rice": [
            "Groundnut",
            "Soybean",
            "Maize"
        ],

        "Cotton": [
            "Groundnut",
            "Maize"
        ],

        "Maize": [
            "Groundnut",
            "Soybean"
        ],

        "Chilli": [
            "Groundnut",
            "Maize"
        ],

        "Tomato": [
            "Groundnut",
            "Soybean"
        ]

    }


    for crop in suggestions.get(
        current,
        [
            "Groundnut",
            "Maize",
            "Soybean"
        ]
    ):

        st.markdown(
            f"""
            <div class="alert-good">

            🌱 <b>Next Crop: {crop}</b>

            <br>

            Helps diversify crop planning
            and farming decisions.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# WHAT IF
# =========================================================

def what_if():

    st.markdown(
        '<div class="section-title">'
        '🎛️ What-If Simulator'
        '</div>',
        unsafe_allow_html=True
    )


    rainfall = st.slider(
        "Rainfall Change %",
        -50,
        50,
        0
    )


    temperature = st.slider(
        "Temperature Change °C",
        -5,
        5,
        0
    )


    price_change = st.slider(
        "Market Price Change %",
        -40,
        40,
        0
    )


    input_change = st.slider(
        "Input Cost Change %",
        -30,
        50,
        0
    )


    base_profit = 38000


    estimated_profit = base_profit * (
        1
        + price_change / 100
        - rainfall * 0.002
        - temperature * 0.01
        - input_change / 100
    )


    risk = min(
        95,
        max(
            5,
            30
            - rainfall * 0.2
            + abs(temperature) * 7
            - input_change * 0.15
        )
    )


    a, b = st.columns(2)


    a.metric(
        "Estimated Profit",
        f"₹{estimated_profit:,.0f}"
    )


    b.metric(
        "Risk Score",
        f"{risk:.0f}%"
    )


    st.info(
        "This is a planning simulator, not a guaranteed forecast."
    )


# =========================================================
# BUY & SELL MARKETPLACE
# =========================================================

def marketplace():

    st.markdown(
        '<div class="section-title">'
        '🛒 Farmer Marketplace — Buy & Sell'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="alert-warning">

        ⚠️ Verify farmer/buyer identity,
        crop quality and quantity before transaction.

        No online payment is included in this demo.

        </div>
        """,
        unsafe_allow_html=True
    )


    mode = st.radio(
        "Marketplace",
        [
            "🛍️ Buy",
            "📦 Sell",
            "📋 My List",
            "📈 Prices",
            "👥 Directory"
        ],
        horizontal=True
    )


    # BUY

    if mode == "🛍️ Buy":

        crop_filter = st.selectbox(
            "Filter Crop",
            ["All"] + CROPS
        )


        for item in st.session_state.listings:

            if item["status"] != "Available":
                continue


            if (
                crop_filter != "All"
                and item["crop"] != crop_filter
            ):
                continue


            verified = (
                "✅ Verified"
                if item["verified"]
                else ""
            )


            st.markdown(
                f"""
                <div class="market-card">

                <h3>
                🌾 {item["crop"]}
                -
                {item["variety"]}
                </h3>

                <p>
                Grade:
                <b>{item["grade"]}</b>
                </p>

                <p>
                Quantity:
                <b>{item["quantity"]} Quintal</b>
                </p>

                <p>
                Price:
                <b>₹{item["price"]}/quintal</b>
                </p>

                <p>
                📍 {item["village"]}
                </p>

                <p>
                👨‍🌾 {item["seller"]}
                {verified}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


    # SELL

    elif mode == "📦 Sell":

        with st.form("marketplace_listing"):

            c1, c2, c3 = st.columns(3)


            with c1:

                crop = st.selectbox(
                    "Crop",
                    CROPS
                )


            with c2:

                variety = st.text_input(
                    "Variety",
                    "Local"
                )


            with c3:

                grade = st.selectbox(
                    "Grade",
                    [
                        "A",
                        "B",
                        "C"
                    ]
                )


            quantity = st.number_input(
                "Quantity (Quintal)",
                1.0,
                10000.0,
                10.0
            )


            price = st.number_input(
                "Price per Quintal",
                100.0,
                100000.0,
                2800.0
            )


            village = st.text_input(
                "Village",
                st.session_state.profile.get(
                    "village",
                    ""
                )
            )


            photo = st.file_uploader(
                "Crop Photo",
                type=[
                    "jpg",
                    "jpeg",
                    "png"
                ]
            )


            publish = st.form_submit_button(
                "📢 Publish Listing",
                type="primary"
            )


            if publish:

                new_id = max(
                    [
                        item["id"]
                        for item in st.session_state.listings
                    ]
                    or [0]
                ) + 1


                new_item = {

                    "id": new_id,

                    "crop": crop,

                    "variety": variety,

                    "grade": grade,

                    "quantity": quantity,

                    "price": price,

                    "village":
                        village or "Local",

                    "seller":
                        st.session_state.profile.get(
                            "name",
                            "Farmer"
                        ),

                    "verified": False,

                    "status": "Available"

                }


                st.session_state.listings.append(
                    new_item
                )


                save_json(
                    "marketplace.json",
                    st.session_state.listings
                )


                st.success(
                    "Your crop listing has been published."
                )


    # MY LIST

    elif mode == "📋 My List":

        farmer = st.session_state.profile.get(
            "name",
            "Farmer"
        )


        mine = [

            item

            for item in st.session_state.listings

            if item["seller"] == farmer

        ]


        if mine:

            st.dataframe(
                pd.DataFrame(mine),
                use_container_width=True
            )

        else:

            st.info(
                "You do not have any listings yet."
            )


    # PRICES

    elif mode == "📈 Prices":

        table = pd.DataFrame(

            [

                {
                    "Crop": crop,
                    "Minimum": values[0],
                    "Average": values[1],
                    "Maximum": values[2]
                }

                for crop, values
                in MARKET_PRICES.items()

            ]

        )


        st.dataframe(
            table,
            use_container_width=True
        )


    # DIRECTORY

    else:

        directory = pd.DataFrame(

            {
                "Type": [
                    "FPO",
                    "Buyer",
                    "Trader"
                ],

                "Name": [
                    "Warangal FPO",
                    "Local Rice Buyer",
                    "Agri Trade Hub"
                ],

                "Location": [
                    "Warangal",
                    "Karimnagar",
                    "Hyderabad"
                ],

                "Contact": [
                    "Contact locally",
                    "Contact locally",
                    "Contact locally"
                ]
            }

        )


        st.dataframe(
            directory,
            use_container_width=True
        )


# =========================================================
# AGRI STORE
# =========================================================

def agri_store():

    st.markdown(
        '<div class="section-title">'
        '🏪 Agri Store'
        '</div>',
        unsafe_allow_html=True
    )


    category = st.selectbox(
        "Category",
        [
            "All",
            "Soil",
            "Irrigation",
            "Seeds",
            "Tools",
            "Fertilizer"
        ]
    )


    for index, (
        name,
        item_category,
        price
    ) in enumerate(PRODUCTS):


        if (
            category != "All"
            and item_category != category
        ):
            continue


        c1, c2 = st.columns(
            [5, 1]
        )


        with c1:

            st.markdown(
                f"""
                <div class="market-card">

                <b>{name}</b>

                <br>

                {item_category}

                • {price}

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            if st.button(
                "Add",
                key=f"cart_{index}",
                use_container_width=True
            ):

                st.session_state.cart.append(
                    name
                )

                st.success(
                    "Added to cart."
                )


# =========================================================
# DEALERS
# =========================================================

def dealers():

    st.markdown(
        '<div class="section-title">'
        '📍 Dealers Near Me'
        '</div>',
        unsafe_allow_html=True
    )


    dealer_df = pd.DataFrame(
        DEALERS,
        columns=[
            "Name",
            "Services",
            "lat",
            "lon",
            "Distance"
        ]
    )


    st.map(
        dealer_df[
            [
                "lat",
                "lon"
            ]
        ]
    )


    for (
        name,
        services,
        lat,
        lon,
        distance
    ) in DEALERS:

        st.markdown(
            f"""
            <div class="market-card">

            <b>🏪 {name}</b>

            • {distance}

            <br>

            {services}

            <br>

            📞 Contact dealer locally.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# KISAN FORUM
# =========================================================

def forum():

    st.markdown(
        '<div class="section-title">'
        '👥 Kisan Forum'
        '</div>',
        unsafe_allow_html=True
    )


    with st.form("forum_question"):

        question = st.text_area(
            "Ask your farming question"
        )


        post = st.form_submit_button(
            "Post Question"
        )


        if post and question:

            st.session_state.forum.insert(
                0,
                {
                    "farmer":
                        st.session_state.profile.get(
                            "name",
                            "Farmer"
                        ),

                    "question":
                        question,

                    "likes": 0,

                    "expert": False
                }
            )


            st.rerun()


    for item in st.session_state.forum:

        badge = (
            " 🧑‍🌾 Expert"
            if item["expert"]
            else ""
        )


        st.markdown(
            f"""
            <div class="market-card">

            <b>
            {item["farmer"]}
            {badge}
            </b>

            <p>
            {item["question"]}
            </p>

            ❤️ {item["likes"]} likes

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# SCHEMES & NEWS
# =========================================================

def schemes_news():

    st.markdown(
        '<div class="section-title">'
        '📢 Schemes & News'
        '</div>',
        unsafe_allow_html=True
    )


    for name, description in SCHEMES:

        st.markdown(
            f"""
            <div class="market-card">

            <h3>
            📢 {name}
            </h3>

            <p>
            {description}
            </p>

            <b>
            Check current official eligibility
            before applying.
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PAGE ROUTER
# =========================================================

def show_page():

    page = st.session_state.service


    if page == "Home":

        home()


    elif page == "Farm Setup":

        farm_setup()


    elif page == "Weather":

        weather()


    elif page == "Mandi Prices":

        mandi()


    elif page == "Crop Advice":

        crop_advice()


    elif page == "Soil Health":

        soil_health()


    elif page == "Plant Doctor":

        plant_doctor()


    elif page == "Crop Protection":

        crop_protection()


    elif page == "Irrigation":

        irrigation()


    elif page == "Cost & Profit":

        cost_profit()


    elif page == "Crop Diary":

        crop_diary()


    elif page == "Crop Rotation":

        crop_rotation()


    elif page == "What-If":

        what_if()


    elif page == "Buy & Sell":

        marketplace()


    elif page == "Agri Store":

        agri_store()


    elif page == "Dealers":

        dealers()


    elif page == "Kisan Forum":

        forum()


    elif page == "Schemes & News":

        schemes_news()


# =========================================================
# MAIN
# =========================================================

if not st.session_state.logged_in:

    login_page()

else:

    top_header()


    if (
        not st.session_state.profile_complete
        and st.session_state.service != "Farm Setup"
    ):

        st.warning(
            "Please complete Farm Setup before using the services."
        )

        st.session_state.service = "Farm Setup"


    show_page()


    st.markdown(
        """
        <div class="app-footer">

        🌱 Kisan Dost • Smart Farming • Better Tomorrow

        <br>

        Demo/MVP version — connect real APIs and ML models
        for production deployment.

        </div>
        """,
        unsafe_allow_html=True
    )