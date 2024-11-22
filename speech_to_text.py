from openai import OpenAI
import json
import os
import subprocess
import tempfile
import datetime
from dotenv import load_dotenv

load_dotenv()

class SpeechToText:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.MAX_AUDIO_SIZE_BYTES = int(os.getenv('MAX_AUDIO_SIZE_BYTES', 20 * 1024 * 1024))
        self.GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-4')
        self.WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'whisper-1')

    def get_file_size(self, file_path):
        return os.path.getsize(file_path)

    def get_audio_duration(self, audio_file_path):
        result = subprocess.run(['ffprobe', '-i', audio_file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)

    def resize_audio_if_needed(self, audio_file_path):
        audio_size = self.get_file_size(audio_file_path)
        if audio_size > self.MAX_AUDIO_SIZE_BYTES:
            current_duration = self.get_audio_duration(audio_file_path)
            target_duration = current_duration * self.MAX_AUDIO_SIZE_BYTES / audio_size
            
            temp_dir = tempfile.mkdtemp()
            print(f"Compressed audio will be stored in {temp_dir}")
            
            compressed_audio_path = os.path.join(temp_dir, f'compressed_audio_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.wav')
            
            subprocess.run(['ffmpeg', '-i', audio_file_path, '-ss', '0', '-t', str(target_duration), compressed_audio_path])
            
            return compressed_audio_path
        return audio_file_path

    def transcribe_audio(self, audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcript = self.client.audio.translations.create(
                file=audio_file,
                model=self.WHISPER_MODEL,
            )
            print("Transcribe: Done")
            return transcript.text

    def abstract_summary_extraction(self, transcription):
        response = self.client.chat.completions.create(
            model=self.GPT_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        print("Summary: Done")
        return response.choices[0].message.content

    def key_points_extraction(self, transcription):
        response = self.client.chat.completions.create(
            model=self.GPT_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        print("Key Points: Done")
        return response.choices[0].message.content

    def action_item_extraction(self, transcription):
        response = self.client.chat.completions.create(
            model=self.GPT_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        print("Action Items: Done")
        return response.choices[0].message.content

    def sentiment_analysis(self, transcription):
        response = self.client.chat.completions.create(
            model=self.GPT_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        print("Sentiment: Done")
        return response.choices[0].message.content

    def meeting_minutes(self, transcription):
        abstract_summary = self.abstract_summary_extraction(transcription)
        key_points = self.key_points_extraction(transcription)
        action_items = self.action_item_extraction(transcription)
        sentiment = self.sentiment_analysis(transcription)
        return {
            'abstract_summary': abstract_summary,
            'key_points': key_points,
            'action_items': action_items,
            'sentiment': sentiment
        }

    def store_in_json_file(self, data):
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, f'meeting_data_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        print(f"JSON file path: {file_path}")
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print("JSON file created successfully.")

    def transcribe(self, audio_file_path):
        audio_file_path = self.resize_audio_if_needed(audio_file_path)
        transcription = self.transcribe_audio(audio_file_path)
        summary = self.meeting_minutes(transcription)
        self.store_in_json_file(summary)
    
        print(f"Abstract Summary: {summary['abstract_summary']}")
        print(f"Key Points: {summary['key_points']}")
        print(f"Action Items: {summary['action_items']}")
        print(f"Sentiment: {summary['sentiment']}")
