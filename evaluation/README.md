# Evaluation

Use `evaluate_storyad_qa.py` to score multiple-choice predictions against a StoryAD-QA answer-key CSV.

## Prediction Format

Predictions should be a CSV with:

```text
file,prediction
```

The `prediction` value should be one of:

```text
A, B, C, D, E
```

If a CSV contains duplicate `file` values, add a `row_index` column to disambiguate examples. The evaluator supports either:

- `file,prediction`
- `row_index,prediction`
- `file,row_index,prediction`

## Example

```bash
python evaluation/evaluate_storyad_qa.py \
  --answers data/StoryAD-QA/movie_qa_v5_30s_gemini-3-flash-preview.csv \
  --predictions predictions/my_model_v5_30s.csv
```

## Output

The script prints:

- total examples
- evaluated examples
- missing predictions
- invalid predictions
- accuracy
- per-answer accuracy
