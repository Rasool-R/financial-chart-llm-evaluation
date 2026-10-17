# Financial Chart LLM Evaluation

A small benchmark for testing how well a vision-capable LLM answers questions about financial charts. The dataset contains Persian questions about Iranian stock and asset charts, covering forecasting and chart-reading. The pipeline sends each chart and question to the model, collects structured answers, and measures them against ground truth.

## How It Works

1. **Dataset**: `data/final_dataset_filtered.xlsx` holds 36 questions, each linked to a chart image in `img/`, with the expected answer, answer type, task type, difficulty, and forecast horizon.
2. **Prediction**: `main.py` sends each image and question to the model through LangChain. Structured output (Pydantic) forces clean answers: `yes`/`no` for yes/no questions, a `float` for numeric ones.
3. **Evaluation**: `src/evaluate.py` compares predictions with ground truth and writes a Markdown report.

Predictions are saved to `data/predictions.xlsx` every 5 rows, and also if a request fails, so a crash does not lose progress.

## Metrics

| Question type | Metrics |
|---------------|---------|
| Yes/No (18 rows) | Accuracy, F1 (positive class: `yes`) |
| Numeric (18 rows) | MAPE, plus a list of predictions with error above 20% |

## Results

Results from the included run (see `reports/evaluation_report.md` for the full error tables):

| Metric | Value |
|--------|-------|
| Yes/No accuracy | 0.611 |
| Yes/No F1 | 0.696 |
| Numeric MAPE | 1852% |
| Numeric predictions above 20% error | 8 of 18 |

- All 7 wrong yes/no answers are cases where the correct answer was `yes` and the model said `no`, which suggests a bias toward negative answers on forecast questions.
- The MAPE is dominated by a few extreme cases, mostly profit/loss percentage questions where the model's value and the ground truth differ by orders of magnitude. Treat it together with the error count rather than as a standalone number.

## Getting Started

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Create a `.env` file** in the project root

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=your_vision_model   # must support image input
OPENAI_URL_BASE=                 # optional, for OpenAI-compatible endpoints
```

**3. Run predictions, then evaluation**

```bash
python main.py
python -m src.evaluate
```

## Project Structure

```
financial-chart-llm-evaluation/
├── main.py              # Runs the model over the dataset
├── data/
│   ├── final_dataset_filtered.xlsx   # Questions and ground truth
│   └── predictions.xlsx              # Dataset + model answers
├── img/                 # Chart images
├── reports/
│   └── evaluation_report.md          # Generated results
└── src/
    ├── model.py         # LLM setup with structured output
    ├── predict.py       # Prompt, image encoding, answer extraction
    ├── schemas.py       # YesNoAnswer / NumberAnswer models
    └── evaluate.py      # Metrics and report generation
```

## Using Your Own Data

Add chart images to `img/` and rows to the Excel file with the columns `image_file`, `question`, `answer`, `answer_type` (`yes_no` or `number`), and an empty `LLM_answer`. The script checks that all images exist before it starts.

## Tech Stack

Python · LangChain · Pydantic · pandas · scikit-learn · OpenAI-compatible vision models
