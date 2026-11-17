import streamlit as st
import random

st.set_page_config(page_title="تجارب الذكاء الاصطناعي", page_icon="🤖")
st.markdown("<style>.stApp {direction: rtl; text-align: right;}</style>", unsafe_allow_html=True)
st.title("🤖 تجارب الذكاء الاصطناعي")

tab1, tab2 = st.tabs(["1) الهلوسة", "2) التوليد المعزّز بالاسترجاع (RAG)"])

# ---------- التجربة 1: النموذج يتوقع الكلمة الجاية ----------
with tab1:
    st.subheader("النموذج يكتب بتوقع الكلمة الجاية")

    # البيانات: جمل تعلّم منها النموذج
    sentences = [
        "الزيارة يوم الخميس",
        "الزيارة تبدأ الساعة عشرة",
        "الدوام يبدأ الساعة ثمانية",
        "الطلب تم استلامه",
        "الطلب تحت المراجعة",
    ]
    st.write("**البيانات اللي تعلّم منها:**")
    for s in sentences:
        st.write("•", s)

    # التدريب: نحفظ وش الكلمة اللي تجي بعد كل كلمة
    next_words = {}
    for s in sentences:
        words = s.split()
        for i in range(len(words) - 1):
            next_words.setdefault(words[i], []).append(words[i + 1])

    start = st.selectbox("كلمة البداية", ["الزيارة", "الدوام", "الطلب"])

    if st.button("✍️ خلّه يكتب 10 جمل"):
        for n in range(10):
            word = start
            text = [word]
            for _ in range(3):
                if word not in next_words:
                    break
                word = random.choice(next_words[word])
                text.append(word)
            sentence = " ".join(text)
            if sentence in sentences:
                st.success("✔ " + sentence)
            else:
                st.error("❌ " + sentence + "  (هلوسة: جملة ما كانت في البيانات)")

# ---------- التجربة 2: RAG ----------
with tab2:
    st.subheader("يبحث في الدليل، وبعدين يجاوب")

    # الوثيقة: دليل مقسوم لمقاطع
    guide = [
        "الزيارة يوم الخميس وتبدأ الساعة عشرة صباحاً",
        "الإجازة السنوية مدتها ثلاثون يوماً",
        "الإجازة الاضطرارية مدتها خمسة أيام",
        "الدوام يبدأ الساعة ثمانية صباحاً",
    ]

    question = st.text_input("اكتب سؤالك", "كم مدة الإجازة الاضطرارية")

    if st.button("🔍 ابحث وجاوب"):
        # 1) الاسترجاع: نعدّ الكلمات المشتركة بين السؤال وكل مقطع
        q = set(question.split())
        best, best_score = "", 0
        st.write("**الخطوة 1: الاسترجاع** (عدد الكلمات المشتركة)")
        for part in guide:
            score = len(q & set(part.split()))
            st.write(f"{score} ← {part}")
            if score > best_score:
                best, best_score = part, score

        # 2) التوليد: نكتب الجواب من المقطع
        st.write("**الخطوة 2: التوليد**")
        if best:
            st.info("حسب الدليل: " + best)
        else:
            st.warning("ما لقيت المعلومة في الدليل")