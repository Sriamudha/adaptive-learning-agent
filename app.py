import streamlit as st
import uuid

from supabase import create_client

# --------------------------------------------------
# SUPABASE CONNECTION
# --------------------------------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Adaptive Learning Agent",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "teacher_page" not in st.session_state:
    st.session_state.teacher_page = "setup"

if "subject" not in st.session_state:
    st.session_state.subject = "MYP 4 Mathematics"

if "topic" not in st.session_state:
    st.session_state.topic = "Quadratic Equations"

if "progression" not in st.session_state:
    st.session_state.progression = {}

if "practice_id" not in st.session_state:
    st.session_state.practice_id = None

if "practice_code" not in st.session_state:
    st.session_state.practice_code = None

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 Adaptive Learning Agent")

st.caption(
    "Teacher-designed pathways • AI-supported personalised practice"
)

st.divider()

# ==================================================
# TEACHER SETUP
# ==================================================

if st.session_state.teacher_page == "setup":

    st.subheader("👩‍🏫 Create Adaptive Practice")

    subject = st.text_input(
        "Subject",
        value="MYP 4 Mathematics"
    )

    topic = st.text_input(
        "Topic",
        value="Quadratic Equations"
    )

    st.write(
        "### How would you like to create the learning progression?"
    )

    method = st.radio(
        "Choose one",
        [
            "✨ Generate with AI",
            "✏️ Create my own",
            "🤝 Help me create one with AI"
        ],
        label_visibility="collapsed"
    )

    st.write("### Purpose")

    purpose = st.radio(
        "Purpose",
        [
            "Practice",
            "Revision",
            "Assessment"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    duration = st.selectbox(
        "Practice duration",
        [
            "10 minutes",
            "15 minutes",
            "20 minutes",
            "30 minutes"
        ],
        index=1
    )

    st.divider()

    if st.button(
        "Create Learning Progression",
        type="primary",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            st.session_state.subject = subject
            st.session_state.topic = topic
            st.session_state.method = method
            st.session_state.purpose = purpose
            st.session_state.duration = duration

            st.session_state.teacher_page = "progression"

            st.rerun()


# ==================================================
# PROGRESSION BUILDER
# ==================================================

elif st.session_state.teacher_page == "progression":

    st.subheader("📈 Review Learning Progression")

    st.write(
        f"**Subject:** {st.session_state.subject}"
    )

    st.write(
        f"**Topic:** {st.session_state.topic}"
    )

    st.info(
        "For this prototype, the progression is pre-generated. "
        "Next we will connect AI so it creates the progression."
    )

    level1 = st.text_area(
        "Level 1 — Foundation",
        "Factorise simple monic quadratics"
    )

    level2 = st.text_area(
        "Level 2 — Developing",
        "Solve quadratic equations by factorisation"
    )

    level3 = st.text_area(
        "Level 3 — Secure",
        "Solve quadratics requiring rearrangement or increased complexity"
    )

    level4 = st.text_area(
        "Level 4 — Application",
        "Apply quadratic equations to contextual problems"
    )

    level5 = st.text_area(
        "Level 5 — Transfer",
        "Explain, justify and generalise mathematical reasoning"
    )

    st.caption(
        "The teacher can edit any level before approving the pathway."
    )

    st.divider()

    col1, col2 = st.columns(2)

    # -------------------------------
    # BACK BUTTON
    # -------------------------------

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.teacher_page = "setup"
            st.rerun()

    # -------------------------------
    # CREATE PRACTICE
    # -------------------------------

    with col2:

        if st.button(
            "Approve & Create Practice",
            type="primary",
            use_container_width=True
        ):

            progression = {
                1: level1,
                2: level2,
                3: level3,
                4: level4,
                5: level5
            }

            # Generate student practice code
            practice_code = str(
                uuid.uuid4()
            )[:6].upper()

            try:

                # ----------------------------------
                # SAVE PRACTICE TO SUPABASE
                # ----------------------------------

                practice_result = (
                    supabase
                    .table("practices")
                    .insert({
                        "practice_code": practice_code,
                        "subject": st.session_state.subject,
                        "topic": st.session_state.topic,
                        "purpose": st.session_state.purpose,
                        "duration_minutes": int(
                            st.session_state.duration.split()[0]
                        )
                    })
                    .execute()
                )

                practice_id = (
                    practice_result.data[0]["id"]
                )

                # ----------------------------------
                # SAVE PROGRESSION TO SUPABASE
                # ----------------------------------

                for level, description in progression.items():

                    (
                        supabase
                        .table("progression")
                        .insert({
                            "practice_id": practice_id,
                            "level": level,
                            "skill": f"Level {level}",
                            "description": description
                        })
                        .execute()
                    )

                # ----------------------------------
                # SAVE LOCALLY FOR THIS TEACHER
                # ----------------------------------

                st.session_state.progression = progression

                st.session_state.practice_id = (
                    practice_id
                )

                st.session_state.practice_code = (
                    practice_code
                )

                st.session_state.teacher_page = "ready"

                st.rerun()

            except Exception as e:

                st.error(
                    "The practice could not be saved to Supabase."
                )

                st.code(str(e))


# ==================================================
# PRACTICE READY
# ==================================================

elif st.session_state.teacher_page == "ready":

    st.subheader("🚀 Adaptive Practice Ready")

    st.success(
        f"{st.session_state.topic} practice has been created."
    )

    # --------------------------------------------------
    # PRACTICE CODE
    # --------------------------------------------------

    st.write("### Practice Code")

    st.code(
        st.session_state.practice_code
    )

    st.caption(
        "Students will use this code to join this practice."
    )

    # --------------------------------------------------
    # LEARNING PROGRESSION
    # --------------------------------------------------

    st.write("### Learning Progression")

    for level, description in (
        st.session_state.progression.items()
    ):

        st.write(
            f"**Level {level}:** {description}"
        )

    st.divider()

    # --------------------------------------------------
    # STUDENT ACCESS
    # --------------------------------------------------

    st.write("### Student Access")

    st.write(
        "Students use the **Student Practice** page."
    )

    if st.button(
        "Open Student Practice →",
        type="primary"
    ):

        st.switch_page(
            "pages/Student_Practice.py"
        )

    st.divider()

    # ==================================================
    # LIVE TEACHER DASHBOARD
    # ==================================================

    st.write("### 📊 Teacher Dashboard")

    try:

        # ----------------------------------------------
        # GET STUDENTS
        # ----------------------------------------------

        student_result = (
            supabase
            .table("students")
            .select("*")
            .eq(
                "practice_id",
                st.session_state.practice_id
            )
            .execute()
        )

        students = student_result.data

        # ----------------------------------------------
        # GET ATTEMPTS
        # ----------------------------------------------

        attempt_result = (
            supabase
            .table("attempts")
            .select("*")
            .eq(
                "practice_id",
                st.session_state.practice_id
            )
            .execute()
        )

        attempts = attempt_result.data

        # ----------------------------------------------
        # CALCULATE DASHBOARD VALUES
        # ----------------------------------------------

        total_students = len(students)

        total_attempts = len(attempts)

        support_student_ids = set()

        for attempt in attempts:

            action = (
                attempt.get("agent_action") or ""
            ).lower()

            evaluation = (
                attempt.get("evaluation") or ""
            ).lower()

            if (
                "support" in action
                or "incorrect" in evaluation
                or "needs support" in evaluation
            ):

                support_student_ids.add(
                    attempt.get("student_id")
                )

        need_support = len(
            support_student_ids
        )

        # ----------------------------------------------
        # METRICS
        # ----------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Students",
            total_students
        )

        col2.metric(
            "Questions Answered",
            total_attempts
        )

        col3.metric(
            "Need Support",
            need_support
        )

        # ----------------------------------------------
        # STUDENT PROGRESS
        # ----------------------------------------------

        if students:

            st.write("#### Student Progress")

            for student in students:

                student_name = student.get(
                    "student_name",
                    "Student"
                )

                current_level = student.get(
                    "current_level",
                    1
                )

                status = student.get(
                    "status",
                    "Developing"
                )

                st.write(
                    f"**{student_name}** — "
                    f"Level {current_level} — "
                    f"{status}"
                )

        else:

            st.info(
                "No students have joined this practice yet."
            )

        # ----------------------------------------------
        # REFRESH
        # ----------------------------------------------

        if st.button("🔄 Refresh Dashboard"):

            st.rerun()

    except Exception as e:

        st.warning(
            "The dashboard could not load student data yet."
        )

        st.code(str(e))

    st.divider()

    # --------------------------------------------------
    # CREATE ANOTHER PRACTICE
    # --------------------------------------------------

    if st.button(
        "Create Another Practice"
    ):

        st.session_state.teacher_page = "setup"

        st.session_state.practice_id = None

        st.session_state.practice_code = None

        st.session_state.progression = {}

        st.rerun()