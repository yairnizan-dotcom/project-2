import streamlit as st
import time
import random

# הגדרת הדף
st.set_page_config(page_title="Hollywood Studio Tycoon", page_icon="🎮", layout="centered")

# --- כותרת וסיפור המשחק ---
st.title("🎮 Hollywood Studio Tycoon: הדרך לאוסקר")
st.markdown("""
### 🎬 משימת חייך: להציל את אולפני הקולנוע!
המועצה החליטה לתת לך צ'ק של **$50,000,000** ותקציב של **10 נקודות השראה (Creative Points)**. 
עליך לתמרן בין תקציב הכסף לבין הפופולריות והבאזז כדי לבנות את שובר הקופות הגדול ביותר בהיסטוריה.

⚠️ **חוקי הברזל:** 
* כל נקודת השראה שתשקיע בשיווק ובבאזז מעלה את הפופולריות ב-1 (מקסימום 10).
* התקציב הכספי המינימלי לסרט הוא $1,000,000.
""")

st.divider()

# --- שלב א': יצירת הסרט ---
st.header("📝 שלב 1: כתיבת הקונספט")

col1, col2 = st.columns(2)
with col1:
    movie_name = st.text_input("💡 שם הסרט שלך:", placeholder="לדוגמה: מהיר ועצבני 24")
with col2:
    genre = st.selectbox("🎭 ז'אנר:", [
        "אקשן חלל מפוצץ 🚀", 
        "קומדיית טעויות קורעת 🍿", 
        "אימה קלאוסטרופובי 👻", 
        "דרמת אוסקרים מרגשת 🏆"
    ])

# --- שלב ב': ניהול משאבים (מכניקת משחק) ---
st.header("📊 שלב 2: הקצאת משאבי הפקה")
st.info("💡 יש לך **10 נקודות השראה** לחלק. השתמש בהן בחוכמה!")

# בחירת רמת פופולריות בעזרת נקודות השראה (משפיע ישירות על ה-Popularity שבין 1 ל-10)
points_for_buzz = st.slider(
    "🔥 כמה נקודות תשקיע בקמפיין שיווק ובאזז תקשורתי?", 
    min_value=1, 
    max_value=10, 
    value=5,
    help="כל נקודה שווה לדרגת פופולריות אחת במודל"
)

remaining_points = 10 - points_for_buzz
st.write(f"🌟 נקודות השראה שנותרו להפקת האפקטים והתפאורה: **{remaining_points}**")

# קביעת התקציב הכספי
budget = st.number_input(
    "💵 תקציב כספי מהאולפן (בדוֹלָרִים):", 
    min_value=1000000.0, 
    max_value=300000000.0,
    value=50000000.0, 
    step=5000000.0,
    format="%f"
)

# אלמנט משחקי: בחירת כוכב ראשי (מוסיף באזז רנדומלי או סיכון תקציבי)
star_actor = st.radio(
    "🌟 בחר שחקן ראשי לסרט (אלמנט סיכון):",
    [
        "שחקן אנונימי וזול (בטוח, ללא השפעה)", 
        "כוכב אקשן מזדקן (סיכוי מוגבר לבאזז, עלול לעשות פדיחות ברשת)", 
        "מגה-סטאר הוליוודי (מבטיח מינימום פופולריות 7, אבל גוזל 20% מהתקציב על שכר)"
    ]
)

# --- כפתור ההפעלה: ערב הבכורה ---
st.divider()
launch_game = st.button("🎬 שלח את הסרט לבתי הקולנוע! 🍿")

if launch_game:
    if not movie_name:
        st.error("⚠️ אי אפשר להקרין סרט בלי שם! המפיקים זורקים אותך מהחדר.")
    else:
        # לוגיקת משחק: השפעת בחירת השחקן על הפרמטרים
        game_popularity = float(points_for_buzz)
        game_budget = budget
        
        if "מגה-סטאר" in star_actor:
            game_popularity = max(7.0, game_popularity)
            game_budget += (budget * 0.20)  # תוספת תקציב של 20% עבור השחקן
        elif "מזדקן" in star_actor:
            # אלמנט רנדומלי של מזל
            luck = random.choice(["good", "bad"])
            if luck == "good":
                st.toast("🎉 המזל איתך! השחקן המזדקן הפך לויראלי בטיקטוק!")
                game_popularity = min(10.0, game_popularity + 2)
            else:
                st.toast("📉 אאוץ'! השחקן הראשי הסתבך בשערורייה ציבורית ערב הבכורה.")
                game_popularity = max(1.0, game_popularity - 2)

        # מתח משחקי
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
            
        with st.spinner('🎬 סופרים את כרטיסי הכניסה...'):
            time.sleep(1)

        # --- מנוע החישוב המקורי שלך (המשקולות נשמרו במדויק) ---
        w_popularity = 1605154.4964212137
        w_budget = 2.6858848237184723
        b = -25644372.266467094
        
        # התאמת קנה המידה המקורית שלך (1-10 הופך ל-1-200)
        scaled_popularity = game_popularity * 20
        
        # חישוב הרווח לפי הנוסחה המקורית
        estimated_revenue = (w_popularity * scaled_popularity) + (w_budget * game_budget) + b
        display_revenue = max(0.0, estimated_revenue)
        
        # --- מסך התוצאות (לוח הניקוד) ---
        st.subheader("📊 דוח רווח והפסד קולנועי")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="💰 הכנסות סופיות בקופות", value=f"${display_revenue:,.0f}")
        with col_res2:
            net_profit = display_revenue - game_budget
            st.metric(label="📈 רווח נקי (או הפסד)", value=f"${net_profit:,.0f}", delta=f"${net_profit:,.0f}")

        # מערכת אצבעות / ציונים לשחקן
        if display_revenue == 0:
            st.error(f"🤮 **ציון: עגבנייה רקובה!** הסרט '{movie_name}' נחשב לאסון הקולנועי הגדול של העשור. הפסדת הכל.")
        elif net_profit < 0:
            st.warning(f"📉 **ציון: אולפן בחובות.** אומנם הכנסת ${display_revenue:,.0f}, אבל בגלל בזבוז כספים של ${game_budget:,.0f} סיימת בהפסדים. המנכ\"ל פיטר אותך.")
        elif net_profit < game_budget * 0.5:
            st.info(f"😐 **ציון: מפיק בינוני.** הסרט כיסה את ההוצאות והביא רווח קטן. המבקרים טוענים שמדובר במיחזור של ז'אנר ה-{genre}.")
        elif net_profit < game_budget * 2:
            st.success(f"⭐ **ציון: במאי מבטיח!** להיט קופתי אמיתי! הצלחת לנצל את {game_popularity} נקודות הפופולריות בצורה מעולה.")
        else:
            st.balloons()
            st.success(f"👑 **ציון: אגדה הוליוודית!** שברת את שיא הגינס של אווטאר! קיבלת 10 מתוך 10 בכל המגזינים והאולפן בונה לך פסל מזהב!")

        # מידע טכני מוסתר לשמירה על שקיפות המודל המקורי
        with st.expander("🛠️ נתוני המנוע המתמטי (מאחורי הקלעים):"):
            st.write(f"• פופולריות סופית שחושבה: {game_popularity} (סקיילד: {scaled_popularity})")
            st.write(f"• תקציב סופי שנכנס למודל: ${game_budget:,.0f}")
            st.write("• המשקולות המקוריות שלך יציבות ולא השתנו.")
