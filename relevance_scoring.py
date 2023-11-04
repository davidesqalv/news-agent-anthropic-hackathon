import re
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

key = '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'
anthropic_client = Anthropic(api_key=key)  # or put it in os.environ as ANTHROPIC_API_KEY

def prompt_claude(prompt, max_tokens=2000):
   c = anthropic_client.completions.create(model="claude-2",max_tokens_to_sample=max_tokens,prompt=prompt)
   return c.completion

test_article = "At least nine individuals were wounded in Russian attacks across Ukraine. The European Commission President visited Kyiv, the capital of Ukraine, to meet with President Volodymyr Zelenskyy amidst ongoing tensions​6​."


preferences = {
    "Interests": {
        "HighInterest": [
            "Functional developments in machine learning models",
            "Innovative research papers on AI and machine learning",
            "Progress between the Russia and Ukraine War",
            "Conflict between Israel and Gaza",
            "Development in the oil market",
            "Developments in China's economic situation",
            "Thoughtful books and quotes"
        ],
        "LowInterest": [
            "Partisan politics",
            "Pop culture"
        ]
    }
}

# Modify the prompt to request a specific response format for scoring relevance
Score_Relevance_prompt = (
    
f"{HUMAN_PROMPT} <preferences>{preferences}</preferences> <article>{test_article}</article>\n"
    f"<Instructions> Score the relevance of the article based on the provided interests. "
    f"Return only a single digit between 1 and 10. Do not provide any other text or explanation.</Instructions>\n"
    f"{AI_PROMPT}{{"
)
Score_Relevance = prompt_claude(Score_Relevance_prompt)
score = re.findall(r'\d+', Score_Relevance)


# Modify the prompt to request a specific response format for creating a headline
Create_Headline_prompt = (
    f"{HUMAN_PROMPT} <article>{test_article}</article>\n"
    f"<Instructions>Please create a short headline for the provided article. "
    f"Provide the headline as a single sentence.</Instructions>\n"
    f"{AI_PROMPT}{{"
)
Create_Headline = prompt_claude(Create_Headline_prompt)

combined = {
    "Create_Headline": Create_Headline,
    "Score_Relevance": score
}

# Optionally convert to JSON and print or write to file
import json
json_string = json.dumps(combined, indent=4)
print(json_string)
