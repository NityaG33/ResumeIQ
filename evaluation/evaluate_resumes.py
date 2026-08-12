import os
import sys
import traceback
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from ml.pdf_parser import extract_text_from_pdf
from ml.resume_quality import build_resume_report


RESUME_FOLDER = "evaluation/resumes"
OUTPUT_FILE = "evaluation/results.csv"

rows = []

for filename in os.listdir(RESUME_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        RESUME_FOLDER,
        filename,
    )

    try:

        resume_text = extract_text_from_pdf(pdf_path)

        report = build_resume_report(resume_text)

        breakdown = report["score_breakdown"]

        rows.append({

            "Resume": filename,

            "Overall Score": report["overall_score"],
            "Grade": report["grade"],
            "Summary": report["summary"],

            "Structure": breakdown["structure"]["score"],
            "Structure Max": breakdown["structure"]["max_score"],

            "Contact": breakdown["contact"]["score"],
            "Contact Max": breakdown["contact"]["max_score"],

            "Content": breakdown["content"]["score"],
            "Content Max": breakdown["content"]["max_score"],

            "ATS": breakdown["ats"]["score"],
            "ATS Max": breakdown["ats"]["max_score"],

            "Strengths":
                " | ".join(report["strengths"]),

            "Recommendations":
                " | ".join(report["recommendations"]),

            "Priority Improvements":
                " | ".join(report["priority_improvements"]),
        })

        print(f"✓ {filename}")

    except Exception:

        print(f"\n✗ Failed: {filename}")
        traceback.print_exc()

df = pd.DataFrame(rows)

df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\n==============================")
print(f"Processed {len(df)} resumes")
print(f"Saved to {OUTPUT_FILE}")
print("==============================")