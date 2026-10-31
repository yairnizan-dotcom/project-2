import streamlit as st
import time

# --- כותרת ראשית של האפליקציה ---
st.title("🎬 CinePredict AI")
st.info("🤖 מערכת לחיזוי רווחי סרטים לפי פופולריות ותקציב")

# --- חלק הקלט מהמשתמש ---
st.header("📝 הזנת פרטי הסרט")

# תיבות קלט פשוטות וברורות
movie_name = st.text_input("שם הסרט:", placeholder="לדוגמה: אווטאר")

# מאפיין 1: פופולריות (טווח משתמש: 1 עד 10)
popularity = st.number_input(
    "הכנס את מדד הפופולריות של הסרט (מ-1 עד 10):", 
    min_value=1.0, 
    max_value=10.0, 
    value=5.0
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
            
        # משקולות המודל המקוריות שסופקו
        w_popularity = 1605154.4964212137
        w_budget = 2.6858848237184723
        b = -25644372.266467094
        
        # התאמת קנה מידה (Scaling): הפיכת טווח 1-10 לטווח 1-200
        # כך שציון 10 הופך ל-200 ומניב תרומה מקסימלית של ~321 מיליון דולר
        scaled_popularity = popularity * 20
        
        # חישוב החיזוי לפי הנוסחה הליניארית עם הערך המותאם
        estimated_revenue = (w_popularity * scaled_popularity) + (w_budget * budget) + b
        
        # יצירת תיבת תשובה מעוצבת ונקייה בעזרת st.success ו-st.metric
        st.success(f"📊 התחזית עבור הסרט: **{movie_name}** מוכנה!")
        
        # הצגת התוצאה במדד (Metric) - אם התוצאה שלילית מוצג 0
        display_revenue = max(0.0, estimated_revenue)
        st.metric(label="💰 רווח משוער בקופות", value=f"${display_revenue:,.0f}")
        
        # פירוט קצר מתחת לתיבה
        st.write(f"לפי מודל החיזוי, סרט עם פופולריות של **{popularity}** (שקול ל-{scaled_popularity:.0f} במודל המקורי) ותקציב של **${budget:,.0f}** צפוי להניב רווחים אלו בקולנוע.")
