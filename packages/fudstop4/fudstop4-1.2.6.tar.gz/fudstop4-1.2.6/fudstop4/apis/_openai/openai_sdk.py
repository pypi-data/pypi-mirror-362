import sys
from pathlib import Path
import base64
# Add the project directory to the sys.path
from fudstop4.apis.polygonio.polygon_options import PolygonOptions
opts = PolygonOptions()
import requests
project_dir = str(Path(__file__).resolve().parents[1])
import os
from dotenv import load_dotenv
load_dotenv()
import time
import json
from openai import OpenAI
import pandas as pd
from fudstop4.apis.polygonio.polygon_options import PolygonOptions
import asyncpg
import datetime
import aiohttp
from .tools_shcema import tools, serialize_record
class OpenAISDK:
    def __init__(self):
        

        self.client = OpenAI(api_key=os.environ.get('YOUR_OPENAI_KEY'))
        self.pool = None
        self.opts = PolygonOptions(database='fudstop3')

    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def init_db(self):
        self.pool = await asyncpg.create_pool(dsn=os.environ.get('OPENAI_STRING'))

    async def save_message(self, chat_id, message_type, content):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                INSERT INTO messages(chat_id, message_type, content)
                VALUES($1, $2, $3)
            ''', chat_id, message_type, content)

    async def get_conversation_history(self, chat_id):
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('''
                SELECT content FROM messages WHERE chat_id = $1 ORDER BY timestamp ASC
            ''', chat_id)

        return [row['content'] for row in rows]

    async def communicate(self, prompt, model: str = 'o1'):
        # Connect to the database (if not already connected)
        await opts.connect()

        # Load conversation history from long-term storage (database)
        message_history = await self.load_message_history()

        # Append the current user prompt
        message_history.append({'role': 'user', 'content': prompt})

        # Call the API using the full conversation history for context
        response = self.client.chat.completions.create(
            model=model,
            messages=message_history,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_response = response.choices[0].message.content

        # Append the AI's response to the conversation history
        message_history.append({'role': 'assistant', 'content': ai_response})

        # Save the updated conversation history back to the database
        await self.save_message_history(message_history)

        return ai_response

    async def load_message_history(self):
        """
        Load conversation history from the database using the custom opts class.
        Assumes a table 'conversation_history' exists with columns:
        message_index, role, content, and timestamp.
        """
        table_name = "conversation_history"
        # Retrieve messages ordered by message_index to preserve conversation order
        query = f"SELECT role, content FROM {table_name} ORDER BY message_index ASC"
        results = await opts.fetch(query)
        
        # Convert query results into the expected list of dictionaries
        message_history = [{"role": row[0], "content": row[1]} for row in results]
        return message_history

    async def save_message_history(self, history):
        """
        Save (or upsert) the entire conversation history to the database.
        Converts the history to a DataFrame and uses opts.batch_upsert_dataframe.
        """
        data = []
        for idx, message in enumerate(history):
            data.append({
                "message_index": idx,
                "role": message["role"],
                "content": message["content"],
                "timestamp": datetime.datetime.utcnow().isoformat()  # Store timestamp in ISO format
            })
        df = pd.DataFrame(data)
        table_name = "conversation_history"
        unique_columns = ["message_index"]  # Use message_index as the unique identifier
        await opts.batch_upsert_dataframe(df, table_name=table_name, unique_columns=unique_columns)

    async def vision(self, prompt, image_url):


        response = self.client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{prompt}? Read the image to the best of your ability. Listen to the user request."},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

        return response.choices[0].message.content
    



    async def multi_image(self, prompt, image_urls):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}",
                    },
                ],
            }
        ]

        for image_url in image_urls:
            image_message = {
                "type": "image_url",
                "image_url": {
                    "url": f"{image_url}",
                },
            }
            messages[0]["content"].append(image_message)

        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content
    
    async def list_files(self):
        files = self.client.files.list()
        
        data = files.data

        ids = [i.id for i in data]
        purposes = [i.purpose for i in data]
        bytes = [i.bytes for i in data]
        names = [i.filename for i in data]
        data_dict = { 
            'id': ids,
            'name': names,
            'purpose': purposes,
            'bytes': bytes
        }
        df = pd.DataFrame(data_dict)

        return df

    async def upload_files(self, filename):


        self.client.files.create(
        file=open(f"{filename}", "rb"),
        purpose="assistants"
        )



    async def retrieve_file_content(self, filename):
        data = self.client.files.retrieve(filename)
        
        return data
    

        
        
   

    async def run_conversation(self,query):
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": f"{query} | | Be clear and concise in your response. Offer tabulated formatting when appropriate to the user. Be sure to include all dates in API responses. Convert all decimal percentages to %. Instead of writing 1,000,000 or 1,000,000,000,000 use 1 billion, 1 trillion, 1 million, etc. IF THE FUNCTION CALL IS FINANCIALS - DO NOT USE TABULATED FORMAT. EXPLAIN THE RESULTS TO THE USER USING VARIOUS METRICS."}]
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            tools=tools,
            max_tokens=750,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                'law': self.law


            }

            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                records = await function_to_call(**function_args)

                # Process each record for serialization
                processed_records = [serialize_record(record) for record in records]

                # Serialize the list of processed records
                serialized_response = json.dumps(processed_records)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": serialized_response,
                })

            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                max_tokens=1250
            )  # get a new response from the model where it can see the function response
            return second_response.choices[0].message.content
        


    async def embeddings(self):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))



        return client

        


