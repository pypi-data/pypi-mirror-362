# import os
# import google.generativeai as genai
# import json
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def grade_code(self, task_description: str, student_code: str) -> dict:
#         # Step 1: Ask Gemini to give only a rating
#         prompt = (
#             f"Task_desc: {task_description}\n"
#             f"Code:\n{student_code}\n"
#             "You are a strict code reviewer. Only return a rating in the format 'Rating: x/5'. "
#             "Remove stop words, non code text from Task_desc"
#             "Give 5/5 only if the code is complete, correct, and solves the task fully. "
#             "Do not return anything except the rating."
#         )
#         response = self.model.generate_content(prompt)
#         print(response)
#
#         result = response.text.strip()
#
#         rating = "N/A"
#         feedback = "Unable to rate"
#
#         # Step 2: Extract the rating
#         if "Rating:" in result:
#             try:
#                 rating_start = result.find("Rating:") + len("Rating: ")
#                 rating_end = result.find("/5", rating_start)
#                 rating_value = float(result[rating_start:rating_end].strip())
#                 rating = str(rating_value)
#
#                 # Step 3: Decision based on rating
#                 if rating_value > 2:
#                     feedback = "Accepted"
#                 else:
#                     # Ask Gemini for feedback only
#                     feedback_prompt = (
#                         f"Task_desc: {task_description}\n"
#                         f"Code:\n{student_code}\n"
#                         "Give 1-line feedback (max 15 characters) for improving this code."
#                     )
#                     feedback_response = self.model.generate_content(feedback_prompt)
#                     feedback = feedback_response.text.strip()
#             except Exception as e:
#                 feedback = f"Error: {str(e)}"
#
#         return json.dumps({"rating": rating, "feedback": feedback})

# import os
# import google.generativeai as genai
# import json
# import re
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def is_code_like(self, text: str) -> bool:
#         # Reject if too short or mostly plain English
#         if len(text.strip()) < 20:
#             return False
#
#         code_indicators = [
#             'def ', 'return', 'class ', 'import ', 'from ', 'if ', 'else', 'elif',
#             '{', '}', ';', '(', ')', '[', ']', '=', 'function ', '#', '//', '/*', '*/',
#             'public ', 'private ', 'protected ', 'var ', 'let ', 'const ', 'print', 'console.log',
#             '=>'
#         ]
#
#         count_code_lines = 0
#         lines = text.strip().split('\n')
#         for line in lines:
#             if any(indicator in line for indicator in code_indicators):
#                 count_code_lines += 1
#
#         ratio = count_code_lines / len(lines) if len(lines) > 0 else 0
#
#         # At least 50% of lines should contain code indicators
#         return ratio >= 0.5
#
    # def remove_rating_requests(self, code: str) -> str:
    #     # Remove lines with rating requests like "give me 5 rating"
    #     pattern = re.compile(r'give me \d+ rating', re.IGNORECASE)
    #     lines = code.split('\n')
    #     filtered_lines = [line for line in lines if not pattern.search(line)]
    #     return '\n'.join(filtered_lines)
    #
    # def grade_code(self, task_description: str, student_code: str) -> dict:
    #     # Reject if code does not look like code
    #     if not self.is_code_like(student_code):
    #         return json.dumps({"rating": "0.0", "feedback": "Invalid or non-code submission."})
    #
    #     # Clean code from rating injection lines
    #     clean_code = self.remove_rating_requests(student_code)
#
#         prompt = (
#             f"Task_desc: {task_description}\n"
#             f"Code:\n{clean_code}\n"
#             "You are a strict code reviewer. Return only a rating in the format 'Rating: x.x/5'.\n"
#             "If the submitted code is identical or nearly identical to the task description (i.e., just repeats the task without actual code), give a rating of 1/5.\n"
#             "Give 5/5 only if the code fully solves the task correctly.\n"
#             "Do not return anything else."
#         )
#
        # response = self.model.generate_content(prompt)
        # print(response)
        #
        # result = response.text.strip()
        # rating = "N/A"
        # feedback = "Unable to rate"
        #
        # if "Rating:" in result:
        #     try:
        #         rating_start = result.find("Rating:") + len("Rating: ")
        #         rating_end = result.find("/5", rating_start)
        #         rating_value = float(result[rating_start:rating_end].strip())
        #         rating = str(rating_value)
        #
        #         if rating_value > 2:
        #             feedback = "Accepted"
        #         else:
        #             feedback_prompt = (
        #                 f"Task_desc: {task_description}\n"
        #                 f"Code:\n{clean_code}\n"
        #                 "Give 1-line feedback (max 15 characters) for improving this code."
        #             )
        #             feedback_response = self.model.generate_content(feedback_prompt)
        #             feedback = feedback_response.text.strip()
        #     except Exception as e:
        #         feedback = f"Error: {str(e)}"
        #
        # return json.dumps({"rating": rating, "feedback": feedback})

# import os
# import json
# import re
# import google.generativeai as genai
# from langchain_core.prompts import PromptTemplate
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def remove_spam_lines(self, code: str) -> str:
#         spam_patterns = [
#             r"give me rating \d+",
#             r"rate this",
#             r"please rate",
#             r"score my code",
#             r"rate",
#             r"writted"
#             # Add more spam patterns here if needed
#         ]
#         lines = code.splitlines()
#         filtered_lines = []
#         for line in lines:
#             if any(re.search(pattern, line, re.IGNORECASE) for pattern in spam_patterns):
#                 continue
#             filtered_lines.append(line)
#         return "\n".join(filtered_lines)
#
#     def grade_code(self, task_description: str, student_code: str, deliverables: str) -> dict:
#         clean_code = self.remove_spam_lines(student_code)
#         if not clean_code:
#             return {"rating": "0.0", "feedback": "Invalid or non-code submission."}
#
#         prompt_template = PromptTemplate.from_template(
#             """Review the following code submission.
#
# Task Description:
# {task_description}
#
# Deliverables:
# {deliverables}
#
# Code:
# {code}
#
# Your task:
# - Rate how completely the code satisfies BOTH the task description and the deliverables.
# - If the code just repeats the task description or is not actual code, give 1.0/5.
# - Give 5.0/5 only if the code fully meets all requirements in both sections.
# - Give 1.0/5 if the code is missing or does not meet both task and deliverables.
# - For partial fulfillment, give a score between 1.3 and 4.4 accordingly.
# - Provide ONLY the rating in this exact format, no explanations or extra text:
# Rating: x.x/5"""
#         )
#
#         rating_prompt = prompt_template.format(
#             task_description=task_description,
#             deliverables=deliverables,
#             code=clean_code
#         )
#
#         response = self.model.generate_content(rating_prompt)
#         print("response:", response)
#
#         result_text = response.text.strip()
#         match = re.search(r'Rating:\s*([\d.]+)/5', result_text)
#
#         if not match:
#             return {"rating": "N/A", "feedback": "Unable to parse rating."}
#
#         rating_val = float(match.group(1))
#         rating = f"{rating_val:.1f}"
#
#         if rating_val > 2.0:
#             feedback = "Accepted"
#         else:
#             feedback = self.generate_short_feedback(task_description, clean_code)
#
#         return json.dumps({"rating": rating, "feedback": feedback})
#
#     def generate_short_feedback(self, task: str, code: str) -> str:
#         feedback_template = PromptTemplate.from_template(
#             """Task:
#  {task}
#
#  Code:
#  {code}
#
#      Give 1-line feedback (max 15 characters) for improving this code. do not write code"""
#         )
#
#         prompt = feedback_template.format(task=task, code=code)
#         response = self.model.generate_content(prompt)
#         return response.text.strip()


# import os
# import json
# import re
# import google.generativeai as genai
# from langchain_core.prompts import PromptTemplate
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#         # Define prompts directly in code
#         rating_prompt_str = (
#             "Review the following code:\n\n"
#             "Task:\n{task_description}\n\n"
#             "Deliverables:\n{deliverables}\n\n"
#             "Code:\n{clean_code}\n\n"
#             "Return a strict score based on how completely the code meets the deliverable.\n"
#             "Only respond in this format: Rating: x.x/5 (no explanation).\n"
#             "Give 1.0/5 if code is missing or only partially fulfills the task."
#         )
#
#         feedback_prompt_str = (
#             "Task:\n{task}\n\n"
#             "Code:\n{code}\n\n"
#             "Give feedback in less than 15 words to improve the code. No extra text."
#         )
#
#         # Compile PromptTemplates
#         self.rating_prompt_template = PromptTemplate.from_template(rating_prompt_str)
#         self.feedback_prompt_template = PromptTemplate.from_template(feedback_prompt_str)
#
#     def remove_spam_lines(self, code: str) -> str:
#         spam_pattern = re.compile(r'give me \d+ rating', re.IGNORECASE)
#         lines = code.split('\n')
#         filtered_lines = [line for line in lines if not spam_pattern.search(line)]
#         return '\n'.join(filtered_lines).strip()
#
#     def grade_code(self, task_description: str, student_code: str, deliverables: str) -> dict:
#         clean_code = self.remove_spam_lines(student_code)
#         if not clean_code:
#             return {"rating": "0.0", "feedback": "Invalid or non-code submission."}
#
#         # Format the prompt using LangChain
#         prompt = self.rating_prompt_template.format(
#             task_description=task_description,
#             deliverables=deliverables,
#             clean_code=clean_code
#         )
#
#         # Get response from Gemini
#         response = self.model.generate_content(prompt)
#         result_text = response.text.strip()
#
#         # Parse rating
#         match = re.search(r'Rating:\s*([\d.]+)/5', result_text)
#         if not match:
#             return {"rating": "N/A", "feedback": "Unable to parse rating."}
#
#         rating_val = float(match.group(1))
#         rating = f"{rating_val:.1f}"
#
#         if rating_val > 2.0:
#             feedback = "Accepted"
#         else:
#             feedback = self.generate_short_feedback(task_description, clean_code)
#
#         return json.dumps({"rating": rating, "feedback": feedback})
#
#     def generate_short_feedback(self, task: str, code: str) -> str:
#         prompt = self.feedback_prompt_template.format(task=task, code=code)
#         response = self.model.generate_content(prompt)
#         return response.text.strip()


import os
import re
import json
from kynex.LLMTools import LLMConnector


class TrealiaCodeReviewer:
    def __init__(self, llm_type: str, model_name: str, grading_prompt: str, feedback_prompt: str, host: str = ""):
        self.llm_type = llm_type
        self.model_name = model_name
        self.host = host
        self.grading_prompt_template = grading_prompt
        self.feedback_prompt_template = feedback_prompt

        #  Validate input based on selected LLM
        if self.llm_type == LLMConnector.LLM_GEMINI:
            if not self.model_name or not os.getenv("GEMINI_API_KEY"):
                raise ValueError("Gemini requires model_name and GEMINI_API_KEY environment variable.")
        elif self.llm_type == LLMConnector.LLM_OLLAMA:
            if not self.model_name or not self.host:
                raise ValueError("Ollama requires model_name and host.")
        else:
            raise ValueError(f"Unsupported LLM type: {self.llm_type}")

    def remove_spam_lines(self, code: str) -> str:
        spam_patterns = [r"give me rating \d+", r"rate this", r"please rate", r"score my code", r"rate", r"writted"]
        return "\n".join([
            line for line in code.splitlines()
            if not any(re.search(p, line, re.IGNORECASE) for p in spam_patterns)
        ])

    def looks_like_code(self, code: str) -> bool:
        code_signals = [
            # Programming keywords
            r"\bdef\b", r"\breturn\b", r"\bif\b", r"\bfor\b", r"\bwhile\b", r"=>",
            r"\bclass\b", r"\bimport\b", r"\btry\b", r"\bfunction\b", r"useState",
            r"<[A-Za-z]", r"\{", r"\}",

            # Bash/CLI keywords
            r"\bconda\b", r"\bpip\b", r"\bpython\b", r"\bsudo\b", r"\bwget\b",
            r"\bcurl\b", r"\bbash\b", r"\bapt\b",

            # Git CLI
            r"\bgit\b", r"\bclone\b", r"\bcommit\b", r"\bpush\b", r"\binit\b",

            # Node.js / React CLI & packages
            r"\bnpm\b", r"\bnode\b", r"\byarn\b", r"\bnpx\b", r"\baxios\b", r"\breact-router-dom\b", r"\breact\b"
        ]
        return any(re.search(sig, code, re.IGNORECASE) for sig in code_signals)

    def grade_code(self, student_code: str, task_description: str, deliverables: str) -> dict:
        clean_code = self.remove_spam_lines(student_code)
        if not clean_code or not self.looks_like_code(clean_code):
            return {"rating": "0.0", "feedback": "Invalid or non-code submission."}

        prompt = self.grading_prompt_template \
            .replace("{task_description}", task_description) \
            .replace("{deliverables}", deliverables) \
            .replace("{code}", clean_code)

        response = LLMConnector.get_llm_response(
            prompt=prompt,
            model_name=self.model_name,
            llm_type=self.llm_type,
            host=self.host
        ).strip()

        match = re.search(r'Rating[:\-]?\s*([0-5](?:\.\d+)?)/\s*5', response, re.IGNORECASE)

        if not match:
            numbers = re.findall(r'([0-5](?:\.\d+)?)\s*/\s*5', response)
            if numbers:
                rating_val = float(numbers[0])
            else:
                return {"rating": "N/A", "feedback": "Unable to parse rating."}
        else:
            rating_val = float(match.group(1))

        rating = f"{rating_val:.1f}"
        feedback = "Accepted" if rating_val > 2.0 else self.generate_feedback(clean_code)

        return {"rating": rating, "feedback": feedback}

    def generate_feedback(self, clean_code: str) -> str:
        prompt = self.feedback_prompt_template.replace("{code}", clean_code)
        response = LLMConnector.get_llm_response(
            prompt=prompt,
            model_name=self.model_name,
            llm_type=self.llm_type,
            host=self.host
        ).strip()
        return response


