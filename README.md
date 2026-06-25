# StoryAD-QA

Official ECCV 2026 release for **StoryTeller: Training-Free Narrative Grounding for Long-Form Audio Description**.

Seung Hyun Hahm, Minh T. Dinh, SouYoung Jin<br>
Dartmouth College<br>
ECCV 2026

[Dataset](data/StoryAD-QA/) | [Evaluation Code](evaluation/) | [Prompts](prompts/)

## Overview

StoryTeller is a training-free framework for long-form movie audio description. Its goal is to generate descriptions that help viewers follow a story over time, not just describe isolated frames. This matters because movie understanding depends on continuity: recurring characters, prior actions, visual consequences, scene transitions, and story-relevant details that may only become meaningful later.

StoryTeller addresses this setting by maintaining narrative state while processing clips chronologically. It uses character continuity, video-grounded facts, and a lightweight memory of salient story information to produce audio descriptions that are more coherent across long videos.

StoryAD-QA is the benchmark released with StoryTeller. It evaluates whether generated audio descriptions preserve the information needed to answer grounded questions about the story. Instead of only comparing generated descriptions to reference text, StoryAD-QA tests whether the descriptions support downstream narrative understanding.

This repository contains the official StoryAD-QA release for the ECCV 2026 StoryTeller paper, including annotations, answer keys, evaluation code, and prompt templates. It does not include movie videos, audio, frames, subtitles, or scripts.

## Benchmark

StoryAD-QA contains five-option multiple-choice questions over movie clips. The questions are visually grounded and are designed to test whether an audio description preserves information that matters for story understanding.

The benchmark includes two settings:

| Setting | Description |
|---|---|
| Track A: segment QA | Questions are generated from a single clip window. The description for that same window is used for answering. |
| Track B: context QA | Questions are generated from prior context plus a target clip. Only the target-clip description is used for answering, so the task tests whether the description carries the relevant context forward. |

In the paper, StoryAD-QA is used as an evaluation benchmark for generated AD. The answering model receives only:

- the generated audio description
- the question
- the five answer choices

It does not receive the video, movie title, plot summary, subtitles, script, retrieved metadata, or outside context.

The paper describes benchmark construction over 2,729 generated questions. This repository contains a verified public release of **2,572 QA pairs** after validation and cleanup.

## Repository Structure

```text
data/
  StoryAD-QA/                    # full QA files with answer keys
  StoryAD-QA-questions/          # questions and answer choices only
  StoryAD-QA-answer-key/         # correct answers and rationales
  dataset_summary.csv            # counts by file
evaluation/
  evaluate_storyad_qa.py         # accuracy evaluator
  requirements.txt
prompts/
  storyadqa_track_a_generation.md
  storyadqa_track_b_generation.md
  storyadqa_answering.md
  storyteller_fact_verification.md
docs/
  index.html                     # GitHub Pages site
```

## Data Format

The main release files are in `data/StoryAD-QA/`.

Each CSV row contains:

| Column | Description |
|---|---|
| `file` | Clip identifier used to align the question with an evaluation window |
| `raw_response` | Original formatted model response used during dataset construction |
| `question` | Multiple-choice question |
| `option_A` ... `option_E` | Five answer choices |
| `correct_answer` | Correct choice, one of `A`, `B`, `C`, `D`, or `E` |
| `rationale` | Short explanation for the correct choice |

The full files in `data/StoryAD-QA/` are the main dataset. The question-only and answer-key folders are provided for workflows where questions and answers should be handled separately.

| File | Setting | Questions |
|---|---|---:|
| `movie_qa_v5_30s_gemini-3-flash-preview.csv` | Track A, 30s segment | 858 |
| `movie_qa_v5_60s_gemini-3-flash-preview.csv` | Track A, 60s segment | 430 |
| `movie_qa_v5_120s_gemini-3-flash-preview.csv` | Track A, 120s segment | 212 |
| `movie_qa_v5_240s_gemini-3-flash-preview.csv` | Track A, 240s segment | 109 |
| `movie_qa_v9_60s_gemini-3-flash-preview.csv` | Track B, context QA | 449 |
| `movie_qa_v9_90s_gemini-3-flash-preview.csv` | Track B, context QA | 294 |
| `movie_qa_v9_120s_gemini-3-flash-preview.csv` | Track B, context QA | 220 |

## Evaluation

The evaluation code scores multiple-choice predictions against the released answer key.

The intended workflow is:

1. Run an audio description system on the evaluation clips.
2. Ask an answering model to answer each StoryAD-QA question using only the generated AD text.
3. Save the selected choices in a prediction CSV.
4. Run the evaluator to compute accuracy.

Prediction CSV format:

```text
file,prediction
movie_id/segment_0001.mp4,A
movie_id/segment_0002.mp4,D
```

If a file identifier appears more than once, include `row_index`:

```text
file,row_index,prediction
movie_id/segment_0001.mp4,0,A
movie_id/segment_0001.mp4,1,C
```

Run:

```bash
pip install -r evaluation/requirements.txt
python evaluation/evaluate_storyad_qa.py \
  --answers data/StoryAD-QA/movie_qa_v5_30s_gemini-3-flash-preview.csv \
  --predictions path/to/predictions.csv
```

The script reports the number of questions, matched predictions, missing predictions, invalid predictions, and accuracy. It does not call a language model; it only scores predictions that have already been produced.

## Prompts

The `prompts/` folder includes the public prompt templates for:

- Track A question generation
- Track B context-conditioned question generation
- AD-only answer selection
- StoryTeller video-grounded fact verification

These prompts are included so the dataset construction and evaluation protocol are transparent.

## Notes On Media

This repository releases annotations and evaluation code only. It does not redistribute copyrighted videos or derived media. The `file` column is an identifier for aligning questions with the evaluation clips used in the paper. Users are responsible for obtaining lawful access to any underlying video content.

## Citation

```bibtex
@inproceedings{hahm2026storyteller,
  title = {StoryTeller: Training-Free Narrative Grounding for Long-Form Audio Description},
  author = {Hahm, Seung Hyun and Dinh, Minh T. and Jin, SouYoung},
  booktitle = {European Conference on Computer Vision},
  year = {2026}
}
```
