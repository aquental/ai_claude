from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()

# Choose a model to use
model = "claude-sonnet-4-6"

# Add a fourth specialist (science_specialist) to the router prompt and update the response instruction
# Router system prompt - decides which specialist to use
router_prompt = """You are a task router. Your job is to analyze user requests and determine which specialist should handle them.

Available specialists:
- math_specialist: For mathematical calculations, equations, and numerical problems
- writing_specialist: For creative writing, essays, stories, and text composition
- code_specialist: For programming questions, code review, and technical implementation
- science_specialist: For science questions and science related topics

Respond with ONLY the specialist name (math_specialist, writing_specialist, or code_specialist) that best matches the user's request."""

# Specialist system prompts
math_specialist_prompt = "You are a mathematics expert. You excel at solving equations, performing calculations, and explaining mathematical concepts clearly."

writing_specialist_prompt = "You are a creative writing expert. You specialize in crafting engaging stories, essays, and helping with all forms of written communication."

code_specialist_prompt = "You are a programming expert. You specialize in writing code, debugging, code review, and explaining technical concepts."

# Create a science_specialist_prompt for handling scientific concepts, theories, and natural phenomena
science_specialist_prompt = "You are a PHD scientist. Your specialization is research and science."

# User request to route
user_request = "How does photosynthesis work in plants?"

# Step 1: Send request to router to determine which specialist to use
router_messages = [
    {
        "role": "user",
        "content": user_request
    }
]

# Get routing decision from Claude
router_response = client.messages.create(
    model=model,
    max_tokens=100,  # Short response expected
    messages=router_messages,
    system=router_prompt
)

# Extract the routing decision
specialist_choice = router_response.content[0].text.strip()
print(f"Router decision: {specialist_choice}")

# Step 2: Route to the appropriate specialist based on the router's decision

# Add a fourth condition for science_specialist in the if-elif-else logic
if specialist_choice == "math_specialist":
    specialist_prompt = math_specialist_prompt
elif specialist_choice == "writing_specialist":
    specialist_prompt = writing_specialist_prompt
elif specialist_choice == "code_specialist":
    specialist_prompt = code_specialist_prompt
elif specialist_choice == "science_specialist":
    specialist_prompt = science_specialist_prompt
else:
    # Default fallback if router gives unexpected response
    specialist_prompt = "You are a helpful assistant."

# Step 3: Send the original request to the chosen specialist
specialist_messages = [
    {
        "role": "user",
        "content": user_request
    }
]

# Get response from the chosen specialist
specialist_response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=specialist_messages,
    system=specialist_prompt
)

# Extract and display the specialist's response
final_response = specialist_response.content[0].text
print("Specialist Response:")
print(final_response)
