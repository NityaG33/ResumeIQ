import os
import sys
import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

from ml.pdf_parser import extract_text_from_pdf
from services.match_service import run_match


# ============================================================
# PATHS
# ============================================================

RESUME_FOLDER = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "resumes"
)

JD_FOLDER = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "jds"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "jd_matching_results.csv"
)


# ============================================================
# ROLE MAPPING
# ============================================================

ROLE_MAPPING = {
    "backend.txt": "backend",
    "frontend.txt": "frontend",
    "software_engineer.txt": "software_engineer",
    "ml_engineer.txt": "ml_engineer",
}


# ============================================================
# LOAD JOB DESCRIPTIONS
# ============================================================

jds = []

for filename in sorted(
    os.listdir(JD_FOLDER)
):

    if not filename.lower().endswith(".txt"):
        continue

    role = ROLE_MAPPING.get(
        filename.lower()
    )

    if not role:
        print(
            f"Skipping unknown JD: {filename}"
        )
        continue

    jd_path = os.path.join(
        JD_FOLDER,
        filename
    )

    try:

        with open(
            jd_path,
            "r",
            encoding="utf-8"
        ) as file:

            jd_text = file.read()

        if not jd_text.strip():
            print(
                f"Skipping empty JD: {filename}"
            )
            continue

        jds.append({
            "filename": filename,
            "role": role,
            "text": jd_text,
        })

    except Exception as e:

        print(
            f"Failed to load JD "
            f"{filename}: {e}"
        )


print(
    f"Loaded {len(jds)} job descriptions."
)


# ============================================================
# FIND RESUMES
# ============================================================

resume_files = [
    filename
    for filename in sorted(
        os.listdir(RESUME_FOLDER)
    )
    if filename.lower().endswith(".pdf")
]


expected_tests = (
    len(resume_files) * len(jds)
)


print(
    f"Found {len(resume_files)} resumes."
)

print(
    f"Expected matches: {expected_tests}"
)

print()


# ============================================================
# EVALUATION
# ============================================================

rows = []

successful_tests = 0
failed_tests = 0


for resume_filename in resume_files:

    resume_path = os.path.join(
        RESUME_FOLDER,
        resume_filename
    )

    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    try:

        resume_text = extract_text_from_pdf(
            resume_path
        )

        if not resume_text.strip():

            print(
                f"✗ Empty resume: "
                f"{resume_filename}"
            )

            # Every JD is effectively a failed
            # evaluation for this resume.
            failed_tests += len(jds)

            continue

    except Exception as e:

        print(
            f"✗ PDF extraction failed: "
            f"{resume_filename}"
        )

        print(
            f"  Error: {e}"
        )

        failed_tests += len(jds)

        continue


    # --------------------------------------------------------
    # Match resume against every JD
    # --------------------------------------------------------

    for jd in jds:

        jd_filename = jd["filename"]
        role = jd["role"]

        print(
            f"Testing: "
            f"{resume_filename} "
            f"→ {jd_filename}"
        )

        try:

            result = run_match(
                resume_text,
                jd["text"],
                role,
            )


            # =================================================
            # IMPORTANT
            # run_match() returns:
            #
            # {
            #     "jd_match": {...},
            #     "resume_report": {...},
            #     "recommendations": {...},
            #     "explanation": [...]
            # }
            # =================================================

            jd_match = result["jd_match"]


            # -------------------------------------------------
            # Extract JD match components
            # -------------------------------------------------

            final_score = jd_match["score"]

            confidence = jd_match["confidence"]

            component_scores = (
                jd_match["component_scores"]
            )

            skill_coverage = (
                jd_match["skill_coverage"]
            )

            role_alignment = (
                jd_match["role_alignment"]
            )


            # -------------------------------------------------
            # Store result
            # -------------------------------------------------

            rows.append({

                "Resume":
                    resume_filename,

                "JD":
                    jd_filename,

                "Role":
                    role,

                "Final Score":
                    final_score,

                "Confidence":
                    confidence,

                "Skill Coverage":
                    component_scores[
                        "skill_coverage"
                    ],

                "Embedding Similarity":
                    component_scores[
                        "embedding_similarity"
                    ],

                "TF-IDF Similarity":
                    component_scores[
                        "tfidf_similarity"
                    ],

                "Role Alignment":
                    component_scores[
                        "role_alignment"
                    ],

                "Matched Skills":
                    ", ".join(
                        skill_coverage.get(
                            "matched",
                            []
                        )
                    ),

                "Missing Skills":
                    ", ".join(
                        skill_coverage.get(
                            "missing",
                            []
                        )
                    ),

                "Extra Skills":
                    ", ".join(
                        skill_coverage.get(
                            "extra",
                            []
                        )
                    ),

                "Role Matched Skills":
                    ", ".join(
                        role_alignment.get(
                            "matched_role_skills",
                            []
                        )
                    ),

                "Additional Technologies":
                    ", ".join(
                        role_alignment.get(
                            "additional_technologies",
                            []
                        )
                    ),
            })


            successful_tests += 1

            print(
                f"  ✓ Score: "
                f"{final_score}"
            )


        except Exception as e:

            failed_tests += 1

            print(
                f"  ✗ Failed: "
                f"{resume_filename} "
                f"→ {jd_filename}"
            )

            print(
                f"    Error: {e}"
            )


# ============================================================
# SAVE RESULTS
# ============================================================

df = pd.DataFrame(rows)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 55)
print("JD MATCHING EVALUATION COMPLETE")
print("=" * 55)

print(
    f"Resumes:            {len(resume_files)}"
)

print(
    f"Job Descriptions:   {len(jds)}"
)

print(
    f"Expected tests:     {expected_tests}"
)

print(
    f"Successful tests:   {successful_tests}"
)

print(
    f"Failed tests:       {failed_tests}"
)

print(
    f"Results saved to:"
)

print(
    OUTPUT_FILE
)

print("=" * 55)