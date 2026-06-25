# StoryAD-QA

Official dataset, evaluation, and prompt release for the ECCV 2026 paper:

**StoryTeller: Training-Free Narrative Grounding for Long-Form Audio Description**

StoryAD-QA is a multiple-choice question-answering benchmark for evaluating whether generated audio descriptions preserve the story of a long-form video. The benchmark is released with StoryTeller, a training-free framework for movie audio description that grounds narration in visual evidence, public story context, character continuity, and a lightweight narrative memory.

## Why We Release This Benchmark

Audio description (AD) should help blind and low-vision audiences follow not only what is visible in the current shot, but also how events connect across time: who is present, what changed, which earlier event matters now, and why a visual action is narratively important.

Most automatic AD evaluations still rely on captioning metrics such as CIDEr, SPICE, BLEU, and ROUGE-L. These metrics are useful for measuring overlap with reference text, but they do not directly test whether an AD output contains the information needed to understand the story. A description can use different words from a reference and still be useful; it can also match local words while failing to preserve narrative state.

StoryAD-QA addresses this gap. It turns long-form AD evaluation into a downstream story-reasoning test: given only a system's generated AD text, can an answering model choose the correct answer to grounded questions about the video?

## Relation To StoryTeller

The StoryTeller paper studies training-free long-form audio description. StoryTeller processes movie clips chronologically, builds an identity graph for recurring characters, induces video-supported narrative facts, and maintains a salience-weighted memory that can be reused in later scenes. Public metadata such as movie summaries and character lists can suggest context, but facts are only retained when they are grounded in the video and pass verification.

StoryAD-QA is the paper's QA-based evaluation benchmark. It is designed to complement lexical AD metrics by measuring whether generated descriptions support narrative comprehension.

## Benchmark Design

StoryAD-QA contains five-choice multiple-choice questions. The question generation model sees video evidence and limited movie background for question construction, but evaluation is stricter: the answering model receives only the generated AD text plus the question and answer choices. It does not receive the video, movie title, plot summaries, subtitles, scripts, retrieved metadata, or any other external context.

The benchmark has two evaluation settings:

- **Track A: segment-only QA.** Questions are generated from a single continuous clip window. Evaluation uses the AD generated for that same window.
- **Track B: context-conditioned QA.** Questions are generated from a short prior context window plus a target clip. Evaluation uses only the AD for the target clip, testing whether the description preserves visually grounded cues that make the target moment understandable.

The paper describes the benchmark construction process over 2,729 generated questions. This repository provides a verified public release of **2,572 QA pairs** after validation and cleanup.

## What Is Included

```text
data/
  StoryAD-QA/                    # canonical QA CSVs with gold answers
  StoryAD-QA-questions/          # question/options-only split
  StoryAD-QA-answer-key/         # answer-key/rationale split
  dataset_summary.csv            # per-file counts
evaluation/
  evaluate_storyad_qa.py         # multiple-choice accuracy evaluator
  requirements.txt
prompts/
  storyadqa_track_a_generation.md
  storyadqa_track_b_generation.md
  storyadqa_answering.md
  storyteller_fact_verification.md
docs/
  index.html                     # GitHub Pages project website
  assets/style.css
```

This repository releases annotations, answers, prompt templates, and evaluation code. It does **not** release movie videos, audio, frames, subtitles, scripts, or copyrighted media.

## Data Files

The canonical public CSVs are in:

```text
data/StoryAD-QA/
```

Each row contains:

```text
file, raw_response, question, option_A, option_B, option_C, option_D, option_E, correct_answer, rationale
```

- `file`: clip identifier used for alignment with the evaluation windows
- `raw_response`: original formatted model response used to create the row
- `question`: multiple-choice question
- `option_A` through `option_E`: answer choices
- `correct_answer`: gold label, one of `A`, `B`, `C`, `D`, or `E`
- `rationale`: short explanation for the gold answer

The combined files in `data/StoryAD-QA/` are the authoritative release for reproducibility. We also provide two convenience splits:

- `data/StoryAD-QA-questions/`: question and option fields without the gold answer
- `data/StoryAD-QA-answer-key/`: answer labels and rationales

Keeping both formats is intentional. The combined files make the released dataset transparent and easy to audit, while the split files support benchmark-style use where questions and answer keys are handled separately.

| File | Setting | Questions |
|---|---|---:|
| `movie_qa_v5_30s_gemini-3-flash-preview.csv` | Track A, 30s segment | 858 |
| `movie_qa_v5_60s_gemini-3-flash-preview.csv` | Track A, 60s segment | 430 |
| `movie_qa_v5_120s_gemini-3-flash-preview.csv` | Track A, 120s segment | 212 |
| `movie_qa_v5_240s_gemini-3-flash-preview.csv` | Track A, 240s segment | 109 |
| `movie_qa_v9_60s_gemini-3-flash-preview.csv` | Track B, context-conditioned | 449 |
| `movie_qa_v9_90s_gemini-3-flash-preview.csv` | Track B, context-conditioned | 294 |
| `movie_qa_v9_120s_gemini-3-flash-preview.csv` | Track B, context-conditioned | 220 |

## Evaluation

To evaluate an AD system:

1. Generate audio descriptions for the corresponding movie clips or windows.
2. Use the released StoryAD-QA answering prompt to answer each question from the generated AD text only.
3. Save model predictions as a CSV with `file,prediction`, where `prediction` is one of `A`, `B`, `C`, `D`, or `E`.
4. Score predictions against the gold CSV.

```bash
pip install -r evaluation/requirements.txt
python evaluation/evaluate_storyad_qa.py \
  --gold data/StoryAD-QA/movie_qa_v5_30s_gemini-3-flash-preview.csv \
  --predictions path/to/predictions.csv
```

The evaluator reports total examples, evaluated examples, missing predictions, invalid predictions, overall accuracy, and per-answer accuracy. The script does not call an LLM; it scores predictions that have already been produced.

## Prompts

The `prompts/` folder contains the prompt templates used for the benchmark and paper pipeline:

- Track A question generation from a single video segment
- Track B context-conditioned question generation
- AD-only multiple-choice answering for evaluation
- strict video-grounded fact verification used by StoryTeller

We include prompts because StoryAD-QA is not only a dataset release; it is also a reproducible evaluation protocol.

## GitHub Pages

The `docs/` folder contains a lightweight project website suitable for GitHub Pages. To publish it, enable GitHub Pages from the `main` branch and `/docs` folder in the repository settings.

## Media And Licensing

This release intentionally excludes copyrighted video media and derived media assets. The `file` field is an identifier for alignment with the evaluation clips used in the paper. Users are responsible for ensuring lawful access to any underlying video content.

Please confirm the final license with all authors before public release.

## Citation

Please cite the StoryTeller ECCV 2026 paper when using StoryAD-QA:

```bibtex
@inproceedings{hahm2026storyteller,
  title = {StoryTeller: Training-Free Narrative Grounding for Long-Form Audio Description},
  author = {Hahm, Seung Hyun and Dinh, Minh T. and Jin, SouYoung},
  booktitle = {European Conference on Computer Vision},
  year = {2026}
}
```
