# StoryAD-QA Track B Generation Prompt

Use this prompt to generate one five-choice multiple-choice question from a prior context window plus a target clip.

## Inputs

- `CONTEXT_VIDEO`: the preceding context window
- `TARGET_VIDEO`: the target clip
- `MOVIE_OVERVIEW`: a short movie overview used only as background during question construction

## Prompt

You are given a preceding context video and a target video clip from the same movie. Generate exactly one multiple-choice question whose answer is visible in the target clip, but where the preceding context helps identify or interpret the person, object, situation, action, or visual change in the target clip.

The question should test whether an audio description preserves context across time. Do not rely on character names, dialogue, subtitles, scripts, later events, or outside movie knowledge. The correct answer must be supported by the target clip, and the context should make the question more meaningful or less ambiguous.

If there is no clear visual moment in the target clip that connects to the preceding context, output `SKIP`.

Return exactly:

```text
Question: ...
A. ...
B. ...
C. ...
D. ...
E. ...
Correct Answer: ...
Rationale: ...
```
