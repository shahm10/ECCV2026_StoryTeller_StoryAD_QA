# Dataset Card: StoryAD-QA

## Dataset Summary

StoryAD-QA is a multiple-choice question-answering benchmark released with the ECCV 2026 paper **StoryTeller: Training-Free Narrative Grounding for Long-Form Audio Description**. It evaluates whether generated audio descriptions preserve story-level understanding in long-form movie videos.

Unlike lexical-overlap AD metrics, StoryAD-QA asks whether a system output contains enough information to answer grounded questions about events, character actions, and narrative context.

## Motivation

Long-form audio description requires more than frame-level captioning. A useful AD system must identify recurring characters, preserve context across scenes, and explain narratively important actions without relying only on local visual details.

StoryTeller proposes a training-free framework with an identity graph, grounded narrative facts, and salience-weighted memory for this setting. StoryAD-QA is released to support that evaluation: it provides a QA-based benchmark for measuring story comprehension in generated AD outputs.

## Contents

The release includes:

- public QA CSVs and gold answers
- question-only CSVs
- answer-key CSVs
- an evaluation script for multiple-choice accuracy
- prompt templates for Track A generation, Track B generation, AD-only answering, and fact verification

The release does not include videos, audio, frames, or subtitles.

## Data Fields

Each row contains:

- `file`: clip identifier/path
- `raw_response`: original formatted QA generation response
- `question`: multiple-choice question
- `option_A` through `option_E`: answer choices
- `correct_answer`: gold answer label
- `rationale`: explanation for the gold answer

## Dataset Size

The StoryAD-QA construction process described in the paper produced 2,729 generated questions. This repository contains a verified public release of 2,572 QA pairs across seven CSV files after validation and cleanup. See `data/dataset_summary.csv` for per-file counts.

The main files in `data/StoryAD-QA/` include both questions and answers. The same data is also available in `data/StoryAD-QA-questions/` and `data/StoryAD-QA-answer-key/` for workflows that separate question distribution from answer-key evaluation.

## Intended Use

StoryAD-QA is intended for:

- evaluating generated AD outputs with multiple-choice QA
- comparing systems on narrative comprehension
- reproducing StoryTeller paper evaluations
- studying prompt-based QA generation, AD-only answering, and video-grounded verification

During evaluation, the answering model should receive only the generated AD text, the question, and the answer choices. It should not receive the video, movie title, plot summaries, subtitles, scripts, retrieved metadata, or external context.

## Out-of-Scope Use

StoryAD-QA should not be used as redistributed movie video. The dataset contains annotations and identifiers only.

## Legal And Ethical Notes

This repository does not distribute copyrighted movie media. Users are responsible for ensuring lawful access to any underlying clips referenced by `file`.

## Maintenance

This release is prepared for ECCV 2026 public release. Final camera-ready metadata, license, and links should be confirmed before publication.
