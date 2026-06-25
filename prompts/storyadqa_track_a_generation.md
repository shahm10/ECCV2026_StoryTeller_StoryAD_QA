# StoryAD-QA Track A Generation Prompt

Use this prompt to generate one five-choice multiple-choice question from a single continuous video segment.

## Inputs

- `VIDEO_CLIP`: the target video segment
- `MOVIE_OVERVIEW`: a short movie overview used only as background during question construction

## Prompt

You are given a video clip from a movie and a short movie overview. Generate exactly one multiple-choice question about the main visual event, progression, reaction, reveal, or cause-effect moment in the clip.

The question must be answerable from the clip itself. Do not require dialogue, subtitles, prior movie knowledge, later events, or external facts. Do not ask about hidden thoughts, emotions, or motivations unless they are directly visible from actions or reactions.

If the clip does not contain a clear self-contained visual event that supports a high-quality question, output `SKIP`.

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
