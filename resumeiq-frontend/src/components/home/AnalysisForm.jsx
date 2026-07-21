import { useState } from "react";
import ResumeInput from "./ResumeInput";
import JobDescriptionInput from "./JDInput";
import RoleSelector from "./RoleSelector";
import {
    analyzeResumePDF,
    analyzeResumeText,
} from "../../services/api";

function AnalysisForm() {
  const [inputMode, setInputMode] = useState("upload");
  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {

      if (!role) {
          alert("Please select a role.");
          return;
      }

      if (!jobDescription.trim()) {
          alert("Please enter a job description.");
          return;
      }

      try {

          setLoading(true);

          let result;

          if (inputMode === "paste") {

              if (!resumeText.trim()) {
                  alert("Please paste your resume.");
                  return;
              }

              result = await analyzeResumeText({
                  resume_text: resumeText,
                  jd_text: jobDescription,
                  role,
              });

          } else {

              if (!selectedFile) {
                  alert("Please upload a PDF.");
                  return;
              }

              const formData = new FormData();

              formData.append("resume_file", selectedFile);
              formData.append("jd_text", jobDescription);
              formData.append("role", role);

              result = await analyzeResumePDF(formData);

          }

          console.log(result);

      } catch (err) {

          console.error(err);

          alert(
              err.response?.data?.detail ||
              "Analysis failed."
          );

      } finally {

          setLoading(false);

      }
  };

  return (

    <section className="pb-24">

      <div className="max-w-5xl mx-auto bg-white rounded-2xl shadow-lg p-10">

        <h2 className="text-3xl font-bold">
            Analyze Your Resume
        </h2>

        <p className="text-slate-600 mt-2 mb-8">
            Paste your resume and job description below to receive an AI-powered analysis.
        </p>

        {/* Resume */}

        <div className="mb-8">
          <ResumeInput
            inputMode={inputMode}
            setInputMode={setInputMode}
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
            resumeText={resumeText}
            setResumeText={setResumeText}
          />
        </div>

        {/* JD */}

        <JobDescriptionInput
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
        />

        {/* Role */}

        <RoleSelector
            role={role}
            setRole={setRole}
        />

        <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white py-4 rounded-xl text-lg font-semibold transition"
        >
            {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>
    </section>
  );
}

export default AnalysisForm;