import asyncio
from anthropic import AsyncAnthropic

# Initialize the async Anthropic client
client = AsyncAnthropic()

# List of independent questions for Paris trip planning
questions = [
    "What are the top 3 must-see attractions in Paris?",
    "What is the most efficient way to get around Paris as a tourist?",
    "What are important cultural etiquette tips for visitors to France?"
]


async def ask_question(question):
    """
    Async function to ask Claude a single question
    """
    print(f"🔄 Asking: {question}")

    # Send async request to Claude
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system="You are a travel expert. Give brief, helpful answers.",
        messages=[{"role": "user", "content": question}]
    )

    # Extract the answer
    answer = response.content[0].text

    print(f"✅ Answered: {question}")

    return question, answer


# Create an async function that takes the research results as a parameter
    # Combine all Q&A pairs into a formatted research string
    # Send the combined research to Claude with instructions to create a brief, practical travel guide
    # Return the travel guide
async def create_travel_plan(results):
    """
    Aggregate all research results into a comprehensive travel plan
    """
    # Combine all Q&A pairs into a formatted string
    combined_research = ""
    for question, answer in results:
        combined_research += f"{question}\n{answer}\n\n"

    # Create aggregator prompt
    aggregator_prompt = f"Create a brief Paris travel guide based on this research:\n\n{combined_research}\n\nMake it concise and practical."

    # Send to Claude for final synthesis
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system="You are a travel planner. Create brief, useful guides.",
        messages=[{"role": "user", "content": aggregator_prompt}]
    )

    return response.content[0].text


async def main():
    """
    Execute parallel research and create comprehensive travel plan
    """
    print(f"Starting {len(questions)} research questions in parallel...")

    # Create tasks for all questions
    tasks = [ask_question(question) for question in questions]

    # Execute all tasks in parallel
    results = await asyncio.gather(*tasks)

    print("\nResearch completed!")

    # Call your aggregation function with the results and store the return value
    travel_plan = await create_travel_plan(results)

    # Print the travel plan with a nice header like "Paris Travel Guide:"
    print("\nParis Travel Guide:")
    print(travel_plan)

# Run the parallel workflow
if __name__ == "__main__":
    asyncio.run(main())
