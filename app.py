import streamlit as st

from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

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

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 Adaptive Learning Agent")
st.caption("Teacher-designed pathways • AI-supported personalised practice")

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

    st.write("### How would you like to create the learning progression?")

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
        ["Practice", "Revision", "Assessment"],
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

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):
            st.session_state.teacher_page = "setup"
            st.rerun()

    with col2:

        if st.button(
            "Approve & Create Practice",
            type="primary",
            use_container_width=True
        ):

            st.session_state.progression = {
                1: level1,
                2: level2,
                3: level3,
                4: level4,
                5: level5
            }

            st.session_state.teacher_page = "ready"

            st.rerun()


# ==================================================
# PRACTICE READY
# ==================================================

elif st.session_state.teacher_page == "ready":

    st.subheader("🚀 Adaptive Practice Ready")

    st.success(
        f"{st.session_state.topic} practice has been created."
    )

    st.write("### Learning Progression")

    for level, description in st.session_state.progression.items():

        st.write(
            f"**Level {level}:** {description}"
        )

    st.divider()

    st.write("### Student Access")

    st.write(
        "Students use the **Student Practice** page."
    )

    st.info(
        "For this local prototype, use the Student Practice page "
        "from the Streamlit sidebar. When we deploy the app, "
        "we'll create proper student access."
    )

    if st.button(
        "Open Student Practice →",
        type="primary"
    ):
        st.switch_page("pages/Student_Practice.py")

    st.divider()

    st.write("### Teacher Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Students", "0")
    col2.metric("Questions Answered", "0")
    col3.metric("Need Support", "0")

    st.caption(
        "Live student data will appear here in a later version."
    )

    st.divider()

    if st.button("Create Another Practice"):
        st.session_state.teacher_page = "setup"
        st.rerun()