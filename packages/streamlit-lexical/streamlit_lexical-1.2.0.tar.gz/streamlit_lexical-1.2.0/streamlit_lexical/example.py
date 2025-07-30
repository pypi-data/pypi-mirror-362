import streamlit as st
from __init__ import streamlit_lexical


def update_val():
    new_content = "# New Heading\n\n\n\nThis is updated content in **Markdown**."
    st.session_state["editor_content"] = new_content


st.write("#")
st.header("Lexical Rich Text Editor")
# Initialize the session state for editor content
if "editor_content" not in st.session_state:
    st.session_state["editor_content"] = "# initial **value**\n\ntest"

col1, col2 = st.columns(2)
with col1:
    # Button to update content
    if st.button("Update Editor Content"):
        update_val()

with col2:
    if st.button("Append Content"):
        st.session_state["editor_content"] += (
            "\n\nThis is appended content in **Markdown**."
        )

# Create an instance of our component
markdown = streamlit_lexical(
    value=st.session_state["editor_content"],
    placeholder="Enter some rich text",
    key="editor",
    height=300,
    overwrite=True,
    on_change=lambda: st.session_state.update(
        {"editor_content": st.session_state.get("editor")}
    ),
)
st.markdown(markdown)
st.markdown("---")

# Display the current content in session state (for debugging)
st.write("Current content in session state:\n", st.session_state["editor_content"])
