# Prompts

This folder contains the public prompt templates associated with StoryTeller and StoryAD-QA.

- `storyadqa_track_a_generation.md`: segment-only StoryAD-QA question generation
- `storyadqa_track_b_generation.md`: context-conditioned StoryAD-QA question generation
- `storyadqa_answering.md`: AD-only multiple-choice answering used for evaluation
- `storyteller_fact_verification.md`: strict video-grounded fact verification used by StoryTeller

The prompts are released to make the benchmark construction and evaluation protocol auditable. They intentionally describe the information available to each model call: generation may use video evidence and limited background for question construction, while evaluation answers must be produced from generated AD text only.
