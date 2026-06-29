import dspy
import os
from typing import Dict, List

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)


# Create a class-based signature for citation faithfulness checking
# The class should inherit from dspy.Signature and include a descriptive docstring
# explaining that it verifies if claims are supported by context
class CheckCitationFaithfulness(dspy.Signature):
    """Verify whether the given claim (text) is faithful to / supported by the provided context.
    Return evidence as a dictionary that maps key phrases or sentences from the claim to the specific supporting excerpts from the context."""
    # Define two input fields:
    # - context (string with description indicating facts are trusted)
    context: str = dspy.InputField(
        desc="Trusted source material containing facts")
    # - text (string for the claim to verify)
    text: str = dspy.InputField(
        desc="The claim or statement to verify against the context")

    # Define two output fields:
    # - faithfulness (boolean indicating if claim is supported)
    faithfulness: bool = dspy.OutputField(
        desc="True if the claim is fully supported by the context, False otherwise")
    # - evidence (dictionary mapping strings to lists of strings for supporting evidence)
    evidence: Dict[str, List[str]] = dspy.OutputField(
        desc="Dictionary mapping key phrases/sentences from the claim to lists of supporting excerpts from the context")


# Example context and claim
context = "The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League One last term, with Blackpool and then Colchester United. He scored twice for the U's but was unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been revealed. Find all the latest football transfers on our dedicated page."

text = "Lee scored 3 goals for Colchester United."

# Create a predictor using your signature
predictor = dspy.Predict(CheckCitationFaithfulness)
# Use the predictor to check the claim
result = predictor(context=context, text=text)
# Print the results showing both the faithfulness assessment and the evidence
print(result)
print("Faithfulness:", result.faithfulness)
print("Evidence:", result.evidence)
