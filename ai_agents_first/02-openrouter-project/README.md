#  OpenRouter

Yeh project OpenRouter ka use karke multiple AI models ko test karne ke liye banaya gaya hai. Is mein hum ne OpenAI jaisa API use kiya hai jo OpenRouter ke through 50+ free models ko access karta hai.

## ✨ Features

- Use karo 50+ AI models (ChatGPT, Claude, Mistral, etc.)
- Sirf ek API endpoint se kaam
- OpenAI Chat Completion API jaisa syntax
- Google Gemini aur OpenRouter dono support
- Function calling aur tool integration ka option

## 🔑 Requirements

- Python 3.9+
- `requests` library (install karne ke liye `pip install requests`)
- OpenRouter API key (https://openrouter.ai)

## 🧪 Example Code

```python
import requests

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY_HERE",
    "Content-Type": "application/json"
}
data = {
    "model": "openchat-3.5:free",
    "messages": [
        {"role": "user", "content": "Assalamualaikum, aap kaun hain?"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```
###Rate Limits (Free Models)
200 requests per day

20 requests per minute

Models ending with :free are free to use

###
🙋‍♀️ Author
Made with ❤️ by Bisma Arshad

