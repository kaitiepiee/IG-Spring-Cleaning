import streamlit as st
import json
import io

st.set_page_config(page_title="Instagram Spring Cleaning 🧹 ", page_icon="🧹")
st.markdown(
    """
    <h1 style='color:#C13584;'>Instagram Spring Cleaning🧹</h1>
    <p>Clean up Szn! See who follows you back and and who doesn’t hehehe </p>
    <p> This app processes your Instagram data *locally* in your browser. No data is collected or stored.</p>
    <p>📥 <a href='https://www.instagram.com/download/request/' target='_blank'>Click here to download your Instagram data</a> (please choose JSON format).</p>
    """,
    unsafe_allow_html=True
)

followers_file = st.file_uploader("Upload your `followers_1.json`", type="json")
following_file = st.file_uploader("Upload your `following.json`", type="json")

if followers_file and following_file:
    try:
        # Load and process data
        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        followers = set(user['string_list_data'][0]['value'] for user in followers_data)
        followees_data = following_data["relationships_following"]
        followees = set(user['string_list_data'][0]['value'] for user in followees_data)

        mutuals = sorted(followers & followees)
        ghosts = sorted(followees - followers)
        fans = sorted(followers - followees)

        def display_category(title, items, emoji):
            st.markdown(f"### {emoji} {title}")
            st.markdown(
                f"""
                <div style="background-color:#fafafa; padding:10px; border:1px solid #ddd; border-radius:10px; height:200px; overflow:auto; color:#262626;">
                    {'<br>'.join(items) if items else 'None'}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Display categories
        display_category("Mutuals", mutuals, "🤝")
        display_category("You follow, they don’t:", ghosts, "💔")
        display_category("They follow, you don’t:", fans, "👀")

        # Prepare text file for download
        output = io.StringIO()
        output.write("🤝 Mutuals:\n" + "\n".join(mutuals) + "\n\n")
        output.write("💔 You follow, they don’t:\n" + "\n".join(ghosts) + "\n\n")
        output.write("👀 They follow, you don’t:\n" + "\n".join(fans) + "\n")

        st.download_button(
            "📄 Download Results as .txt",
            data=output.getvalue(),
            file_name="ig_spring_cleaning.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
