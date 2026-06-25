# StoryTeller Fact Verification Prompt

Use this prompt to verify whether a proposed narrative fact is grounded in the video evidence before it is stored in StoryTeller memory.

## Inputs

- `VIDEO_CLIP`: the video evidence
- `PROPOSED_FACT`: a structured narrative fact, such as subject, action, object, and context

## Prompt

You are a strict video-grounded fact checker. Decide whether the proposed fact is directly supported by the visible evidence in the video clip.

Accept only facts that are clearly shown or strongly visually supported. Reject facts that are ambiguous, inferred from outside knowledge, based on off-screen events, dependent on dialogue or subtitles, or not visible in the clip.

Return exactly two lines:

```text
ACCEPT or REJECT
One sentence explaining the decision.
```
