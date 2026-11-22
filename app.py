
import os
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st


# ============================================================
# STUDENT360 AI
# ============================================================

st.set_page_config(
    page_title="Student360 AI",
    page_icon="🎓",
    layout="centered"
)

MODEL_FILE = "student360_model.pkl"
HISTORY_FILE = "student_progress.csv"

FEATURE_COLUMNS = [
    "Semester",
    "CGPA",
    "Attendance",
    "Internal_Marks",
    "Assignment_Score",
    "Quiz_Score",
    "Study_Hours",
    "Backlogs",
    "Skill_Level"
]


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


try:
    model = load_model()
except Exception as error:
    st.error(f"Unable to load {MODEL_FILE}.")
    st.error(f"Technical details: {error}")
    st.info(
        "Check that student360_model.pkl is present in the same "
        "GitHub repository as app.py."
    )
    st.stop()


# ============================================================
# APP HEADER
# ============================================================

st.title("🎓 Student360 AI")
st.caption("AI-Powered Student Performance & Academic Risk Analysis")
st.subheader("Student Performance Predictor")
st.write(
    "Enter your academic details to receive an estimated performance "
    "prediction, academic risk level, strengths, areas to improve, "
    "a study plan, and career guidance."
)
st.divider()


# ============================================================
# STUDENT INFORMATION
# ============================================================

st.header("📋 Student Information")

student_name = st.text_input("Student Name", value="Student")

semester = st.number_input(
    "Semester", min_value=1, max_value=8, value=5, step=1
)
cgpa = st.number_input(
    "CGPA", min_value=0.0, max_value=10.0, value=7.2, step=0.1
)
attendance = st.number_input(
    "Attendance (%)", min_value=0.0, max_value=100.0,
    value=82.0, step=1.0
)
internal = st.number_input(
    "Internal Marks", min_value=0.0, max_value=100.0,
    value=75.0, step=1.0
)
assignment = st.number_input(
    "Assignment Score", min_value=0.0, max_value=100.0,
    value=80.0, step=1.0
)
quiz = st.number_input(
    "Quiz Score", min_value=0.0, max_value=100.0,
    value=72.0, step=1.0
)
study_hours = st.number_input(
    "Study Hours per Day", min_value=0.0, max_value=24.0,
    value=3.0, step=0.5
)
backlogs = st.number_input(
    "Number of Backlogs", min_value=0, max_value=20,
    value=1, step=1
)
skill = st.slider(
    "Technical Skill Level", min_value=1, max_value=5, value=3
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


# ============================================================
# WHAT-IF PERFORMANCE SIMULATOR
# ============================================================

st.divider()
st.subheader("🔮 What-If Performance Simulator")
st.write(
    "Change study hours and attendance to see how the model's "
    "estimated prediction may change."
)

whatif_study_hours = st.slider(
    "What-If Study Hours/Day",
    min_value=0.0,
    max_value=12.0,
    value=min(12.0, float(study_hours)),
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
    whatif_data = pd.DataFrame([{
        "Semester": semester,
        "CGPA": cgpa,
        "Attendance": whatif_attendance,
        "Internal_Marks": internal,
        "Assignment_Score": assignment,
        "Quiz_Score": quiz,
        "Study_Hours": whatif_study_hours,
        "Backlogs": backlogs,
        "Skill_Level": skill
    }], columns=FEATURE_COLUMNS)

    try:
        whatif_score = float(model.predict(whatif_data)[0])
        whatif_score = max(0.0, min(100.0, whatif_score))
        st.metric(
            "What-If Predicted Performance",
            f"{whatif_score:.2f} / 100"
        )
        st.caption(
            "This is a model-based simulation, not a guarantee "
            "of future academic results."
        )
    except Exception as error:
        st.error(f"Simulation failed: {error}")


# ============================================================
# MAIN PREDICTION
# ============================================================

if st.button("🚀 Predict My Performance", type="primary"):

    student_data = pd.DataFrame([{
        "Semester": semester,
        "CGPA": cgpa,
        "Attendance": attendance,
        "Internal_Marks": internal,
        "Assignment_Score": assignment,
        "Quiz_Score": quiz,
        "Study_Hours": study_hours,
        "Backlogs": backlogs,
        "Skill_Level": skill
    }], columns=FEATURE_COLUMNS)

    # Make sure the model receives the expected input columns.
    try:
        predicted_score = float(model.predict(student_data)[0])
    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.stop()

    predicted_score = max(0.0, min(100.0, predicted_score))

    # Academic risk
    if predicted_score < 50:
        risk_level = "High"
    elif predicted_score < 70:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Performance category
    if predicted_score >= 80:
        performance_level = "Excellent 🏆"
    elif predicted_score >= 70:
        performance_level = "Good 👍"
    elif predicted_score >= 50:
        performance_level = "Needs Improvement 📈"
    else:
        performance_level = "At Risk ⚠️"

    # ========================================================
    # SAVE PREDICTION TO CSV
    # ========================================================

    new_record = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_Name": student_name,
        "Semester": semester,
        "CGPA": cgpa,
        "Attendance": attendance,
        "Internal_Marks": internal,
        "Assignment_Score": assignment,
        "Quiz_Score": quiz,
        "Study_Hours": study_hours,
        "Backlogs": backlogs,
        "Skill_Level": skill,
        "Career_Goal": career_goal,
        "Predicted_Performance": predicted_score,
        "Risk_Level": risk_level,
        "Performance_Level": performance_level
    }])

    try:
        if os.path.exists(HISTORY_FILE):
            old_records = pd.read_csv(HISTORY_FILE)
            all_records = pd.concat(
                [old_records, new_record],
                ignore_index=True
            )
        else:
            all_records = new_record

        all_records.to_csv(HISTORY_FILE, index=False)
    except Exception as error:
        st.warning(f"Prediction completed, but history was not saved: {error}")

    # ========================================================
    # RESULTS OVERVIEW
    # ========================================================

    st.divider()
    st.header("📊 Your Results")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric("Predicted Performance", f"{predicted_score:.2f}/100")
    with result_col2:
        st.metric("Academic Risk", risk_level)
    with result_col3:
        st.metric("Performance Level", performance_level)

    st.subheader("👤 Student Profile")
    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        st.write(f"**Student:** {student_name}")
        st.write(f"**Semester:** {semester}")
        st.write(f"**CGPA:** {cgpa:.1f}")
        st.write(f"**Career Goal:** {career_goal}")

    with profile_col2:
        st.write(f"**Attendance:** {attendance:.0f}%")
        st.write(f"**Study Hours:** {study_hours:.1f}/day")
        st.write(f"**Backlogs:** {backlogs}")
        st.write(f"**Technical Skill:** {skill}/5")

    # ========================================================
    # PERFORMANCE DASHBOARD
    # ========================================================

    st.subheader("📈 Performance Dashboard")

    dashboard_data = pd.DataFrame({
        "Area": [
            "CGPA", "Attendance", "Internal Marks",
            "Assignment", "Quiz"
        ],
        "Score": [
            cgpa * 10, attendance, internal, assignment, quiz
        ]
    })

    st.bar_chart(
        dashboard_data,
        x="Area",
        y="Score",
        height=350
    )

    # ========================================================
    # ACADEMIC STATUS
    # ========================================================

    st.subheader("🎓 Academic Status")

    if risk_level == "Low":
        st.success(
            "Your current indicators show a lower estimated academic risk."
        )
    elif risk_level == "Medium":
        st.warning(
            "Your indicators suggest moderate academic risk. "
            "Focus on areas that need improvement."
        )
    else:
        st.error(
            "Your indicators suggest higher academic risk. "
            "A consistent improvement plan is recommended."
        )

    # ========================================================
    # EXPLAINABLE AI / FEATURE IMPORTANCE
    # ========================================================

    st.subheader("🔍 Why This Prediction?")

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_

        if len(importances) == len(FEATURE_COLUMNS):
            display_names = [
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
                "Feature": display_names,
                "Importance": importances
            }).sort_values("Importance", ascending=False)

            st.bar_chart(
                importance_data.set_index("Feature"),
                height=350
            )
            st.caption(
                "Feature importance describes which inputs the model "
                "used most. It does not prove cause and effect."
            )
        else:
            st.info(
                "Feature importance cannot be displayed because the "
                "model feature count does not match the input columns."
            )
    else:
        st.info("Feature importance is not available for this model.")

    # ========================================================
    # PERFORMANCE TARGET
    # ========================================================

    st.subheader("🎯 Performance Goal")

    target_score = st.slider(
        "Set Your Target Performance",
        min_value=50,
        max_value=100,
        value=90,
        step=1,
        key="prediction_target"
    )

    points_needed = max(0.0, target_score - predicted_score)

    if points_needed > 0:
        st.info(
            f"You need approximately {points_needed:.1f} more predicted "
            f"points to reach your target of {target_score}/100."
        )
    else:
        st.success(f"You have reached your target of {target_score}/100!")

    # ========================================================
    # AI PERFORMANCE SUMMARY
    # ========================================================

    st.subheader("🧠 AI Performance Summary")

    if predicted_score >= 80:
        summary = (
            "Your predicted performance is strong. Maintain your study "
            "routine and continue developing your technical skills."
        )
    elif predicted_score >= 70:
        summary = (
            "Your predicted performance is satisfactory. Focus on weaker "
            "areas to improve your overall performance."
        )
    elif predicted_score >= 50:
        summary = (
            "Your predicted performance needs improvement. Follow the "
            "study plan and work on your weaker areas."
        )
    else:
        summary = (
            "Your predicted performance indicates higher academic risk. "
            "Focus on study consistency and clearing backlogs."
        )

    st.info(summary)

    # ========================================================
    # STRENGTHS AND AREAS TO IMPROVE
    # ========================================================

    areas = {
        "Attendance": attendance,
        "Internal Marks": internal,
        "Assignment Score": assignment,
        "Quiz Score": quiz,
        "Study Hours": study_hours,
        "CGPA": cgpa * 10
    }

    strong_areas = [
        name for name, score in areas.items() if score >= 75
    ]
    weak_areas = [
        name for name, score in areas.items() if score < 60
    ]

    st.subheader("💪 Strong Areas")
    if strong_areas:
        for area in strong_areas:
            st.write("✅", area)
    else:
        st.write("No major strong area identified.")

    st.subheader("⚠️ Areas to Improve")
    if weak_areas:
        for area in weak_areas:
            st.write("🔸", area)
    else:
        st.write("No major weak area identified.")

    # ========================================================
    # STUDY CONSISTENCY AND ACADEMIC CHECKS
    # ========================================================

    st.subheader("⏱️ Study Consistency")

    if study_hours < 2:
        st.warning(
            "Your current study time is below 2 hours/day. "
            "Try gradually increasing focused study time."
        )
    elif study_hours < 4:
        st.info(
            "You study around 2–4 hours/day. Maintaining consistency "
            "can help improve your performance."
        )
    else:
        st.success("You are maintaining a relatively high daily study duration.")

    if attendance < 75:
        st.warning(
            "Attendance is below 75%. Try to improve your class attendance."
        )

    if backlogs > 0:
        st.warning(
            f"You have {backlogs} backlog(s). Include backlog preparation "
            "in your weekly plan."
        )
    else:
        st.success("No backlogs reported.")

    # ========================================================
    # PERSONALIZED WEEKLY STUDY PLAN
    # ========================================================

    st.divider()
    st.subheader("📚 Personalized Weekly Study Plan")

    recommended_hours = max(2.0, study_hours + 1.0)
    st.info(
        f"Recommended focused study time: {recommended_hours:.1f} hours/day"
    )

    if weak_areas:
        st.write("Focus on these areas:")
        st.write(", ".join(weak_areas))
        st.write("### 🗓️ This Week")

        weekly_tasks = {
            "Attendance": "Monday: Attend classes and revise missed topics.",
            "Internal Marks": "Tuesday: Revise important internal-exam topics.",
            "Assignment Score": "Wednesday: Complete and review assignments.",
            "Quiz Score": "Thursday: Practice topic-wise quizzes.",
            "Study Hours": "Friday: Add 30–60 minutes of focused study.",
            "CGPA": "Saturday: Revise your weakest academic subjects."
        }

        for area in weak_areas:
            if area in weekly_tasks:
                st.write("•", weekly_tasks[area])

        st.write("• Sunday: Review progress and plan the next week.")
    else:
        st.success(
            "No major weak area detected. Continue your current study routine."
        )

    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

    st.divider()
    st.subheader("💡 Personalized Recommendations")

    recommendations = []

    if attendance < 75:
        recommendations.append(
            "Improve attendance and aim to maintain at least 75%."
        )
    if internal < 60:
        recommendations.append(
            "Revise class notes regularly and prepare for internal exams."
        )
    if assignment < 60:
        recommendations.append(
            "Complete assignments on time and improve their quality."
        )
    if quiz < 60:
        recommendations.append("Practice more quizzes and topic-wise tests.")
    if study_hours < 2:
        recommendations.append(
            "Gradually increase daily focused study time to 2–3 hours."
        )
    if cgpa < 6.5:
        recommendations.append(
            "Focus on weak subjects and follow a consistent study plan."
        )
    if backlogs > 0:
        recommendations.append(
            "Prioritize clearing backlogs while keeping up with current subjects."
        )
    if skill < 3:
        recommendations.append(
            "Improve technical skills through coding practice and projects."
        )

    career_recommendations = {
        "AI/ML Engineer": (
            "Build Python, NumPy, Pandas, Machine Learning and AI projects."
        ),
        "Data Scientist": (
            "Focus on Python, SQL, statistics, data analysis and visualization."
        ),
        "Software Developer": (
            "Strengthen DSA, OOP, Git and software development projects."
        ),
        "Data Analyst": (
            "Learn SQL, Excel, Python, Pandas and data visualization."
        ),
        "Cybersecurity": (
            "Learn networking, Linux, security fundamentals and ethical practices."
        ),
        "Cloud/DevOps": (
            "Learn Linux, Git, Docker, cloud fundamentals and CI/CD."
        ),
        "Higher Studies": (
            "Focus on academic performance, core subjects and entrance preparation."
        ),
        "Other": (
            "Build programming fundamentals and complete practical projects."
        )
    }

    recommendations.append(career_recommendations[career_goal])

    for number, recommendation in enumerate(recommendations, start=1):
        st.write(f"**{number}.** {recommendation}")


# ============================================================
# CAREER SKILL ROADMAP
# ============================================================

st.divider()
st.subheader("🚀 Career Skill Roadmap")

roadmap = {
    "AI/ML Engineer": [
        "Python", "NumPy and Pandas", "Statistics", "Machine Learning",
        "Deep Learning", "Projects", "Model Deployment"
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Pandas",
        "Data Visualization", "Machine Learning", "Projects"
    ],
    "Software Developer": [
        "Programming", "OOP", "Data Structures and Algorithms",
        "Git and GitHub", "Databases", "Projects", "System Design Basics"
    ],
    "Data Analyst": [
        "Excel", "SQL", "Python", "Pandas",
        "Statistics", "Data Visualization", "Projects"
    ],
    "Cybersecurity": [
        "Networking", "Linux", "Python", "Security Fundamentals",
        "Web Security", "Security Tools", "Projects"
    ],
    "Cloud/DevOps": [
        "Linux", "Git", "Docker", "Cloud Basics",
        "CI/CD", "Networking", "Projects"
    ],
    "Higher Studies": [
        "Core Subjects", "Academic Performance", "Research Basics",
        "Problem Solving", "Entrance Exam Preparation",
        "Projects", "Technical Writing"
    ],
    "Other": [
        "Programming", "Problem Solving", "Git and GitHub",
        "Communication", "Projects", "Domain Skills"
    ]
}

for number, roadmap_skill in enumerate(roadmap[career_goal], start=1):
    st.write(f"**{number}.** {roadmap_skill}")


# ============================================================
# STUDENT PROGRESS HISTORY
# ============================================================

st.divider()
st.subheader("📚 Student Progress History")

if os.path.exists(HISTORY_FILE):
    try:
        history = pd.read_csv(HISTORY_FILE)

        required_history_columns = [
            "Date",
            "Predicted_Performance"
        ]

        if all(
            column in history.columns
            for column in required_history_columns
        ):
            history["Date"] = pd.to_datetime(
                history["Date"],
                errors="coerce"
            )
            history["Predicted_Performance"] = pd.to_numeric(
                history["Predicted_Performance"],
                errors="coerce"
            )

            history = history.dropna(
                subset=["Date", "Predicted_Performance"]
            ).sort_values("Date")

            if not history.empty:
                latest_score = float(
                    history["Predicted_Performance"].iloc[-1]
                )
                average_score = float(
                    history["Predicted_Performance"].mean()
                )
                best_score = float(
                    history["Predicted_Performance"].max()
                )

                history_col1, history_col2, history_col3 = st.columns(3)

                with history_col1:
                    st.metric("Latest", f"{latest_score:.2f}")
                with history_col2:
                    st.metric("Average", f"{average_score:.2f}")
                with history_col3:
                    st.metric("Best", f"{best_score:.2f}")

                st.subheader("📈 Performance Trend")
                trend_data = history.set_index("Date")[
                    ["Predicted_Performance"]
                ]
                st.line_chart(trend_data, height=350)

                st.caption(
                    "This chart shows recorded model predictions over time. "
                    "It does not show verified exam results."
                )

                if len(history) >= 2:
                    previous_score = float(
                        history["Predicted_Performance"].iloc[-2]
                    )
                    score_change = latest_score - previous_score

                    st.subheader("📊 Latest Change")

                    if score_change > 0:
                        st.success(
                            f"Latest predicted performance increased by "
                            f"{score_change:.2f} points."
                        )
                    elif score_change < 0:
                        st.warning(
                            f"Latest predicted performance decreased by "
                            f"{abs(score_change):.2f} points."
                        )
                    else:
                        st.info(
                            "Latest predicted performance remained unchanged."
                        )

                st.subheader("🎯 Historical Target Tracking")
                history_target = st.slider(
                    "Choose a target for tracking",
                    min_value=50,
                    max_value=100,
                    value=90,
                    step=1,
                    key="history_target"
                )

                target_gap = history_target - latest_score

                if target_gap > 0:
                    st.info(
                        f"You are {target_gap:.2f} points below your target."
                    )
                else:
                    st.success("Your latest predicted score has reached the target.")

                st.subheader("🗂️ Prediction Records")
                st.dataframe(
                    history.sort_values("Date", ascending=False),
                    use_container_width=True
                )

                st.download_button(
                    label="⬇️ Download Progress History",
                    data=history.to_csv(index=False),
                    file_name="student360_progress.csv",
                    mime="text/csv"
                )
            else:
                st.info("No valid prediction history is available yet.")
        else:
            st.info(
                "The history file is missing required columns. "
                "Make a new prediction to create a valid record."
            )

    except Exception as error:
        st.warning(f"Could not read progress history: {error}")
else:
    st.info(
        "Your progress history will appear here after your first prediction."
    )


# ============================================================
# FINAL DISCLAIMER
# ============================================================

st.divider()
st.caption(
    "Student360 AI is an academic prototype. It uses a trained model "
    "to generate estimates, not guaranteed academic outcomes."
)
st.caption(
    "Feature importance describes model behavior and does not prove "
    "that a feature causes academic performance."
)
st.caption(
    "The app's local CSV history may not persist after a Streamlit "
    "Cloud environment restart. Avoid entering sensitive personal data."
)
