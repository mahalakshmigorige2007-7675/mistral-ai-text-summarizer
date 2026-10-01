import streamlit as st
from mistralai.client import Mistral

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Safe Mistral Text Summarizer",
    page_icon="📝",
    layout="centered"
)

# =====================================================
# TITLE
# =====================================================

st.title("📝 Mistral Text Summarizer")

st.write(
    "Enter your Mistral API key and text to generate a summary."
)

st.divider()

# =====================================================
# API KEY
# =====================================================

st.subheader("🔐 Mistral API Key")

api_key = st.text_input(
    "Enter your API key:",
    type="password",
    placeholder="Paste your Mistral API key here"
)

st.caption(
    "The key is used only for this session and is not written to a file."
)

# =====================================================
# SUMMARY SETTINGS
# =====================================================

st.subheader("⚙️ Summary Settings")

summary_style = st.selectbox(
    "Summary length:",
    ["Short", "Medium", "Detailed"]
)

# =====================================================
# TEXT INPUT
# =====================================================

st.subheader("📄 Text to Summarize")

text = st.text_area(
    "Paste your text:",
    height=250,
    placeholder="Paste your article, notes, or paragraph here..."
)

if text.strip():
    st.caption(
        f"Word count: {len(text.split())}"
    )

# =====================================================
# GENERATE SUMMARY
# =====================================================

if st.button(
    "✨ Generate Summary",
    use_container_width=True
):

    # Check API key
    if not api_key.strip():
        st.error("❌ Please enter your Mistral API key.")
        st.stop()

    # Check text
    if not text.strip():
        st.error("❌ Please enter some text.")
        st.stop()

    # Limit extremely large input
    if len(text) > 50000:
        st.error(
            "❌ Text is too large. Please use less than 50,000 characters."
        )
        st.stop()

    # =================================================
    # SUMMARY INSTRUCTION
    # =================================================

    if summary_style == "Short":

        instruction = """
Summarize the text in 3 to 5 sentences.
Include only the most important points.
"""

    elif summary_style == "Medium":

        instruction = """
Create a medium-length summary.
Include the main ideas and important details.
"""

    else:

        instruction = """
Create a detailed summary.
Include the main ideas, important facts,
and important supporting details.
"""

    # =================================================
    # PROMPT
    # =================================================

    prompt = f"""
You are a text summarization assistant.

{instruction}

Rules:
- Use simple English.
- Keep the original meaning.
- Do not invent information.
- Do not add information that is not in the original text.

Text to summarize:

{text}
"""

    # =================================================
    # MISTRAL REQUEST
    # =================================================

    try:

        with st.spinner("🤖 Generating summary..."):

            client = Mistral(
                api_key=api_key.strip()
            )

            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            summary = response.choices[0].message.content

        # =================================================
        # RESULT
        # =================================================

        st.success("✅ Summary generated successfully!")

        st.subheader("📌 Summary")

        st.write(summary)

        # =================================================
        # STATISTICS
        # =================================================

        original_words = len(text.split())
        summary_words = len(summary.split())

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Original Words",
                original_words
            )

        with col2:
            st.metric(
                "Summary Words",
                summary_words
            )

        # =================================================
        # DOWNLOAD
        # =================================================

        st.download_button(
            "⬇️ Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain",
            use_container_width=True
        )

    # =================================================
    # ERROR HANDLING
    # =================================================

    except Exception as e:

        error = str(e)

        if "429" in error:

            st.error(
                "⚠️ Mistral rate limit reached."
            )

            st.info(
                "Please wait before trying again. "
                "Do not repeatedly click the Generate button."
            )

        elif "401" in error:

            st.error(
                "🔑 Invalid Mistral API key."
            )

            st.info(
                "Check your API key and enter it again."
            )

        elif "403" in error:

            st.error(
                "🚫 Access denied."
            )

        elif "400" in error:

            st.error(
                "❌ Invalid request."
            )

        elif "500" in error or "502" in error or "503" in error:

            st.error(
                "⚠️ Mistral server is temporarily unavailable."
            )

            st.info(
                "Please try again later."
            )

        else:

            st.error(
                "❌ Something went wrong."
            )

            st.code(error)