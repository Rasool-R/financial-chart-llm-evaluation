
import pandas as pd

from src.predict import get_answer, resolve_image_path


DATA_PATH = "data/final_dataset_filtered.xlsx"
OUTPUT_PATH = "data/predictions.xlsx"
CHECKPOINT_INTERVAL = 5


def validate_dataset(df: pd.DataFrame) -> None:
    required_columns = {
        "image_file",
        "question",
        "answer_type",
        "LLM_answer",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    invalid_types = set(df["answer_type"].dropna().unique()) - {
        "yes_no",
        "number",
    }

    if invalid_types:
        raise ValueError(
            f"Unsupported answer types: {invalid_types}"
        )

    missing_images = []

    for image_file in df["image_file"].dropna().unique():
        try:
            resolve_image_path(str(image_file))
        except FileNotFoundError:
            missing_images.append(str(image_file))

    if missing_images:
        print("Missing image files:")
        for image_file in missing_images:
            print(f" - {image_file}")

        raise FileNotFoundError(
            "Resolve all missing images before running predictions."
        )


def main() -> None:
    df = pd.read_excel(DATA_PATH)
    df["LLM_answer"] = df["LLM_answer"].astype("object")

    validate_dataset(df)

    # Preserve existing predictions when resuming.
    if "LLM_answer" not in df.columns:
        df["LLM_answer"] = pd.NA

    for idx, row in df.iterrows():
        current_answer = row["LLM_answer"]

        if pd.notna(current_answer):
            continue

        try:
            answer = get_answer(
                question=str(row["question"]),
                image_file=str(row["image_file"]),
                answer_type=str(row["answer_type"]),
            )

            df.at[idx, "LLM_answer"] = answer

            print(
                f"[{idx + 1}/{len(df)}] "
                f"Type: {row['answer_type']} | "
                f"Answer: {answer}"
            )

        except Exception:
            df.to_excel(OUTPUT_PATH, index=False)
            print(f"Checkpoint saved to {OUTPUT_PATH}")
            raise

        if (idx + 1) % CHECKPOINT_INTERVAL == 0:
            df.to_excel(OUTPUT_PATH, index=False)
            print(f"Checkpoint saved: {idx + 1} rows processed")

    df.to_excel(OUTPUT_PATH, index=False)
    print(f"Predictions saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
