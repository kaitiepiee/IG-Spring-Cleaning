import streamlit as st
import json
import io

st.set_page_config(page_title="Instagram Spring Cleaning 🧹", page_icon="🧹")
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color:#C13584;'>✨ Instagram Spring Cleaning ✨</h1>
        <p style='font-size:18px;'>See your mutuals, who follows you back, and who doesn’t hehe 🧹</p>
        <p style='font-size:16px;'>This app processes your Instagram data <em>locally</em> in your browser for free!<br>
        No data is collected or stored. No sign-in needed.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

with st.expander("🚀 How to Use"):
    st.markdown(
        """
        <div style='padding: 10px; background-color: #fafafa; border-radius: 10px; border: 1px solid #e6e6e6;'>
            <ol style='font-size: 16px; color: #262626;'>
                <li>Go to <a href='https://accountscenter.instagram.com/info_and_permissions/' target='_blank'>Instagram Data Download</a> and request your data. (Select <b>all-time data</b> and <b>JSON format</b>.)</li><br>
                <li>When you receive your data via email, download and extract the <code>.zip</code> file.</li><br>
                <li>Locate the following files inside:
                    <ul>
                        <li><code>followers_1.json</code></li>
                        <li><code>following.json</code></li>
                    </ul>
                </li><br>
                <li>Come back to this web page.</li><br>
                <li>Upload both JSON files.</li><br>
                <li>Scroll through your categorized lists or download your results as a <code>.txt</code> file!</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)


followers_file = st.file_uploader("Upload your `followers_1.json` file", type="json")
following_file = st.file_uploader("Upload your `following.json` file", type="json")

if followers_file and following_file:
    try:
        # Load and process JSON files
        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        followers = set(user['string_list_data'][0]['value'] for user in followers_data)
        followees_data = following_data["relationships_following"]
        followees = set(user['string_list_data'][0]['value'] for user in followees_data)

        mutuals = sorted(followers & followees)
        ghosts = sorted(followees - followers)
        fans = sorted(followers - followees)

        def display_category(title, items, emoji):
            st.markdown(f"## {emoji} {title}")
            st.markdown(
                f"""
                <div style="
                    background-color:#fafafa;
                    padding:20px;
                    margin-bottom:20px;
                    border:1px solid #e6e6e6;
                    border-radius:15px;
                    height:250px;
                    overflow:auto;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                    color:#262626;
                    font-size:16px;">
                    {'<br>'.join(items) if items else 'None'}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Display sections
        display_category("Mutuals", mutuals, "🤝")
        display_category("You follow, they don’t", ghosts, "💔")
        display_category("They follow, you don’t", fans, "👀")

        # Prepare download file
        output = io.StringIO()
        output.write("🤝 Mutuals:\n" + "\n".join(mutuals) + "\n\n")
        output.write("💔 You follow, they don’t:\n" + "\n".join(ghosts) + "\n\n")
        output.write("👀 They follow, you don’t:\n" + "\n".join(fans) + "\n")

        st.download_button(
            label="📄 Download Results as .txt",
            data=output.getvalue(),
            file_name="ig_spring_cleaning.txt",
            mime="text/plain",
            help="Download your categorized follower list"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px; font-size: 15px; color: #888;'>
        made by the final girl 👩🏻‍💻<br><br>
        <a href='https://github.com/kaitiepiee' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/25/25231.png' width='25' style='margin: 0 10px;' />
        </a>
        <a href='https://instagram.com/kaitiepiee' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/2111/2111463.png' width='25' style='margin: 0 10px;' />
        </a>
        <a href='https://www.linkedin.com/in/kait-tighe/' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='25' style='margin: 0 10px;' />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


