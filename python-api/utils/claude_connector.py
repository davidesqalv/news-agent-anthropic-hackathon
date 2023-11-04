import os

from anthropic import Anthropic, AsyncAnthropic


class ClaudeConnector:
    """Used for the LLM calls"""

    client = None
    async_client = None

    @classmethod
    def initialize(cls):
        ClaudeConnector.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        ClaudeConnector.async_client = AsyncAnthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    @classmethod
    def prompt_claude_sync(cls, prompt, max_tokens=2000):
        if not ClaudeConnector.client:
            ClaudeConnector.initialize()
        c = ClaudeConnector.client.completions.create(
            model="claude-2", max_tokens_to_sample=max_tokens, prompt=prompt
        )
        return c.completion

    @classmethod
    async def prompt_claude_async(cls, prompt, max_tokens=2000):
        if not ClaudeConnector.async_client:
            ClaudeConnector.initialize()
        c = await ClaudeConnector.async_client.completions.create(
            model="claude-2", max_tokens_to_sample=max_tokens, prompt=prompt
        )
        return c.completion

    @classmethod
    async def prompt_claude_async_stream(cls, prompt, max_tokens=2000):
        """Usage:
        stream = ClaudeConnector.prompt_claude_async_stream(f'{HUMAN_PROMPT} myprompt{AI_PROMPT}')
        async for completion in stream:
            print(completion.completion, end="", flush=True)
        """
        if not ClaudeConnector.async_client:
            ClaudeConnector.initialize()
        c = await ClaudeConnector.async_client.completions.create(
            model="claude-2",
            max_tokens_to_sample=max_tokens,
            prompt=prompt,
            stream=True,
        )
        return c.completion
