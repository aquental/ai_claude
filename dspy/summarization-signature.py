import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Create a string-based signature for summarization
# Define a signature that takes a document as input and returns a summary as output
summarize = dspy.Predict('document -> summary')

# Example document to summarize
document = "The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League One last term, with Blackpool and then Colchester United. He scored twice for the U's but was unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been revealed. Find all the latest football transfers on our dedicated page."

# Use the signature to generate a summary
result = summarize(document=document)

# Print the summary
print(result.summary)
