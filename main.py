
import streamlit as st
import time

# --- כותרת ראשית של האפליקציה ---
st.title("🎬 CinePredict AI")
st.info("🤖 מערכת לחיזוי רווחי סרטים לפי פופולריות ותקציב")

# --- חלק הקלט מהמשתמש ---
st.header("📝 הזנת פרטי הסרט")

# תיבות קלט פשוטות וברורות
movie_name = st.text_input("שם הסרט:", placeholder="לדוגמה: אווטאר")

# מאפיין 1: פופולריות
popularity = st.number_input(
    "הכנס את מדד הפופולריות של הסרט (מ-1 עד 200):", 
    min_value=1.0, 
    max_value=200.0, 
    value=50.0
)

# מאפיין 2: תקציב
budget = st.number_input(
    "הכנס את תקציב הסרט (בדוֹלָרִים):", 
    min_value=0.0, 
    value=50000000.0, 
    step=1000000.0,
    format="%f"
)

# --- כפתור הפעלה ---
predict_button = st.button("🚀 חזה רווח צפוי")

# --- תיבת התשובה (Answer Box) ---
if predict_button:
    if not movie_name:
        st.warning("⚠️ אנא הכנס את שם הסרט קודם לכן.")
    else:
        # אפקט טעינה קצר בשביל ההרגשה של ה-AI
        with st.spinner('מחשב את הרווח הצפוי...'):
            time.sleep(1)
            
        # משקולות המודל שסופקו
        w_popularity = 1605154.4964212137
        w_budget = 2.6858848237184723
        b = -25644372.266467094
        
        # חישוב החיזוי לפי הנוסחה הליניארית
        estimated_revenue = (w_popularity * popularity) + (w_budget * budget) + b
        
        # יצירת תיבת תשובה מעוצבת ונקייה בעזרת st.success ו-st.metric
        st.success(f"📊 התחזית עבור הסרט: **{movie_name}** מוכנה!")
        
        # הצגת התוצאה במדד (Metric) - אם התוצאה שלילית מוצג 0
        display_revenue = max(0.0, estimated_revenue)
        st.metric(label="💰 רווח משוער בקופות", value=f"${display_revenue:,.0f}")
        
        # פירוט קצר מתחת לתיבה
        st.write(f"לפי מודל החיזוי, סרט עם פופולריות של **{popularity}** ותקציב של **${budget:,.0f}** צפוי להניב רווחים אלו בקולנוע.")
