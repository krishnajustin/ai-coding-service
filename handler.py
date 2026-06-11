import runpod
import subprocess
import time
import os
import ollama

MODEL = 'qwen2.5-coder:32b'
os.environ['OLLAMA_MODELS'] = '/runpod-volume/ollama-models'

subprocess.Popen(['ollama', 'serve'])
time.sleep(3)
print('Ollama ready!')

def handler(job):
    inp = job['input']
    messages = inp.get('messages', [])
    max_tokens = inp.get('max_tokens', 4096)

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        options={'num_predict': max_tokens}
    )

    return {
        'id': 'chatcmpl-runpod',
        'object': 'chat.completion',
        'model': MODEL,
        'choices': [{
            'message': {
                'role': 'assistant',
                'content': response['message']['content']
            },
            'finish_reason': 'stop',
            'index': 0
        }]
    }

runpod.serverless.start({'handler': handler})