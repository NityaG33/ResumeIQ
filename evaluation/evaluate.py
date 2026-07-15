import json
from collections import defaultdict

from ml.scoring import compute_match_score


def evaluate():
    with open("evaluation/test_cases.json", "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    correct = 0
    confusion = defaultdict(int)
    prediction_distribution = defaultdict(int)

    for idx, case in enumerate(test_cases, 1):

        result = compute_match_score(
            case["resume_text"],
            case["jd_text"],
            case["role"],
        )

        predicted = result["confidence"]
        expected = case["expected_confidence"]
        prediction_distribution[predicted] += 1
        confusion[
            f"Expected: {expected} | Predicted: {predicted}"
        ] += 1
        is_correct = predicted == expected

        if is_correct:
            correct += 1

        print(f"\nTest Case {idx}")
        print("Expected:", expected)
        print("Predicted:", predicted)
        print("Match Score:", result["final_score"])
        print(
            "Resume Quality:",
            result["resume_report"]["overall_score"],
        )
        print(
            "Result:",
            "✅ Correct" if is_correct else "❌ Incorrect",
        )

    accuracy = (correct / total) * 100

    print("\n--------------------------------")
    print("Total Cases:", total)
    print("Correct:", correct)
    print(f"Accuracy: {accuracy:.2f}%")
    print("--------------------------------")
    print("\nPrediction Distribution")

    for label, count in prediction_distribution.items():
        print(f"{label}: {count}")

    print("\nConfusion Matrix")

    for key, value in confusion.items():
        print(f"{key} -> {value}")


if __name__ == "__main__":
    evaluate()