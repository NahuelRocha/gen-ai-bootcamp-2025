import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import asyncio

import torch

class LLMService:
    def __init__(self):
        # Usar un modelo más pequeño para CPU
        model_id = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF" # Puedes ajustar según tu hardware
        
        # Cargar el modelo y tokenizador usando CTransformers (optimizado para CPU)
        from langchain.llms import CTransformers
        
        self.llm = CTransformers(
            model=model_id,
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            model_type="mistral",
            config={
                'max_new_tokens': 1024,
                'context_length': 1024,
                'temperature': 0.2,
                'threads': 6,  
                'batch_size': 1
            }
        )
    
    async def generate_dialog(self, language, difficulty, scenario=None):
        # Crear plantilla de prompt para generar diálogos
        prompt_template = PromptTemplate(
            input_variables=["language", "difficulty", "scenario"],
            template="""
            Create a realistic dialogue in English for listening comprehension practice.
            The dialogue should be between two people discussing a scenario.
            The difficulty level is: {difficulty}.
            Scenario: {scenario}

            Please generate a dialogue with at least 4 turns (each person speaks at least twice) and enough detail so that, when read aloud, it lasts approximately 30 seconds.

            Response format:
            Title: [Dialogue Title].
            Description: [Brief description of the scenario]
            Dialogue:
            [Person 1]: [Text]
            [Person 2]: [Text]
            [Person 1]: [Text]
            [Person 2]: [Text]
            ... (more lines if needed)
            """
        )
        
        # Crear cadena de LLM
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        # Ejecutar la cadena
        scenario_text = scenario if scenario else "An everyday scenario."
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,  # Usa el executor por defecto (thread pool)
            lambda: chain.run(
                language=language, 
                difficulty=difficulty, 
                scenario=scenario_text
            )
        )
        print("Raw output from LLM (generate_dialog):", result)
        # Procesar el resultado para extraer título, descripción y diálogo
        try:
            lines = result.strip().split("\n")
            title = lines[0].replace("Title:", "").strip()
            description = lines[1].replace("Description:", "").strip()
            dialog_marker = "Dialogue:"
            dialog_start = result.find(dialog_marker)
            dialog = result[dialog_start + len(dialog_marker):].strip() if dialog_start != -1 else ""
            return {
                "title": title,
                "description": description,
                "dialog": dialog
            }
        except Exception as e:
            return {
                "title": "Generated Dialogue",
                "description": "Scenario description",
                "dialog": result
            }
    
    async def generate_questions(self, dialog, language, num_questions=3):
        # Crear plantilla de prompt para generar preguntas
        prompt_template = PromptTemplate(
            input_variables=["dialog", "language", "num_questions"],
            template="""
            Based on the following dialogue in {language}:

            {dialog}

            Generate {num_questions} multiple-choice comprehension questions (4 choices per question, only one correct answer).

            Response format:
            [
            {{
                "question": "Question 1",
                "options": [
                {{ "text": "Option 1", "correct": true}},
                {{ "text": "Option 2", "correct": false}},
                {{ "text": "Option 3", "correct": false}},
                {{ "text": "Option 4", "correct": false}}
                ]
            }},
            ...
            ]

            Ensure the questions test understanding of the content, not just superficial details.
            """
        )
        
        # Crear cadena de LLM
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        # Ejecutar la cadena
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: chain.run(
                dialog=dialog,
                language=language,
                num_questions=num_questions
            )
        )
        
        # Procesar el resultado para obtener las preguntas y opciones en formato JSON
        import json
        try:
            # Extraer solo la parte que contiene el JSON
            json_start = result.find("[")
            json_end = result.rfind("]") + 1
            json_str = result[json_start:json_end]
            
            # Analizar el JSON
            questions_data = json.loads(json_str)
            
            # Procesar cada pregunta para el formato requerido por la base de datos
            questions = []
            for q_data in questions_data:
                question = {
                    "question_text": q_data["question"],
                    "options": []
                }
                
                for opt in q_data["options"]:
                    question["options"].append({
                        "option_text": opt["text"],
                        "is_correct": 1 if opt["correct"] else 0
                    })
                
                questions.append(question)
            
            return questions
        except Exception as e:
            # En caso de error, devolver un formato básico de preguntas
            return [
                {
                    "question_text": "What is the main topic of this dialogue?",
                    "options": [
                        {"option_text": "Automatically generated option 1", "is_correct": 1},
                        {"option_text": "Automatically generated option 2", "is_correct": 0},
                        {"option_text": "Automatically generated option 3", "is_correct": 0},
                        {"option_text": "Automatically generated option 4", "is_correct": 0}
                    ]
                }
            ]