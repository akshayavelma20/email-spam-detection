import streamlit as st
import pickle

model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.set_page_config(page_title="Email Spam Detector")

st.title("📧 Email Spam Detection System")
st.write("Enter an email message to check whether it is Spam or Not Spam.")

email_text = st.text_area("✉️ Email Content")

if st.button("Check Email"):
    if email_text.strip() == "":
        st.warning("Please enter an email message.")
    else:
        email_vector = vectorizer.transform([email_text])
        prediction = model.predict(email_vector)[0]
        result = "Spam" if prediction == 1 else "Not Spam"

        if result == "Spam":
            st.error("🚫 This email is SPAM")
        else:
            st.success("✅ This email is NOT SPAM")
