import streamlit as st
import time

# הגדרת הדף
st.set_page_config(page_title="Hollywood Tycoon Clicker", page_icon="💰", layout="centered")

# --- אתחול הקופה של האולפן (Session State) ---
if "studio_bank" not in st.session_state:
    st.session_state.studio_bank = 100000000.0

# --- כותרת ומצב הקופה הנוכחי ---
st.title("💰 Hollywood Tycoon: קליקר האולפנים")
st.markdown("נסה להגדיל את קופת האולפן שלך מבלי לפשוט רגל! בכל סיבוב אתה משקיע תקציב ומקבל את הכנסות הסרט.")

# הצגת תקציב האולפן הנוכחי (יכול להציג גם מינוס וחובות)
st.metric(label="🏦 קופת האולפן הנוכחית שלך (Studio Bank)", value=f"${st.session_state.studio_bank:,.0f}")

st.divider()

# --- פרמטרים של הסרט הנוכחי ---
st.header("🎬 הפק את הסרט הבא שלך")

movie_name = st.text_input("💡 שם הסרט:", placeholder="לדוגמה: מטריקס 5")

# קביעת התקציב הכספי - פתוח לחלוטין לכל מספר (ללא max_value)
movie_budget = st.number_input(
    "💵 תקציב הפקה (בדוֹלָרִים):", 
    min_value=0.0, 
    value=50000000.0, 
    step=1000000.0,
    format="%f",
    help="אתה יכול להציב כאן כל מספר, גם אם הוא גבוה מהקופה שלך!"
)

# מדד פופולריות פשוט - עודכן לטווח של 0 עד 10
popularity = st.slider(
    "🔥 מדד פופולריות ובאזז מתוכנן:", 
    min_value=0.0, 
    max_value=10.0, 
    value=5.0
)

# --- כפתור ההפעלה ---
st.divider()
launch_movie = st.button("🚀 שחרר לקולנוע ועדכן קופה!")

if launch_movie:
    if not movie_name:
        st.warning("⚠️ אנא הכנס את שם הסרט קודם לכן.")
    else:
        # 1. הפחתת התקציב מהקופה (מאפשר כניסה למינוס וחובות)
        st.session_state.studio_bank -= movie_budget
        
        # אפקט טעינה קצר ומהיר
        with st.spinner('🎬 מריצים בבתי הקולנוע...'):
            time.sleep(0.5)
            
        # --- משקולות המודל המקוריות שלך (ללא שינוי) ---
        w_popularity = 1605154.4964212137
        w_budget = 2.6858848237184723
        b = -25644372.266467094
        
        # התאמת קנה מידה (Scaling) המקורית שלך
        scaled_popularity = popularity * 20
        
        # חישוב החיזוי לפי הנוסחה הליניארית המקורית
        estimated_revenue = (w_popularity * scaled_popularity) + (w_budget * movie_budget) + b
        display_revenue = max(0.0, estimated_revenue)
        
        # 2. הוספת ההכנסות בחזרה לקופת האולפן
        st.session_state.studio_bank += display_revenue
        
        # --- הצגת תוצאות הסיבוב ---
        net_result = display_revenue - movie_budget
        
        st.subheader(f"📊 תוצאות עבור: {movie_name}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="💰 הכנסות מהסרט", value=f"${display_revenue:,.0f}")
        with c2:
            st.metric(label="📈 רווח/הפסד נקי", value=f"${net_result:,.0f}", delta=f"${net_result:,.0f}")
            
        # הודעות פידבק מהירות
        if net_result > 0:
            st.success(f"🎉 להיט! הסרט הכניס יותר מתקציבו והרווח נשפך לקופה!")
        else:
            st.error(f"📉 פלופ! הסרט הפסיד כסף ורוקן חלק מהקופה של האולפן.")
            
        # הרצה מחדש אוטומטית כדי לעדכן את המטריקה העליונה של הבלנס בקופה
        time.sleep(1.2)
        st.rerun()

# --- כפתור איפוס ידני לקופה (למקרה שרוצים להתחיל מחדש) ---
st.sidebar.markdown("---")
if st.sidebar.button("🔄 איפוס קופה ל-100 מיליון"):
    st.session_state.studio_bank = 100000000.0
    st.rerun()
