import streamlit as st
import requests


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# API Configuration
# ============================================================

API_URL = "http://localhost:8000/predict"


# ============================================================
# City Lists
# ============================================================

tier_1_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune"
]

tier_2_cities = [
    "Jaipur",
    "Chandigarh",
    "Indore",
    "Lucknow",
    "Patna",
    "Ranchi",
    "Visakhapatnam",
    "Coimbatore",
    "Bhopal",
    "Nagpur",
    "Vadodara",
    "Surat",
    "Rajkot",
    "Jodhpur",
    "Raipur",
    "Amritsar",
    "Varanasi",
    "Agra",
    "Dehradun",
    "Mysore",
    "Jabalpur",
    "Guwahati",
    "Thiruvananthapuram",
    "Ludhiana",
    "Nashik",
    "Allahabad",
    "Udaipur",
    "Aurangabad",
    "Hubli",
    "Belgaum",
    "Salem",
    "Vijayawada",
    "Tiruchirappalli",
    "Bhavnagar",
    "Gwalior",
    "Dhanbad",
    "Bareilly",
    "Aligarh",
    "Gaya",
    "Kozhikode",
    "Warangal",
    "Kolhapur",
    "Bilaspur",
    "Jalandhar",
    "Noida",
    "Guntur",
    "Asansol",
    "Siliguri"
]


all_cities = sorted(
    tier_1_cities + tier_2_cities
)


# ============================================================
# Header
# ============================================================

st.title("🏥 Insurance Premium Category Predictor")

st.markdown(
    """
    Enter the customer's details below and our machine learning
    model will predict the **insurance premium category**.
    """
)

st.divider()


# ============================================================
# Input Section
# ============================================================

st.subheader("👤 Customer Information")


col1, col2, col3 = st.columns(3)


with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=119,
        value=30,
        step=1
    )


with col2:

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=65.0,
        step=0.5
    )


with col3:

    height = st.number_input(
        "Height (m)",
        min_value=0.5,
        max_value=2.5,
        value=1.70,
        step=0.01
    )


col4, col5, col6 = st.columns(3)


with col4:

    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=0.1,
        max_value=1000.0,
        value=10.0,
        step=0.5
    )


with col5:

    smoker_option = st.selectbox(
        "Smoking Status",
        ["No", "Yes"]
    )

    smoker = smoker_option == "Yes"


with col6:

    occupation = st.selectbox(
        "Occupation",
        [
            "private_job",
            "government_job",
            "business_owner",
            "freelancer",
            "student",
            "retired",
            "unemployed"
        ]
    )


# ============================================================
# City Selection
# ============================================================

st.subheader("📍 Location")

city = st.selectbox(
    "Select City",
    all_cities,
    index=all_cities.index("Mumbai")
)


st.divider()


# ============================================================
# Prediction Button
# ============================================================

predict_button = st.button(
    "🔮 Predict Premium Category",
    use_container_width=True
)


# ============================================================
# Prediction
# ============================================================

if predict_button:

    input_data = {

        "age": age,

        "weight": weight,

        "height": height,

        "income_lpa": income_lpa,

        "smoker": smoker,

        "city": city,

        "occupation": occupation
    }

    try:

        with st.spinner("Analyzing customer information..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=10
            )


        # ====================================================
        # Successful Response
        # ====================================================

        if response.status_code == 200:

            result = response.json()

            prediction = result["predicted_category"]

            features = result["features"]

            st.success("Prediction generated successfully!")


            # =================================================
            # Prediction Display
            # =================================================

            st.subheader("🎯 Prediction Result")

            result_col1, result_col2, result_col3 = st.columns(3)


            with result_col1:

                st.metric(
                    "Premium Category",
                    prediction
                )


            with result_col2:

                st.metric(
                    "BMI",
                    features["bmi"]
                )


            with result_col3:

                st.metric(
                    "City Tier",
                    features["city_tier"]
                )


            # =================================================
            # Model Features
            # =================================================

            st.subheader("📊 Calculated Features")

            feature_col1, feature_col2 = st.columns(2)


            with feature_col1:

                st.info(
                    f"**Age Group:** {features['age_group']}"
                )


            with feature_col2:

                st.info(
                    f"**Lifestyle Risk:** {features['lifestyle_risk']}"
                )


        # ====================================================
        # API Error
        # ====================================================

        else:

            st.error(
                f"API request failed with status code: "
                f"{response.status_code}"
            )

            try:

                st.json(response.json())

            except Exception:

                st.write(response.text)


    # ========================================================
    # Connection Error
    # ========================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI server."
        )

        st.info(
            "Make sure FastAPI is running on "
            "http://localhost:8000"
        )


    # ========================================================
    # Timeout Error
    # ========================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out. "
            "Please check whether the FastAPI server is running."
        )


    # ========================================================
    # Other Errors
    # ========================================================

    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )