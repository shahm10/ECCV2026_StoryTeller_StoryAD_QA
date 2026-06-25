# StoryAD-QA Answering Prompt

Use this prompt to answer StoryAD-QA questions during evaluation.

## Inputs

- `AUDIO_DESCRIPTION`: generated AD text from the system being evaluated
- `QUESTION`: the StoryAD-QA question
- `OPTIONS`: five answer choices

## Prompt

Answer the multiple-choice question using only the provided audio description. Do not use the video, movie title, subtitles, scripts, retrieved metadata, prior movie knowledge, or external information.

If the audio description does not provide enough evidence, choose the best-supported option from the text and explain the limitation in the rationale.

Return exactly:

```text
Answer: A/B/C/D/E
Rationale: ...
```
