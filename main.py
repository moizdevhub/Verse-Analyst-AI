from agents import Agent, Runner, trace
from connection import config
import asyncio                           
from dotenv import load_dotenv

load_dotenv()

poet_agent = Agent(
    name = "poet agent",
    instructions="""
You are a Poet Agent.

Your job is to either:
1. Generate a short 2-stanza poem (each stanza has 2 lines) if no poem is provided.
2. Or process an input poem if one is provided.

The poem can be one of three types:
- **Lyric poetry**: Expresses emotions or personal thoughts.
- **Narrative poetry**: Tells a story with characters or events.
- **Dramatic poetry**: Mimics performance or dialogue, like acting on stage.

If you are given no poem, create a new 2-stanza poem focused on emotions.
If a poem is provided, simply return it unchanged.""",

    
   model = "gpt-3"
)

Lyric_poetry_agent = Agent(
    name ="Lyric poetry agent",
    instructions = """
    You are a helpful literature tutor. When a user asks about lyric poetry,
    explain it in a simple, beginner-friendly way. 
    Give clear examples, avoid jargon, and keep the tone supportive. 
    If possible, relate it to music or everyday feelings so it's easy to understand.
    """,
    model = "gpt-3"
)


Narrative_poetry_agent = Agent(
    name = "Narrative poetry agent",
    instructions = """
    You are a helpful literature tutor. 
    When a user asks about narrative poetry, explain it in a simple, beginner-friendly way. 
    Describe that it tells a story with characters and events, like a regular story, but in poem form with rhymes or rhythm. 
    Provide short, clear examples so the user understands easily.
    """,
    model = "gpt-3" 

)


Dramatic_poetry_agent =Agent(
    name = "Dramatic poetry agent",
    instructions = """
    You are a helpful literature tutor. 
    When a user asks about dramatic poetry, explain it in a simple, beginner-friendly way. 
    Describe that it is meant to be performed out loud, where someone acts like a character 
    and speaks their thoughts and feelings to an audience, similar to acting in a theatre. 
    Provide short, clear examples so the user can easily understand.
    """,
    model = "gpt-3"
) 



#custom function to process the poem

class CustomParentAgent(Agent):
    async def run(self, input, config):
        # Step 1: Get poem from poet_agent
        poet_output = await poet_agent.run(input, config)
        
        # Use the original input if provided, otherwise use generated poem
        poem_text = input.strip() if input.strip() else poet_output.output.strip()
        poem_text_lower = poem_text.lower()

        # Step 2: Classify the poem
        if "dialogue" in poem_text_lower or "voice" in poem_text_lower or "stage" in poem_text_lower:
            next_agent = Dramatic_poetry_agent
        elif "story" in poem_text_lower or "event" in poem_text_lower or "character" in poem_text_lower:
            next_agent = Narrative_poetry_agent
        else:
            next_agent = Lyric_poetry_agent

        final_output = await self.handoff(next_agent, poem_text, config)
        print("Final analysis by:", next_agent.name)
        return final_output



parent_agent = CustomParentAgent(
    name="Parent Poet Orchestrator",
    instructions="""
You are the Parent Orchestrator Agent responsible for managing poetry tasks.

When a user gives you a poem or a request:
1. First, pass it to the Poet Agent. If no poem is provided, the Poet Agent will generate one.
2. After receiving the poem, analyze the content and determine its type:
   - If the poem expresses personal emotions or feelings, it is **Lyric**.
   - If it tells a story with events or characters, it is **Narrative**.
   - If it includes dialogue, stage-like performance, or dramatic voice, it is **Dramatic**.
3. Based on this classification, delegate the poem to the correct Analyst Agent:
   - Lyric Analyst Agent
   - Narrative Analyst Agent
   - Dramatic Analyst Agent
4. Return only the final analysis from the selected analyst agent to the user.

If the input is unrelated to poetry, politely inform the user that you only handle poetry-related tasks.
""",

handoffs=[poet_agent, Lyric_poetry_agent, Narrative_poetry_agent, Dramatic_poetry_agent]
)

# Runner
async def main():
   with trace("Hand off Trace"):
    user_poem_query = """
            The sun sets in crimson fire,
            My heart aches with lost desire.

            In silent shadows, I remain,
            Whispering dreams in falling rain."""

    result = await Runner.run(parent_agent, user_poem_query, run_config = config)

    print("___Final_Output___")
    print(result.final_output)



    print("___Last_Agent___")
    print(result.last_agent.name)   


if __name__ == "__main__":
    asyncio.run(main())