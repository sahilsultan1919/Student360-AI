
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os


# ============================================================
# STUDENT360 AI
# AI-Powered Student Performance & Personalized Roadmap System
# ============================================================

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student360 AI",
    page_icon="🎓",
    layout="centered"
)

# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = joblib.load("student360_model.pkl")
except Exception as e:
    st.error("❌ Could not load student360_model.pkl")
    st.error(f"Error: {e}")
    st.stop()

# ============================================================
# FILES
# ============================================================

HISTORY_FILE = "student_progress.csv"

# ============================================================
# TITLE
# ============================================================

st.title("🎓 Student360 AI")

st.caption(
    "AI-Powered Student Performance & Academic Risk Analysis"
)

st.subheader("AI-Powered Student Performance Predictor")

st.write(
    "Enter your academic information to get a performance "
    "prediction, academic risk level, strengths, weaknesses, "
    "study recommendations, and career guidance."
)

st.divider()

# ============================================================
# STUDENT INFORMATION
# ============================================================

st.header("📋 Student Information")

student_name = st.text_input(
    "Student Name",
    value="Student"
)

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

# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

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

    try:
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

    except Exception as e:
        st.error(
            f"Could not run What-If simulation: {e}"
        )

# ============================================================
# MAIN PREDICTION
# ============================================================

if st.button("🚀 Predict My Performance"):

    # ========================================================
    # PREPARE STUDENT DATA
    # ========================================================

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

    # ========================================================
    # ML PREDICTION
    # ========================================================

    try:
        predicted_score = float(
            model.predict(new_student)[0]
        )

    except Exception as e:
        st.error(
            f"❌ Prediction failed: {e}"
        )
        st.stop()

    predicted_score = max(
        0,
        min(100, predicted_score)
    )

    # ========================================================
    # RISK CALCULATION
    # ========================================================

    if predicted_score < 50:
        risk = "High"
    elif predicted_score < 70:
        risk = "Medium"
    else:
        risk = "Low"

    # ========================================================
    # PERFORMANCE LEVEL
    # ========================================================

    if predicted_score >= 80:
        performance_level = "Excellent 🏆"
    elif predicted_score >= 70:
        performance_level = "Good 👍"
    elif predicted_score >= 50:
        performance_level = "Needs Improvement 📈"
    else:
        performance_level = "At Risk ⚠️"

    # ========================================================
    # SAVE PREDICTION HISTORY
    # ========================================================

    history_data = pd.DataFrame({
        "Date": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Student_Name": [student_name],
        "Semester": [semester],
        "CGPA": [cgpa],
        "Attendance": [attendance],
        "Internal_Marks": [internal],
        "Assignment_Score": [assignment],
        "Quiz_Score": [quiz],
        "Study_Hours": [study_hours],
        "Backlogs": [backlogs],
        "Skill_Level": [skill],
        "Career_Goal": [career_goal],
        "Predicted_Performance": [predicted_score],
        "Risk_Level": [risk],
        "Performance_Level": [performance_level]
    })

    try:
        if os.path.exists(HISTORY_FILE):
            existing_history = pd.read_csv(HISTORY_FILE)

            updated_history = pd.concat(
                [existing_history, history_data],
                ignore_index=True
            )
        else:
            updated_history = history_data

        updated_history.to_csv(
            HISTORY_FILE,
            index=False
        )

    except Exception as e:
        st.warning(
            f"Prediction completed, but history "
            f"could not be saved: {e}"
        )

    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()
    st.header("📊 Your Results")

    # ========================================================
    # THREE MAIN METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)

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

    with col3:
        st.metric(
            "Performance Level",
            performance_level
        )

    # ========================================================
    # STUDENT PROFILE SUMMARY
    # ========================================================

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

    chart_data = pd.DataFrame({
        "Area": [
            "CGPA",
            "Attendance",
            "Internal Marks",
            "Assignment",
            "Quiz"
        ],
        "Score": [
            float(cgpa * 10),
            float(attendance),
            float(internal),
            float(assignment),
            float(quiz)
        ]
    })

    st.bar_chart(
        chart_data,
        x="Area",
        y="Score",
        height=400
    )

    # ========================================================
    # ACADEMIC STATUS
    # ========================================================

    st.subheader("🎓 Academic Status")

    if risk == "Low":
        st.success(
            "Your current academic indicators show a "
            "lower estimated academic risk."
        )
    elif risk == "Medium":
        st.warning(
            "Your current indicators suggest moderate "
            "academic risk. Focus on your weaker areas."
        )
    else:
        st.error(
            "Your current indicators suggest higher "
            "academic risk. Immediate improvement is recommended."
        )

    # ========================================================
    # EXPLAINABLE AI
    # ========================================================

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

    if hasattr(model, "feature_importances_"):

        importance_data = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })

        importance_data = (
            importance_data
            .sort_values(
                "Importance",
                ascending=False
            )
        )

        st.bar_chart(
            importance_data.set_index("Feature"),
            height=400
        )

        st.caption(
            "Feature importance shows which inputs "
            "the model relied on most. It does not prove "
            "that a feature directly causes performance."
        )

    else:
        st.info(
            "Feature importance is not available "
            "for this model."
        )

    # ========================================================
    # PERFORMANCE GOAL
    # ========================================================

    st.subheader("🎯 Performance Goal")

    target_score = st.slider(
        "Set Your Target Performance",
        min_value=50,
        max_value=100,
        value=90,
        step=1
    )

    improvement_needed = max(
        0,
        target_score - predicted_score
    )

    if improvement_needed > 0:
        st.info(
            f"📈 You need approximately "
            f"{improvement_needed:.1f} more points "
            f"to reach your target of "
            f"{target_score}/100."
        )
    else:
        st.success(
            f"🎉 You have already reached your "
            f"target of {target_score}/100!"
        )

    # ========================================================
    # AI PERFORMANCE SUMMARY
    # ========================================================

    st.subheader("🧠 AI Performance Summary")

    if predicted_score >= 80:
        summary = (
            "Your predicted performance is strong. "
            "Maintain your current academic routine "
            "and continue developing your technical skills."
        )
    elif predicted_score >= 70:
        summary = (
            "Your predicted performance is satisfactory. "
            "Focus on your weaker areas to improve "
            "your overall performance."
        )
    elif predicted_score >= 50:
        summary = (
            "Your predicted performance needs improvement. "
            "Follow the personalized study plan and "
            "focus on your weak areas."
        )
    else:
        summary = (
            "Your predicted performance indicates "
            "higher academic risk. Focus on weak areas, "
            "study consistency, and clearing backlogs."
        )

    st.info(summary)

    # ========================================================
    # STRENGTHS & WEAKNESSES
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
        name
        for name, score in areas.items()
        if score >= 75
    ]

    weak_areas = [
        name
        for name, score in areas.items()
        if score < 60
    ]

    # ========================================================
    # STRONG AREAS
    # ========================================================

    st.subheader("💪 Strong Areas")

    if strong_areas:
        for area in strong_areas:
            st.write("✅", area)
    else:
        st.write(
            "No major strong area identified."
        )

    # ========================================================
    # AREAS TO IMPROVE
    # ========================================================

    st.subheader("⚠️ Areas to Improve")

    if weak_areas:
        for area in weak_areas:
            st.write("🔸", area)
    else:
        st.write(
            "No major weak area identified."
        )

    # ========================================================
    # STUDY CONSISTENCY ANALYSIS
    # ========================================================

    st.subheader("⏱️ Study Consistency")

    if study_hours < 2:
        st.warning(
            "Your current study time is below 2 hours/day. "
            "Try gradually increasing focused study time."
        )
    elif study_hours < 4:
        st.info(
            "You currently study around 2–4 hours/day. "
            "Maintaining consistency can help improve performance."
        )
    else:
        st.success(
            "You are maintaining a relatively high "
            "daily study duration."
        )

    # ========================================================
    # ATTENDANCE ANALYSIS
    # ========================================================

    if attendance < 75:
        st.warning(
            "⚠️ Attendance is below 75%. "
            "Improving attendance may help your academic routine."
        )

    # ========================================================
    # BACKLOG ANALYSIS
    # ========================================================

    if backlogs > 0:
        st.warning(
            f"📚 You currently have {backlogs} backlog(s). "
            "Include backlog preparation in your weekly plan."
        )
    else:
        st.success(
            "✅ No backlogs reported."
        )

    # ========================================================
    # PERSONALIZED WEEKLY STUDY PLAN
    # ========================================================

    st.divider()

    st.subheader(
        "📚 Personalized Weekly Study Plan"
    )

    recommended_hours = max(
        2.0,
        study_hours + 1.0
    )

    st.info(
        f"🎯 Recommended focused study time: "
        f"{recommended_hours:.1f} hours/day"
    )

    if weak_areas:

        st.write(
            "Based on your current performance, "
            "focus on these areas:"
        )

        st.write(", ".join(weak_areas))

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

    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

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

    # ========================================================
    # CAREER RECOMMENDATIONS
    # ========================================================

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

    # ========================================================
    # DISPLAY RECOMMENDATIONS
    # ========================================================

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


# ============================================================
# CAREER SKILL ROADMAP
# ============================================================

st.divider()

st.subheader("🚀 Career Skill Roadmap")

roadmap = {
    "AI/ML Engineer": [
        "Python",
        "NumPy & Pandas",
        "Statistics",
        "Machine Learning",
        "Deep Learning",
        "Projects",
        "Model Deployment"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Pandas",
        "Data Visualization",
        "Machine Learning",
        "Projects"
    ],

    "Software Developer": [
        "Programming",
        "OOP",
        "DSA",
        "Git & GitHub",
        "Databases",
        "Projects",
        "System Design Basics"
    ],

    "Data Analyst": [
        "Excel",
        "SQL",
        "Python",
        "Pandas",
        "Statistics",
        "Visualization",
        "Projects"
    ],

    "Cybersecurity": [
        "Networking",
        "Linux",
        "Python",
        "Security Fundamentals",
        "Web Security",
        "Security Tools",
        "Projects"
    ],

    "Cloud/DevOps": [
        "Linux",
        "Git",
        "Docker",
        "Cloud Basics",
        "CI/CD",
        "Networking",
        "Projects"
    ],

    "Higher Studies": [
        "Core Subjects",
        "Academic Performance",
        "Research Basics",
        "Problem Solving",
        "Entrance Exam Preparation",
        "Projects",
        "Technical Writing"
    ],

    "Other": [
        "Programming",
        "Problem Solving",
        "Git & GitHub",
        "Communication",
        "Projects",
        "Domain Skills"
    ]
}

selected_roadmap = roadmap[career_goal]

for index, skill_name in enumerate(
    selected_roadmap,
    1
):
    st.write(
        f"**{index}.** {skill_name}"
    )


# ============================================================
# PROGRESS HISTORY
# ============================================================

st.divider()

st.subheader("📚 Student Progress History")

if os.path.exists(HISTORY_FILE):

    try:
        history = pd.read_csv(
            HISTORY_FILE
        )

        if not history.empty:

            latest_score = float(
                history[
                    "Predicted_Performance"
                ].iloc[-1]
            )

            average_score = float(
                history[
                    "Predicted_Performance"
                ].mean()
            )

            best_score = float(
                history[
                    "Predicted_Performance"
                ].max()
            )

            hcol1, hcol2, hcol3 = st.columns(3)

            with hcol1:
                st.metric(
                    "Latest",
                    f"{latest_score:.2f}"
                )

            with hcol2:
                st.metric(
                    "Average",
                    f"{average_score:.2f}"
                )

            with hcol3:
                st.metric(
                    "Best",
                    f"{best_score:.2f}"
                )

            st.write("### 📈 Performance Trend")

            trend_data = history[
                ["Date", "Predicted_Performance"]
            ].copy()

            trend_data["Date"] = pd.to_datetime(
                trend_data["Date"],
                errors="coerce"
            )

            trend_data = trend_data.dropna(
                subset=["Date"]
            )

            trend_data = trend_data.set_index(
                "Date"
            )

            st.line_chart(
                trend_data[
                    "Predicted_Performance"
                ]
            )

            if len(history) >= 2:

                previous_score = float(
                    history[
                        "Predicted_Performance"
                    ].iloc[-2]
                )

                change = (
                    latest_score
                    - previous_score
                )

                st.write("### 📊 Latest Change")

                if change > 0:
                    st.success(
                        f"📈 Your latest predicted "
                        f"performance increased by "
                        f"{change:.2f} points."
                    )

                elif change < 0:
                    st.warning(
                        f"📉 Your latest predicted "
                        f"performance decreased by "
                        f"{abs(change):.2f} points."
                    )

                else:
                    st.info(
                        "Your latest predicted performance "
                        "remained unchanged."
                    )

            st.write("### 🎯 Historical Target Tracking")

            history_target = st.slider(
                "Choose a target for tracking",
                min_value=50,
                max_value=100,
                value=90,
                step=1,
                key="history_target"
            )

            target_difference = (
                history_target - latest_score
            )

            if target_difference > 0:
                st.info(
                    f"You are approximately "
                    f"{target_difference:.2f} points "
                    f"below your target."
                )
            else:
                st.success(
                    "🎉 Your latest predicted "
                    "performance has reached your target."
                )

            st.write("### 🗂️ Prediction Records")

            st.dataframe(
                history,
                use_container_width=True
            )

            csv_data = history.to_csv(
                index=False
            )

            st.download_button(
                label="⬇️ Download Progress History",
                data=csv_data,
                file_name="student_progress.csv",
                mime="text/csv"
            )

        else:
            st.info(
                "No prediction history available yet."
            )

    except Exception as e:
        st.warning(
            f"Could not read progress history: {e}"
        )

else:
    st.info(
        "Your prediction history will appear here "
        "after you make your first prediction."
    )


# ============================================================
# FINAL DISCLAIMER
# ============================================================

st.divider()

st.caption(
    "Student360 AI is a prototype trained on synthetic "
    "student data. Predictions are estimates and should "
    "not be treated as guaranteed academic outcomes."
)

st.caption(
    "Feature importance describes model behavior and "
    "does not establish causal relationships."
)

st.caption(
    "Student data should be handled responsibly and "
    "sensitive personal information should not be entered."
)
