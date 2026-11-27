import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CKD AI Prediction",
    page_icon="🩺",
    layout="wide"
)

if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

if "risk_level" not in st.session_state:
    st.session_state.risk_level = ""

if "patient_data" not in st.session_state:
    st.session_state.patient_data = {}


st.sidebar.title("🩺 CKD AI System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Patient Assessment",
        "Risk Prediction",
        "Analysis Dashboard",
        "About Project"
    ]
)


if page == "Home":

    st.title("🩺 AI Driven Chronic Kidney Disease Risk Prediction and Analysis")

    st.subheader("Early Risk Assessment Using Artificial Intelligence")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Problem Statement")
        st.write(
            "Chronic Kidney Disease can develop gradually and may remain "
            "undetected during its early stages. Analyzing multiple health "
            "parameters manually can also be time-consuming."
        )

    with col2:
        st.subheader("Proposed Solution")
        st.write(
            "This project provides an AI-based system that analyzes patient "
            "health parameters and estimates the risk level of Chronic Kidney Disease."
        )

    st.markdown("---")

    st.subheader("Project Workflow")

    st.success(
        "Patient Data → Data Preprocessing → Feature Selection → "
        "ML Model → Risk Prediction → Analysis"
    )

    st.markdown("---")

    st.subheader("Main Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("Patient Details\n\nEnter patient information.")

    with c2:
        st.info("Risk Prediction\n\nEstimate the CKD risk level.")

    with c3:
        st.info("Analysis Dashboard\n\nView patient parameter analysis.")


elif page == "Patient Assessment":

    st.title("👤 Patient Assessment")

    st.write("Enter the patient health parameters.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=40
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        bp = st.number_input(
            "Blood Pressure (mmHg)",
            min_value=50,
            max_value=250,
            value=120
        )

        glucose = st.number_input(
            "Blood Glucose (mg/dL)",
            min_value=50,
            max_value=500,
            value=100
        )

        urea = st.number_input(
            "Blood Urea (mg/dL)",
            min_value=1,
            max_value=300,
            value=30
        )

    with col2:

        creatinine = st.number_input(
            "Serum Creatinine (mg/dL)",
            min_value=0.1,
            max_value=20.0,
            value=1.0,
            step=0.1
        )

        hemoglobin = st.number_input(
            "Hemoglobin (g/dL)",
            min_value=3.0,
            max_value=20.0,
            value=13.0,
            step=0.1
        )

        albumin = st.number_input(
            "Albumin",
            min_value=0.0,
            max_value=6.0,
            value=1.0,
            step=0.1
        )

        sodium = st.number_input(
            "Sodium (mEq/L)",
            min_value=100,
            max_value=200,
            value=140
        )

        potassium = st.number_input(
            "Potassium (mEq/L)",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.1
        )

        wbc = st.number_input(
            "WBC Count",
            min_value=1000,
            max_value=30000,
            value=8000
        )

        rbc = st.number_input(
            "RBC Count",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=0.1
        )

    st.markdown("---")
    
    if st.button("🔍 Predict CKD Risk", use_container_width=True):
        
        patient_payload = {
            "name": name,
            "age": int(age),
            "gender": gender,
            "blood_pressure": int(bp),
            "glucose": int(glucose),
            "urea": int(urea),
            "creatinine": float(creatinine),
            "hemoglobin": float(hemoglobin),
            "albumin": float(albumin),
            "sodium": int(sodium),
            "potassium": float(potassium),
            "wbc": int(wbc),
            "rbc": float(rbc)
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/patient",
                json=patient_payload,
                timeout=5
            )
            response.raise_for_status()
            st.success("Patient data saved to backend successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection failed: {e}")
            st.stop()

        score = 0

        if age > 60:
            score += 10

        if bp > 140:
            score += 15

        if glucose > 140:
            score += 10

        if urea > 45:
            score += 15

        if creatinine > 1.3:
            score += 20

        if hemoglobin < 11:
            score += 10

        if albumin >= 2:
            score += 10

        if sodium < 135 or sodium > 145:
            score += 5

        if potassium < 3.5 or potassium > 5.2:
            score += 5

        score = max(5, min(score, 95))

        if score < 30:
            risk = "Low Risk"
        elif score < 60:
            risk = "Moderate Risk"
        else:
            risk = "High Risk"

        st.session_state.risk_score = score
        st.session_state.risk_level = risk

        st.session_state.patient_data = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Blood Pressure": bp,
            "Glucose": glucose,
            "Blood Urea": urea,
            "Creatinine": creatinine,
            "Hemoglobin": hemoglobin,
            "Albumin": albumin,
            "Sodium": sodium,
            "Potassium": potassium,
            "WBC": wbc,
            "RBC": rbc
        }

        st.session_state.prediction_done = True

        st.success("Prediction completed successfully!")


elif page == "Risk Prediction":

    st.title("🧠 CKD Risk Prediction")

    if not st.session_state.prediction_done:

        st.warning("Please complete Patient Assessment first.")

    else:

        data = st.session_state.patient_data
        score = st.session_state.risk_score
        risk = st.session_state.risk_level

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Patient",
                data["Name"] if data["Name"] else "Anonymous"
            )

        with c2:
            st.metric("Age", str(data["Age"]))

        with c3:
            st.metric("Gender", data["Gender"])

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Risk Score", str(score) + "%")

        with c2:
            st.metric("Risk Level", risk)

        st.progress(score / 100)

        if risk == "Low Risk":
            st.success("🟢 Low estimated risk based on the entered parameters.")

        elif risk == "Moderate Risk":
            st.warning("🟡 Moderate estimated risk based on the entered parameters.")

        else:
            st.error("🔴 High estimated risk based on the entered parameters.")

        st.info("This is an academic prototype and not a medical diagnosis.")


elif page == "Analysis Dashboard":

    st.title("📊 Analysis Dashboard")

    if not st.session_state.prediction_done:

        st.warning("Please complete Patient Assessment first.")

    else:

        data = st.session_state.patient_data

        st.subheader("Patient Parameters")

        df = pd.DataFrame({
            "Parameter": [
                "Age",
                "Blood Pressure",
                "Blood Glucose",
                "Blood Urea",
                "Serum Creatinine",
                "Hemoglobin",
                "Albumin",
                "Sodium",
                "Potassium",
                "WBC",
                "RBC"
            ],
            "Value": [
                data["Age"],
                data["Blood Pressure"],
                data["Glucose"],
                data["Blood Urea"],
                data["Creatinine"],
                data["Hemoglobin"],
                data["Albumin"],
                data["Sodium"],
                data["Potassium"],
                data["WBC"],
                data["RBC"]
            ]
        })

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("Parameter Analysis")

        abnormal = []

        if data["Blood Pressure"] > 140:
            abnormal.append("Blood Pressure is above the selected threshold.")

        if data["Glucose"] > 140:
            abnormal.append("Blood Glucose is above the selected threshold.")

        if data["Blood Urea"] > 45:
            abnormal.append("Blood Urea is above the selected threshold.")

        if data["Creatinine"] > 1.3:
            abnormal.append("Serum Creatinine is above the selected threshold.")

        if data["Hemoglobin"] < 11:
            abnormal.append("Hemoglobin is below the selected threshold.")

        if data["Sodium"] < 135 or data["Sodium"] > 145:
            abnormal.append("Sodium is outside the selected range.")

        if data["Potassium"] < 3.5 or data["Potassium"] > 5.2:
            abnormal.append("Potassium is outside the selected range.")

        if len(abnormal) == 0:

            st.success("No parameters crossed the demo thresholds.")

        else:

            for item in abnormal:
                st.warning(item)

        st.markdown("---")

        st.subheader("Analysis Summary")

        st.write(
            "The system analyzed the entered patient parameters and "
            "generated an estimated CKD risk score of "
            + str(st.session_state.risk_score)
            + "% with an estimated risk category of "
            + st.session_state.risk_level
            + "."
        )


elif page == "About Project":

    st.title("ℹ️ About Project")

    st.subheader("Objective")

    st.write(
        "To develop an AI-based system for analyzing patient health "
        "parameters and estimating the risk of Chronic Kidney Disease."
    )

    st.markdown("---")

    st.subheader("Technologies Used")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info("Python")

    with c2:
        st.info("Pandas")

    with c3:
        st.info("Machine Learning")

    with c4:
        st.info("Streamlit")

    st.markdown("---")

    st.subheader("Workflow")

    st.write(
        "1. Patient Data Collection\n"
        "2. Data Preprocessing\n"
        "3. Feature Selection\n"
        "4. Machine Learning Model\n"
        "5. Risk Prediction\n"
        "6. Analysis"
    )

    st.markdown("---")

    st.subheader("Future Scope")

    st.write(
        "• Integration with a real CKD dataset\n"
        "• Machine learning model training\n"
        "• Improved prediction accuracy\n"
        "• Graphical data visualization\n"
        "• Healthcare application integration"
    )

    st.markdown("---")

    st.caption(
        "Academic Prototype - For educational purposes only."
    )
