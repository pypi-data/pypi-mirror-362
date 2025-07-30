import openai
def get_ai_script(prompt):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    res = openai.ChatCompletion.create(model='gpt-4', messages=[{'role': 'user', 'content': prompt}])
    return res.choices[0].message.content
