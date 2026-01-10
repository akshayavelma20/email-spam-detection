import streamlit as st
import pickle
import mysql.connector

model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@20",
        database="email_spam_db"
    )

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

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO email_logs (email_text, prediction) VALUES (%s, %s)",
                (email_text, result)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Database error: {e}")

        if result == "Spam":
            st.error("🚫 This email is SPAM")
        else:
            st.success("✅ This email is NOT SPAM")
