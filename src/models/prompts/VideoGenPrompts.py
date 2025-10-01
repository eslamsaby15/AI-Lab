from enum import Enum
from langchain.prompts import PromptTemplate

class VideoScriptTemplate(Enum):
    AR = PromptTemplate(
    input_variables=["topic", "style", "total_minutes", "intro_words", "main_words", "conclusion_words"],
        template="""
        اكتب سكريبت فيديو عن: {topic}
        الأسلوب: {style}
        المدة: {total_minutes} دقائق
        عدد الكلمات المقترح: المقدمة {intro_words} كلمة، المحتوى الرئيسي {main_words} كلمة، الخاتمة {conclusion_words} كلمة

        اكتب بهذا الشكل:

        [مقدمة]
        الراوي: [ابدأ بسؤال جذاب]
        المشاهد: [ماذا نعرض]
        النص: [الأفكار الرئيسية]

        [محتوى رئيسي]
        الراوي: [النقطة الأولى. أنهي بربط مع التالي]
        المشاهد: [ماذا نعرض]
        النص: [النقطة الأساسية]

        الراوي: [النقطة التالية. ابدأ بالربط مع السابق. أنهي بربط مع التالي]
        المشاهد: [ماذا نعرض]
        النص: [النقطة الأساسية]

        [أضف فقرات حسب الحاجة لتصل إلى حوالي {total_minutes} دقائق.]

        الراوي: [آخر فقرة: ابدأ بـ "إذن" أو "كما رأينا". لخص جميع النقاط السابقة. لا تضيف مواضيع أو أفكار جديدة]
        المشاهد: [ماذا نعرض]

        [خاتمة]
        الراوي: [اختتم الفيديو]
        المشاهد: [ماذا نعرض]
        النص: [الرسالة النهائية]

        القواعد:
        ١. استخدم كلمات بسيطة
        ٢. ربط كل فكرة بالتالية
        ٣. اكتب فقرات كافية لملء الوقت المطلوب
        ٤. آخر فقرة رئيسية يجب أن: تبدأ بـ "إذن" أو "كما رأينا"، تختصر كل النقاط السابقة، لا تضيف مواضيع جديدة
        ٥. لا تضع سطر "النص" في آخر فقرة رئيسية
        """
    )
    EN =PromptTemplate(
    input_variables=["topic", "style", "total_minutes" ,"intro_words" , 'main_words' , "conclusion_words"],
    template=
            """
    Make a video script about: {topic}
    Style: {style}
    Time: {total_minutes} minutes
    Target word counts: Intro ~{intro_words}, Main ~{main_words}, Conclusion ~{conclusion_words}


    Write like this:

    [INTRO]
    NARRATOR: [Start with a question]
    VISUALS: [What to show]
    TEXT: [Main ideas]

    [MAIN]
    NARRATOR: [First point. End with connection to next]
    VISUALS: [What to show]
    TEXT: [Key point]

    NARRATOR: [Next point. Start with connection to previous. End with connection to next]
    VISUALS: [What to show]
    TEXT: [Key point]

    NARRATOR: [Next point. Start with connection to previous. End with connection to next]
    VISUALS: [What to show]
    TEXT: [Key point]

    [Add more paragraphs as needed until you reach about {total_minutes} minutes.]

    NARRATOR: [LAST PARAGRAPH: Start with "So" or "As we've seen". SUMMARIZE ALL PREVIOUS POINTS. DO NOT add new topics or ideas]
    VISUALS: [What to show]

    [CONCLUSION]
    NARRATOR: [End the video]
    VISUALS: [What to show]
    TEXT: [Final message]

    RULES:
    1. Use simple words
    2. Connect each idea to the next
    3. Write enough paragraphs to fill the time
    4. LAST MAIN PARAGRAPH MUST: Start with "So" or "As we've seen", Summarize all previous points, NO new topics
    5. No TEXT line in last main paragraph
    """
    )