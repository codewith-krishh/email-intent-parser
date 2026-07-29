import streamlit as st
from email_parser import parse_email
import time

# 1. Page config MUST be first Streamlit command
st.set_page_config(page_title="Email Intent Parser", page_icon="📧")
st.title("📧 Email Intent Parser")
st.caption("Paste a raw customer email — get structured triage data instantly.")

# 2. Session state init
if "request_times" not in st.session_state:
    st.session_state.request_times = []

# 3. Inputs (must exist before you can reference them)

raw_email = st.text_area("Raw email text", height=200,
    placeholder="Paste the customer's email here...")

# 4. Single button — all checks happen inside this one block
if st.button("Analyze Email", type="primary"):
    if not raw_email.strip():
        st.warning("Please paste an email first.")
        st.stop()

    if len(raw_email) > 2000:
        st.error("Please keep sample emails under 2000 characters for this demo.")
        st.stop()

    if len(st.session_state.request_times) >= 5:
        st.error("Demo limit reached for this session — thanks for trying it out! DM me if you want to test more.")
        st.stop()

    st.session_state.request_times.append(time.time())

    with st.spinner("Parsing..."):
        result = parse_email(raw_email)

    urgency_color = {1: "🟢", 2: "🟢", 3: "🟡", 4: "🟠", 5: "🔴"}
    col1, col2 = st.columns(2)
    col1.metric("Intent", result["sender_intent"].replace("_", " ").title())
    col2.metric("Urgency", f'{urgency_color[result["urgency_score"]]} {result["urgency_score"]}/5')
    st.write(f"**Tone:** {result['tone'].title()}")
    st.info(f"**Action required:** {result['action_required']}")

    with st.expander("Raw JSON output"):
        st.json(result)