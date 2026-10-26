import streamlit as st
import base64
import os

# إعداد الصفحة لتكون بملء الشاشة وإخفاء القوائم
st.set_page_config(page_title="رحلة عمرنا", page_icon="✨", layout="centered")

# دمج CSS متقدم لعمل الأنيميشن (أوراق الشجر، الشجرة الخلفية) والتصميم الزجاجي والخطوط
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Amiri', serif;
        direction: rtl;
        text-align: center;
        background: linear-gradient(180deg, #071018, #162635, #22384a); /* خلفية ليلية رومانسية أعمق */
        color: #f8fafc;
        scroll-behavior: smooth;
    }
    
    /* إخفاء علامات Streamlit العلوية والسفلية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* الشجرة العملاقة في الخلفية */
    .bg-tree {
        position: fixed;
        bottom: -5vh;
        left: 50%;
        transform: translateX(-50%);
        font-size: 75vh;
        opacity: 0.12; /* شفافة لعدم التشويش على الكلام */
        z-index: 0;
        pointer-events: none;
        filter: drop-shadow(0 0 30px rgba(254, 202, 87, 0.3));
    }

    /* أنيميشن أوراق الشجر المتساقطة مع تمايل يمين ويسار */
    .leaf {
        position: fixed;
        top: -10vh;
        font-size: 32px;
        user-select: none;
        pointer-events: none;
        z-index: 1;
        animation: fall linear infinite, sway 3s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.2));
    }
    @keyframes fall {
        0% { top: -10vh; opacity: 1; }
        100% { top: 110vh; opacity: 0; }
    }
    @keyframes sway {
        0% { transform: translateX(-30px) rotate(0deg); }
        100% { transform: translateX(30px) rotate(60deg); }
    }
    
    /* تصميم الكروت الزجاجية (Glassmorphism) المطور */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(254, 202, 87, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 25px;
        padding: 45px 35px;
        margin: 40px auto;
        max-width: 750px;
        z-index: 10;
        position: relative;
        transition: all 0.5s ease;
    }
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 45px rgba(254, 202, 87, 0.25);
        border: 1px solid rgba(254, 202, 87, 0.6);
    }
    
    /* خطوط العناوين والقصائد */
    .year-title {
        font-family: 'Aref Ruqaa', serif;
        color: #feca57; /* لون ذهبي */
        font-size: 42px;
        margin-bottom: 25px;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.8);
    }
    
    .poem-text {
        font-size: 28px;
        line-height: 2.2;
        color: #f1f2f6;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
    }
    
    /* تخصيص الزر */
    div.stButton > button {
        width: 100%;
        border-radius: 50px !important;
        border: 2px solid #feca57 !important;
        background: rgba(254, 202, 87, 0.1) !important;
        color: #feca57 !important;
        font-size: 30px !important;
        font-family: "Aref Ruqaa" !important;
        padding: 15px !important;
        transition: 0.4s !important;
        box-shadow: 0 0 15px rgba(254, 202, 87, 0.2) !important;
    }
    div.stButton > button:hover {
        background: #feca57 !important;
        color: #071018 !important;
        box-shadow: 0 0 35px rgba(254, 202, 87, 0.6) !important;
        transform: scale(1.05);
    }
</style>

<!-- الشجرة العملاقة في الخلفية -->
<div class="bg-tree">🌳</div>

<!-- توليد الأوراق المتساقطة في الخلفية بسرعات وأماكن مختلفة -->
<div class="leaf" style="left: 15%; animation-duration: 14s; animation-delay: 0s;">🍂</div>
<div class="leaf" style="left: 25%; animation-duration: 17s; animation-delay: 3s;">🍁</div>
<div class="leaf" style="left: 35%; animation-duration: 12s; animation-delay: 1s;">🍃</div>
<div class="leaf" style="left: 50%; animation-duration: 19s; animation-delay: 5s;">🍂</div>
<div class="leaf" style="left: 65%; animation-duration: 15s; animation-delay: 2s;">🍁</div>
<div class="leaf" style="left: 75%; animation-duration: 18s; animation-delay: 4s;">🍃</div>
<div class="leaf" style="left: 85%; animation-duration: 13s; animation-delay: 6s;">🍂</div>
<div class="leaf" style="left: 92%; animation-duration: 16s; animation-delay: 1s;">🍁</div>
''', unsafe_allow_html=True)

# إدارة حالة التطبيق
if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    # شاشة البداية (بوابة الدخول)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: \"Aref Ruqaa\", serif; color: #feca57; font-size: 70px; text-shadow: 0 0 25px rgba(254,202,87,0.5); margin-bottom: 30px;'>رحلة عمركِ 🍂</h1>", unsafe_allow_html=True)
    
    # الجملة المضافة حديثاً
    st.markdown('''
    <div style="background: rgba(0, 0, 0, 0.4); padding: 40px; border-radius: 20px; margin: 0 auto 40px auto; max-width: 650px; border: 1px solid rgba(254,202,87,0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <h3 style='color: #e0e0e0; line-height: 2; font-weight: normal; font-size: 28px; font-family: "Amiri", serif;'>
            أنتي قولتي أنا معنديش سنة مميزة كلها..<br><br>
            <span style='color: #feca57; font-size: 34px; font-weight: bold;'>بس أنا دورت وعرفت إن كل سنة ليكي كانت أحلى سنة ❤️</span>
        </h3>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("اضغطي لتبدأي الرحلة ✨"):
            st.session_state.started = True
            st.rerun()
else:
    # المشهد الثاني: تشغيل الموسيقى تلقائياً وتكرارها
    audio_played = False
    if os.path.exists("music.mp3"):
        try:
            with open("music.mp3", "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            # كود HTML لتشغيل الصوت تلقائياً (autoplay) وتكراره (loop)
            st.markdown(f'<audio autoplay loop><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
            audio_played = True
        except Exception as e:
            pass
            
    if not audio_played:
        st.warning("⚠️ ملحوظة: ملف الموسيقى (music.mp3) غير موجود ليعمل في الخلفية.")

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # قائمة الرسائل الـ 23
    messages = [
        ("العام الأول", "ميلادُ النورِ في عينيكِ، فجرٌ أشرقَ في الدنيا ليضيءَ أيامي الآتية."),
        ("العام الثاني", "خطوتكِ الأولى على الأرض، زرعت في الكونِ ياسمينًا لا يذبل."),
        ("العام الثالث", "ضحكتكِ الطفولية، أولُ أغنيةٍ عرفتها العصافير وحفظتها عن ظهر قلب."),
        ("العام الرابع", "تعلّمَ الوردُ في هذا العام كيف يستمدُّ لونه من حُمرةِ وجنتيكِ."),
        ("العام الخامس", "براءةٌ تسكنُ ملامحكِ، جعلتِ الملائكةَ تحرسُ أحلامكِ الرقيقة."),
        ("العام السادس", "كبرتِ قليلًا، وصار للشمسِ منافسٌ حقيقيٌ في الإشراق والدفء."),
        ("العام السابع", "سبعُ سماواتٍ من الرقةِ تجمّعت واستقرت في قلبكِ الصغير."),
        ("العام الثامن", "كفراشةٍ تلوّنُ الحياة، بدأ سحركِ ينبضُ ويزهر في كل الأرجاء."),
        ("العام التاسع", "تسعةُ أقمارٍ تدورُ حولكِ، تستمدُّ من بهائكِ الضياء والسحر."),
        ("العام العاشر", "أولُ عقدٍ من الزمان، اكتملت فيه لوحةُ طفولتكِ البهية كقطعةِ سكر."),
        ("العام الحادي عشر", "بدايةُ الصِبا، كغصنِ بانٍ يتمايلُ بخفةٍ مع نسيمِ الصباح."),
        ("العام الثاني عشر", "كبرتِ وكبرَ الحلا، وصار وجهكِ قصيدةً تتغنى بها الأيام."),
        ("العام الثالث عشر", "قمرٌ يتململُ في كبد السماء، يغارُ من فتاةٍ تزدادُ حسنًا كل يوم."),
        ("العام الرابع عشر", "ربيعٌ دائمٌ يسكنُ أنفاسكِ، وتزهرُ الأرضُ أينما حلّت خطاكِ."),
        ("العام الخامس عشر", "نصفُ قمرٍ، ونصفُ شمسٍ، وجمالٌ حائرٌ لا يُقاسُ بالكلمات."),
        ("العام السادس عشر", "رقةٌ ودلال، كأنكِ خُلقتِ من قطراتِ الندى وماءِ الورد."),
        ("العام السابع عشر", "أنوثةٌ تتفتحُ كزهرةِ أوركيد، نادرة، ساحرة، وتخطف الأنفاس."),
        ("العام الثامن عشر", "اكتملَ البدرُ، وصارت الصبيةُ سيدةً تسرقُ الألباب وتأسر الروح."),
        ("العام التاسع عشر", "في عينيكِ بحرٌ من الشغف، وفي ابتسامتكِ وطنٌ ألجأ إليه."),
        ("العام العشرون", "عقدانِ من السحرِ، كلُّ عامٍ فيكِ كان أجملُ من ألفِ عامٍ مما يعُدّون."),
        ("العام الحادي والعشرون", "تتوّجتِ أميرةً على عرشِ قلبي، سيدةً لكل تفاصيلي وأيامي."),
        ("العام الثاني والعشرون", "نضجٌ ورقة، عقلٌ يزنُ الدنيا، وقلبٌ حنون يسعُ الكون بأسره."),
        ("العام الثالث والعشرون", "هنا والآن، أنتِ أجملُ ما في العمرِ، وكلُّ سنيني لكِ فداءٌ وحب.")
    ]
    
    # عرض البطاقات بأسلوب سحري
    for idx, (year, text) in enumerate(messages):
        st.markdown(f'''
        <div class="glass-card">
            <div class="year-title">🍂 {year}</div>
            <div class="poem-text">{text}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # مسافة بين كل كارت والتاني عشان التمرير
        if idx < len(messages) - 1:
            st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
            
    # الخاتمة
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    st.markdown('''
    <div style="background: rgba(254, 202, 87, 0.15); border: 2px solid #feca57; border-radius: 25px; padding: 70px 30px; text-align: center; box-shadow: 0 0 50px rgba(254, 202, 87, 0.5); margin-bottom: 150px; backdrop-filter: blur(15px);">
        <h1 style="font-family: 'Aref Ruqaa', serif; color: #feca57; font-size: 60px; margin-bottom: 30px; text-shadow: 0 0 20px #feca57;">🌸 كل عام وأنتِ ملكتي 🌸</h1>
        <h3 style="color: #fff; line-height: 2.2; font-weight: normal; font-size: 30px; text-shadow: 1px 1px 4px #000;">كل سنة وأنتي أجمل وأغلى حاجة في حياتي.<br>العمر كله وإحنا سوا يا روح قلبي.</h3>
    </div>
    ''', unsafe_allow_html=True)
