import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="My Chatbot", page_icon="💬", layout="wide")
st.title("💬 My Knowledge Chatbot")

# Load CometChat credentials from Streamlit secrets
app_id = st.secrets["COMETCHAT_APP_ID"]
auth_key = st.secrets["COMETCHAT_AUTH_KEY"]
region = st.secrets["COMETCHAT_REGION"]

# A simple user login — in production you'd use real user IDs
user_id = "streamlit_user"
user_name = "Guest User"

cometchat_html = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ margin: 0; padding: 0; }}
    #cometchat-app {{
      width: 100%;
      height: 600px;
      border-radius: 12px;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <div id="cometchat-app"></div>

  <script src="https://unpkg.com/@cometchat/chat-uikit-javascript@4.0.0/CometChatUIKit/CometChatUIKit.js"></script>

  <script>
    const appSetting = new CometChatUIKit.UIKitSettingsBuilder()
      .setAppId("{app_id}")
      .setRegion("{region}")
      .setAuthKey("{auth_key}")
      .subscribePresenceForAllUsers()
      .build();

    CometChatUIKit.init(appSetting).then(() => {{
      // Log in the user
      CometChatUIKit.getLoggedinUser().then(user => {{
        if (!user) {{
          const newUser = new CometChat.User("{user_id}");
          newUser.setName("{user_name}");
          CometChatUIKit.createUser(newUser, "{auth_key}").then(createdUser => {{
            return CometChatUIKit.login(createdUser);
          }}).catch(() => {{
            // User may already exist, try logging in directly
            return CometChatUIKit.login("{user_id}", "{auth_key}");
          }}).then(() => {{
            launchChat();
          }});
        }} else {{
          launchChat();
        }}
      }});
    }}).catch(err => {{
      document.getElementById("cometchat-app").innerHTML =
        "<p style='color:red;padding:20px'>CometChat init failed: " + err + "</p>";
    }});

    function launchChat() {{
      const chatContainer = document.getElementById("cometchat-app");
      // Launch CometChat's built-in UI
      new CometChatUI().init(chatContainer);
    }}
  </script>
</body>
</html>
"""

components.html(cometchat_html, height=640, scrolling=False)
