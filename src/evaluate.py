from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import mean_absolute_percentage_error


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "predictions.xlsx"
REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.md"

NUMERIC_ERROR_THRESHOLD = 20


def normalize_label(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value in {"yes", "no"}:
        return value

    return None


def evaluate_yes_no(df):
    data = df[df["answer_type"] == "yes_no"].copy()

    data["true_label"] = data["answer"].apply(normalize_label)
    data["pred_label"] = data["LLM_answer"].apply(normalize_label)

    valid_mask = data["true_label"].notna() & data["pred_label"].notna()
    valid_data = data[valid_mask].copy()

    if valid_data.empty:
        return {
            "count": 0,
            "accuracy": None,
            "f1": None,
            "errors": data,
        }

    y_true = valid_data["true_label"]
    y_pred = valid_data["pred_label"]

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(
        y_true,
        y_pred,
        pos_label="yes",
        zero_division=0,
    )

    errors = valid_data[y_true != y_pred].copy()

    return {
        "count": len(valid_data),
        "accuracy": accuracy,
        "f1": f1,
        "errors": errors,
    }


def evaluate_numbers(df):
    data = df[df["answer_type"] == "number"].copy()

    data["true_number"] = pd.to_numeric(
        data["answer"], errors="coerce"
    )
    data["pred_number"] = pd.to_numeric(
        data["LLM_answer"], errors="coerce"
    )

    valid_mask = (
        data["true_number"].notna()
        & data["pred_number"].notna()
    )

    valid_data = data[valid_mask].copy()

    zero_mask = valid_data["true_number"] == 0
    zero_actual_count = int(zero_mask.sum())

    mape_data = valid_data[~zero_mask].copy()

    if mape_data.empty:
        mape = None
    else:
        mape = mean_absolute_percentage_error(
            mape_data["true_number"],
            mape_data["pred_number"],
        ) * 100

    mape_data["error_pct"] = (
        (
            mape_data["true_number"]
            - mape_data["pred_number"]
        ).abs()
        / mape_data["true_number"].abs()
    ) * 100

    errors = mape_data[
        mape_data["error_pct"] > NUMERIC_ERROR_THRESHOLD
    ].copy()

    return {
        "count": len(valid_data),
        "mape_count": len(mape_data),
        "zero_actual_count": zero_actual_count,
        "mape": mape,
        "errors": errors,
    }


def format_metric(value):
    if value is None:
        return "N/A"

    return f"{value:.4f}"


def generate_report(df, yes_no_results, number_results):
    yes_no_errors = yes_no_results["errors"]
    number_errors = number_results["errors"]

    lines = [
        "# Financial Chart LLM Evaluation Report",
        "",
        "## Dataset Summary",
        "",
        f"- Total evaluated rows: {len(df)}",
        f"- Yes/No rows: {(df['answer_type'] == 'yes_no').sum()}",
        f"- Numeric rows: {(df['answer_type'] == 'number').sum()}",
        "",
        "## Yes/No Evaluation",
        "",
        f"- Valid predictions: {yes_no_results['count']}",
        f"- Accuracy: {format_metric(yes_no_results['accuracy'])}",
        f"- F1-score (positive class: yes): "
        f"{format_metric(yes_no_results['f1'])}",
        f"- Incorrect predictions: {len(yes_no_errors)}",
        "",
        "## Numeric Evaluation",
        "",
        f"- Valid numeric predictions: {number_results['count']}",
        f"- Samples used for MAPE: {number_results['mape_count']}",
        f"- Zero actual values excluded from MAPE: "
        f"{number_results['zero_actual_count']}",
        f"- MAPE (%): {format_metric(number_results['mape'])}",
        f"- Predictions with error above "
        f"{NUMERIC_ERROR_THRESHOLD}%: {len(number_errors)}",
        "",
        "## Incorrect Yes/No Predictions",
        "",
    ]

    if yes_no_errors.empty:
        lines.append("No incorrect Yes/No predictions were found.")
    else:
        lines.append(
            yes_no_errors[
                ["image_file", "question", "answer", "LLM_answer"]
            ].to_markdown(index=False)
        )

    lines.extend([
        "",
        "## Numeric Predictions with High Error",
        "",
    ])

    if number_errors.empty:
        lines.append(
            f"No numeric predictions exceeded "
            f"{NUMERIC_ERROR_THRESHOLD}% error."
        )
    else:
        error_table = number_errors[
            [
                "image_file",
                "question",
                "answer",
                "LLM_answer",
                "error_pct",
            ]
        ].copy()

        error_table["error_pct"] = error_table["error_pct"].map(
            lambda value: f"{value:.2f}%"
        )

        lines.append(error_table.to_markdown(index=False))

    lines.extend([
        "",
        "## Evaluation Notes",
        "",
        "- MAPE excludes rows where the actual value is zero.",
        "- Numeric error examples use a 20% error threshold.",
        "- Invalid or missing predictions are excluded from the "
        "corresponding metric calculations.",
        "- Results reflect the available dataset and the selected model.",
        "",
    ])

    return "\n".join(lines)


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Predictions file not found: {INPUT_PATH}"
        )

    df = pd.read_excel(INPUT_PATH)

    required_columns = {
        "image_file",
        "question",
        "answer_type",
        "answer",
        "LLM_answer",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    yes_no_results = evaluate_yes_no(df)
    number_results = evaluate_numbers(df)

    report = generate_report(
        df,
        yes_no_results,
        number_results,
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print("Evaluation completed.")
    print(f"Total rows: {len(df)}")
    print(f"Yes/No Accuracy: {format_metric(yes_no_results['accuracy'])}")
    print(f"Yes/No F1-score: {format_metric(yes_no_results['f1'])}")
    print(f"Numeric MAPE: {format_metric(number_results['mape'])}%")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
