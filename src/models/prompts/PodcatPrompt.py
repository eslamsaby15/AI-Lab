from enum import Enum
from langchain.prompts import PromptTemplate

class PodCastPromptEnum(Enum):
    AR = PromptTemplate(
            input_variables=["topic", "style", "total_minutes", "intro_words", "main_words", "conclusion_words"],
            template="""
            أنشئ محادثة بودكاست عن: {topic}
            الأسلوب: {style}
            المدة: {total_minutes} دقائق
            عدد الكلمات المستهدف: المقدمة ~{intro_words}، المحتوى الرئيسي ~{main_words}، الخاتمة ~{conclusion_words}

            اكتب بهذا الشكل بالضبط:

            [INTRO]
            [host]: رسالة ترحيب
            [speaker_a]: رد

            [Q&A SESSION]
            [host]: السؤال الأول
            [speaker_a]: الإجابة
            [host]: [تعليق قصير على الإجابة] [السؤال التالي]
            [speaker_a]: الإجابة

            [أضف المزيد من الأسئلة والإجابات حسب الحاجة حتى تصل إلى حوالي {main_words} دقيقة.]
            
            [host]: [تعليق قصير على الإجابة] [السؤال التالي]
            [speaker_a]: الإجابة

            [OUTRO]
            [host]: رسالة شكر
            [speaker_a]: وداع

            القواعد:
            1. كل سطر للمضيف يجب أن يحتوي: تعليق قصير (جملة واحدة) + سؤال
            2. التعليق يجب أن يشير إلى إجابة speaker_a السابقة
            3. حافظ على التعليقات موجزة وطبيعية
            4. احترم عدد الكلمات المستهدف لكل قسم
          
            """
        )
    EN =PromptTemplate(
            input_variables=["topic", "style", "total_minutes", "intro_words", "main_words", "conclusion_words"],
            template="""
            Create a podcast conversation about: {topic}
            Style: {style}
            Duration: {total_minutes} minutes
            Target word counts: Intro ~{intro_words}, Main ~{main_words}, Outro ~{conclusion_words}

            Write in this exact format:

            [INTRO]
            [host]: Welcome message
            [speaker_a]: Response

            [Q&A SESSION]
            [host]: First question
            [speaker_a]: Answer
            [host]: [SHORT COMMENT on the answer] [NEXT QUESTION]
            [speaker_a]: Answer

            [Add more Q|A as needed until you reach about {main_words} minutes.]
            
            [host]: [SHORT COMMENT on the answer] [NEXT QUESTION]
            [speaker_a]: Answer

            [OUTRO]
            [host]: Thank you message
            [speaker_a]: Goodbye

            RULES:
            1. Each host line must have: SHORT COMMENT (1 sentence) + QUESTION
            2. Comment must reference the previous speaker_a answer
            3. Keep comments brief and natural.
            4. Respect the target word counts for each section
           
            """
        )