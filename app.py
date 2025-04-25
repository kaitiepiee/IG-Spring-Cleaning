import streamlit as st
import json
import io

st.title("💅 Instagram Follower Analyzer")

# Upload files
followers_file = st.file_uploader("Upload followers_1.json", type="json")
following_file = st.file_uploader("Upload following.json", type="json")

if followers_file and following_file:
    try:
        # Parse uploaded JSON files
        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        followers = set(user['string_list_data'][0]['value'] for user in followers_data)
        followees_data = following_data["relationships_following"]
        followees = set(user['string_list_data'][0]['value'] for user in followees_data)

        # Categorize
        mutuals = sorted(followers & followees)
        ghosts = sorted(followees - followers)
        fans = sorted(followers - followees)

        # Display
        st.subheader("🤝 Mutuals")
        st.write(mutuals or "None")

        st.subheader("💔 Ghosts (you follow, they don’t)")
        st.write(ghosts or "None")

        st.subheader("👀 Fans (they follow, you don’t)")
        st.write(fans or "None")

        # Prepare downloadable text
        output = io.StringIO()
        output.write("🤝 Mutuals:\n" + "\n".join(mutuals) + "\n\n")
        output.write("💔 Ghosts:\n" + "\n".join(ghosts) + "\n\n")
        output.write("👀 Fans:\n" + "\n".join(fans) + "\n")

        st.download_button(
            "📄 Download Results as .txt",
            data=output.getvalue(),
            file_name="insta_relationships.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
