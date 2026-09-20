import streamlit as st
import pandas as pd
import joblib

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Student360 AI",
    page_icon="🎓",
    layout="centered"
)

# ==============================
# LOAD MODEL
# ==============================

model = joblib.load("student360_model.pkl")

# ==============================
# TITLE
# ==============================

st.title("🎓 Student360 AI")

st.caption(
    "AI-Powered Student Performance & Academic Risk Analysis"
)

st.subheader("AI-Powered Student Performance Predictor")

st.write(
    "Enter your academic information to get a performance prediction, "
    "risk level, strengths, weaknesses, and recommendations."
)

st.divider()

# ==============================
# STUDENT INFORMATION
# ==============================

st.header("📋 Student Information")

semester = st.number_input(
    "Semester",
    min_value=1,
    max_value=8,
    value=5
)

cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.2,
    step=0.1
)

attendance = st.number_input(
    "Attendance (%)",
    min_value=0.0,
    max_value=100.0,
    value=82.0,
    step=1.0
)

internal = st.number_input(
    "Internal Marks",
    min_value=0.0,
    max_value=100.0,
    value=75.0,
    step=1.0
)

assignment = st.number_input(
    "Assignment Score",
    min_value=0.0,
    max_value=100.0,
    value=80.0,
    step=1.0
)

quiz = st.number_input(
    "Quiz Score",
    min_value=0.0,
    max_value=100.0,
    value=72.0,
    step=1.0
)

study_hours = st.number_input(
    "Study Hours per Day",
    min_value=0.0,
    max_value=24.0,
    value=3.0,
    step=0.5
)

backlogs = st.number_input(
    "Number of Backlogs",
    min_value=0,
    max_value=20,
    value=1
)

skill = st.slider(
    "Technical Skill Level",
    min_value=1,
    max_value=5,
    value=3
)

career_goal = st.selectbox(
    "Career Goal",
    [
        "AI/ML Engineer",
        "Data Scientist",
        "Software Developer",
        "Data Analyst",
        "Cybersecurity",
        "Cloud/DevOps",
        "Higher Studies",
        "Other"
    ]
)

# ==============================
# WHAT-IF SIMULATOR
# ==============================

st.divider()

st.subheader("🔮 What-If Performance Simulator")

st.write(
    "Change your study hours and attendance to see how "
    "the model's predicted performance may change."
)

whatif_study_hours = st.slider(
    "What-If Study Hours/Day",
    min_value=0.0,
    max_value=12.0,
    value=float(study_hours),
    step=0.5
)

whatif_attendance = st.slider(
    "What-If Attendance (%)",
    min_value=0.0,
    max_value=100.0,
    value=float(attendance),
    step=1.0
)

if st.button("🔮 Simulate Performance"):

    whatif_student = pd.DataFrame({
        "Semester": [semester],
        "CGPA": [cgpa],
        "Attendance": [whatif_attendance],
        "Internal_Marks": [internal],
        "Assignment_Score": [assignment],
        "Quiz_Score": [quiz],
        "Study_Hours": [whatif_study_hours],
        "Backlogs": [backlogs],
        "Skill_Level": [skill]
    })

    whatif_score = float(
        model.predict(whatif_student)[0]
    )

    whatif_score = max(
        0,
        min(100, whatif_score)
    )

    st.metric(
        "What-If Predicted Performance",
        f"{whatif_score:.2f} / 100"
    )

    st.caption(
        "This is a model-based sensitivity simulation, "
        "not a guarantee of actual future performance."
    )

# ==============================
# MAIN PREDICTION
# ==============================

if st.button("🚀 Predict My Performance"):

    # --------------------------
    # PREPARE STUDENT DATA
    # --------------------------

    new_student = pd.DataFrame({
        "Semester": [semester],
        "CGPA": [cgpa],
        "Attendance": [attendance],
        "Internal_Marks": [internal],
        "Assignment_Score": [assignment],
        "Quiz_Score": [quiz],
        "Study_Hours": [study_hours],
        "Backlogs": [backlogs],
        "Skill_Level": [skill]
    })

    # --------------------------
    # ML PREDICTION
    # --------------------------

    predicted_score = float(
        model.predict(new_student)[0]
    )

    predicted_score = max(
        0,
        min(100, predicted_score)
    )

    # --------------------------
    # RISK CALCULATION
    # --------------------------

    if predicted_score < 50:
        risk = "High"
    elif predicted_score < 70:
        risk = "Medium"
    else:
        risk = "Low"

    # ==========================
    # RESULTS
    # ==========================

    st.divider()

    st.header("📊 Your Results")

    # --------------------------
    # PERFORMANCE METRICS
    # --------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Predicted Performance",
            f"{predicted_score:.2f} / 100"
        )

    with col2:
        st.metric(
            "Academic Risk",
            risk
        )

    # ==========================
    # PERFORMANCE DASHBOARD
    # ==========================

    st.subheader("📈 Performance Dashboard")

    chart_data = pd.DataFrame({
        "Area": [
            "CGPA",
            "Attendance",
            "Internal Marks",
            "Assignment",
            "Quiz"
        ],
        "Score": [
            cgpa * 10,
            attendance,
            internal,
            assignment,
            quiz
        ]
    })

    st.bar_chart(
        chart_data.set_index("Area")
    )
    
        # ==========================
    # EXPLAINABLE AI
    # ==========================

    st.subheader("🔍 Why This Prediction?")

    feature_names = [
        "Semester",
        "CGPA",
        "Attendance",
        "Internal Marks",
        "Assignment Score",
        "Quiz Score",
        "Study Hours",
        "Backlogs",
        "Technical Skill"
    ]

    importance_data = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance_data = importance_data.sort_values(
        "Importance",
        ascending=False
    )

    st.bar_chart(
        importance_data.set_index("Feature")
    )

    # ==========================
    # STRENGTHS & WEAKNESSES
    # ==========================

    areas = {
        "Attendance": attendance,
        "Internal Marks": internal,
        "Assignment Score": assignment,
        "Quiz Score": quiz,
        "Study Hours": study_hours,
        "CGPA": cgpa * 10
    }

    strong_areas = [
        name
        for name, score in areas.items()
        if score >= 75
    ]

    weak_areas = [
        name
        for name, score in areas.items()
        if score < 60
    ]

    # --------------------------
    # STRONG AREAS
    # --------------------------

    st.subheader("💪 Strong Areas")

    if strong_areas:

        for area in strong_areas:
            st.write("✅", area)

    else:

        st.write(
            "No major strong area identified."
        )

    # --------------------------
    # AREAS TO IMPROVE
    # --------------------------

    st.subheader("⚠️ Areas to Improve")

    if weak_areas:

        for area in weak_areas:
            st.write("🔸", area)

    else:

        st.write(
            "No major weak area identified."
        )

    # ==========================
    # PERSONALIZED STUDY PLAN
    # ==========================

    st.divider()

    st.subheader(
        "📚 Personalized Weekly Study Plan"
    )

    # Recommended study time

    recommended_hours = max(
        2.0,
        study_hours + 1.0
    )

    st.info(
        f"🎯 Recommended focused study time: "
        f"{recommended_hours:.1f} hours/day"
    )

    # Weekly plan

    if weak_areas:

        st.write(
            "Based on your current performance, "
            "focus on these areas:"
        )

        st.write(
            ", ".join(weak_areas)
        )

        st.write("### 🗓️ This Week")

        if "Attendance" in weak_areas:

            st.write(
                "• Monday: Attend all classes "
                "and revise missed topics."
            )

        if "Internal Marks" in weak_areas:

            st.write(
                "• Tuesday: Revise important "
                "internal-exam topics."
            )

        if "Assignment Score" in weak_areas:

            st.write(
                "• Wednesday: Complete and review "
                "pending assignments."
            )

        if "Quiz Score" in weak_areas:

            st.write(
                "• Thursday: Practice topic-wise quizzes."
            )

        if "Study Hours" in weak_areas:

            st.write(
                "• Friday: Increase focused study "
                "time by 30–60 minutes."
            )

        if "CGPA" in weak_areas:

            st.write(
                "• Saturday: Revise your weakest "
                "academic subjects."
            )

        st.write(
            "• Sunday: Review your weekly progress "
            "and plan the next week."
        )

    else:

        st.success(
            "🎉 No major weak area detected. "
            "Continue your current study routine."
        )

    # ==========================
    # PERSONALIZED RECOMMENDATIONS
    # ==========================

    st.divider()

    st.subheader(
        "💡 Personalized Recommendations"
    )

    recommendations = []

    if attendance < 75:

        recommendations.append(
            "Improve attendance and maintain "
            "at least 75% attendance."
        )

    if internal < 60:

        recommendations.append(
            "Focus on internal exams and revise "
            "class notes regularly."
        )

    if assignment < 60:

        recommendations.append(
            "Complete assignments on time and "
            "improve assignment quality."
        )

    if quiz < 60:

        recommendations.append(
            "Practice more quizzes and "
            "topic-wise tests."
        )

    if study_hours < 2:

        recommendations.append(
            "Gradually increase daily study "
            "time to 2–3 hours."
        )

    if cgpa < 6.5:

        recommendations.append(
            "Focus on weak subjects and create "
            "a consistent weekly study plan."
        )

    if backlogs > 0:

        recommendations.append(
            "Prioritize clearing backlogs while "
            "maintaining current-semester studies."
        )

    if skill < 3:

        recommendations.append(
            "Develop technical skills through "
            "coding practice and small projects."
        )

    # --------------------------
    # CAREER RECOMMENDATIONS
    # --------------------------

    career_recommendations = {

        "AI/ML Engineer":
            "Build Python, NumPy, Pandas, "
            "Machine Learning and AI projects.",

        "Data Scientist":
            "Focus on Python, SQL, statistics, "
            "data analysis and visualization.",

        "Software Developer":
            "Strengthen DSA, OOP, Git and "
            "software development projects.",

        "Data Analyst":
            "Learn SQL, Excel, Python, Pandas "
            "and data visualization.",

        "Cybersecurity":
            "Learn networking, Linux, security "
            "fundamentals and ethical security practices.",

        "Cloud/DevOps":
            "Learn Linux, Git, Docker, cloud "
            "fundamentals and CI/CD.",

        "Higher Studies":
            "Focus on academic performance, "
            "core subjects and relevant entrance exams.",

        "Other":
            "Build strong programming fundamentals "
            "and complete practical projects."
    }

    recommendations.append(
        career_recommendations[career_goal]
    )

    # --------------------------
    # DISPLAY RECOMMENDATIONS
    # --------------------------

    if recommendations:

        for i, recommendation in enumerate(
            recommendations,
            1
        ):

            st.write(
                f"**{i}.** {recommendation}"
            )

    else:

        st.success(
            "Your current academic indicators are "
            "satisfactory. Continue your current study routine."
        )


# ==============================
# PROTOTYPE DISCLAIMER
# ==============================

st.divider()

st.caption(
    "Student360 AI is a prototype trained on synthetic student data. "
    "Predictions are estimates and should not be treated as guaranteed outcomes."
)
