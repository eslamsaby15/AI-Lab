from .BaseController import BaseController
from langchain.prompts import PromptTemplate
import re

class MiniQuizController(BaseController):
    def __init__(self, provider, num_questions: int = 10):
        super().__init__()
        self.provider = provider
        self.num_questions = num_questions
        self.prompt_template = PromptTemplate(
                input_variables=["text", "num_questions"],
                template="""
            Generate EXACTLY {num_questions} multiple-choice questions from the text below.
            Use this exact format for each question:

            [QUESTION]
            NARRATOR: Question text here
            OPTIONS: A) Option A text | B) Option B text | C) Option C text
            ANSWER: A

            [QUESTION]
            NARRATOR: Another question text here
            OPTIONS: A) First option | B) Second option | C) Third option
            ANSWER: B

            Continue with exactly {num_questions} questions in total.

            Text:
            {text}

            Rules:
            1. Generate EXACTLY {num_questions} questions - no more, no less
            2. Each question must have exactly 3 options (A, B, C)
            3. Use | to separate options
            4. ANSWER must be A, B, or C
            5. Keep questions clear and concise
            6. All questions must be based on the provided text
            """
            )

    def generate_quiz(self, text: str):
        questions = []
        
        prompt = self.prompt_template.format(text=text, num_questions=self.num_questions)
        output = self.provider.generate_Chunks(prompt=prompt, temperature=0.3)
        
        questions.extend(self.script_to_json(output))
        
        return questions
    
    def script_to_json(self, raw_script: str):
        questions = []
        raw_questions = re.split(r'\[QUESTION\]', raw_script)
        
        for q in raw_questions:
            q = q.strip()
            if not q:
                continue
            
            narrator_match = re.search(r'NARRATOR:\s*(.+?)(?=\n|$)', q)
            question_text = narrator_match.group(1).strip() if narrator_match else ""
            
            options_match = re.search(r'OPTIONS:\s*(.+?)(?=\n|$)', q)
            options = []
            if options_match:
                opts_text = options_match.group(1).strip()
                opts_list = opts_text.split('|')
                for opt in opts_list:
                    opt = opt.strip()
                    opt = re.sub(r'^[A-C]\)\s*', '', opt)
                    options.append(opt)
            
            answer_match = re.search(r'ANSWER:\s*([A-C])', q)
            answer = answer_match.group(1) if answer_match else ""
            
            if question_text and len(options) == 3 and answer:
                questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": answer
                })
        
        return questions