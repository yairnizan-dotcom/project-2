import streamlit as st
import time

# --- הגדרות עיצוב עמוד ---
st.set_page_config(page_title="CinePredict AI - משחק מפיקים", page_icon="🎬")

# --- כותרת ראשית של האפליקציה ---
st.title("🎬 CinePredict AI: משחק המפיקים")
st.info("🤖 האם אתה שועל הוליוודי או שתרושש את הסטודיו? בנה סרט וגלה אם תעשה קופה!")

# --- ניהול תקציב התחלתי במשחק ---
if "studio_budget" not in st.session_state:
    st.session_state.studio_budget = 100000000  # 100 מיליון דולר לקופה שלך

st.sidebar.header("💼 מאזן הסטודיו שלך")
st.sidebar.metric(label="קופת הסטודיו", value=f"${st.session_state.studio_budget:,.0f}")

# --- חלק הקלט מהמשתמש ---
st.header("📝 בנה את הסרט הבא שלך")

movie_name = st.text_input("שם הסרט:", placeholder="לדוגמה: אווטאר 4 / מתקפת הטישיו")

# מאפיין 1: פופולריות (טווח משתמש: 1 עד 10)
# במשחק: זה הציון שקיבלת מהבמאי / קמפיין שיווקי
popularity = st.slider(
    "בחר את עוצמת הבאזז / פופולריות (מ-1 עד 10):",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5,
    help="ככל שהבאזז גבוה יותר, הסרט ימשוך יותר קהל."
)

# מאפיין 2: תקציב
budget = st.number_input(
    "הכנס את תקציב ההפקה (בדולרים):",
    min_value=1000000.0,
    max_value=300000000.0,
    value=30000000.0,
    step=1000000.0,
    format="%f"
)

# --- כפתור הפעלה ---
col1, col2 = st.columns([1, 1])
with col1:
    predict_button = st.button("🚀 שחרר את הסרט לאקרנים!", type="primary")
with col2:
    reset_button = st.button("🔄 התחל סטודיו חדש (איפוס כסף)")

if reset_button:
    st.session_state.studio_budget = 100000000
    st.rerun()

# --- תיבת התשובה (Answer Box) והלוגיקה של המשחק ---
if predict_button:
    if not movie_name:
        st.warning("⚠️ אנא הכנס את שם הסרט קודם לכן.")
    else:
        # אפקט טעינה קצר (בדיקת נתוני קופות)
        with st.spinner("סופרים כרטיסים בקופות בבתי הקולנוע..."):
            time.sleep(1.2)

        # משקולות המודל המקוריות
        w_popularity = 1605154.4964212137
        w_budget = 2.6858848237184723
        b = -25644372.266467094

        scaled_popularity = popularity * 20
        estimated_revenue = (w_popularity * scaled_popularity) + (w_budget * budget) + b
        display_revenue = max(0.0, estimated_revenue)
        
        # הרווח הנקי מהסרט (הכנסות פחות תקציב)
        net_profit = display_revenue - budget

        st.success(f"📊 התוצאות עבור הסרט: **{movie_name}** הגיעו!")

        # הצגת מדדים ב-Columns
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric(label="💰 הכנסות בבתי הקולנוע", value=f"${display_revenue:,.0f}")
        mcol2.metric(label="💸 תקציב שהושקע", value=f"${budget:,.0f}")
        mcol3.metric(label="📈 רווח / הפסד נקי", value=f"${net_profit:,.0f}", delta=f"${net_profit:,.0f}")

        # עדכון קופת הסטודיו
        st.session_state.studio_budget += net_profit

        # תגובות אופי לפי תוצאת המשחק
        if net_profit > 50000000:
            st.balloons()
            st.toast("🎉 להיט ענק! האוסקר בדרך!", icon="🏆")
            st.markdown("### 🌟 וואו! עשית היסטוריה בהוליווד!")
        elif net_profit > 0:
            st.toast("👍 סרט רווחי!", icon="💵")
            st.markdown("### 🙂 סרט טוב. כיסית את ההוצאות ויצאת הרווח!")
        else:
            st.toast("💥 פלופ ענק בקופות!", icon="💀")
            st.markdown("### 😱 נפילה! הבמאים זורקים עגבניות על הסט.")

        st.write(f"הפופולריות של **{popularity}** ותקציב של **${budget:,.0f}** הובילו לתוצאה הזו.")
