import { useState } from "react";
import ResumeInput from "./ResumeInput";
import JobDescriptionInput from "./JDInput";
import RoleSelector from "./RoleSelector";
import {
    analyzeResumePDF,
    analyzeResumeText,
    analyzeResumeQualityPDF,
    analyzeResumeQualityText,
} from "../../services/api";
import { useNavigate } from "react-router-dom";

function AnalysisForm() {
  const [inputMode, setInputMode] = useState("upload");
  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [role, setRole] = useState("");
  const [analysisMode, setAnalysisMode] = useState("match");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleAnalyze = async () => {

      if (analysisMode === "match") {
          if (!role) {
              alert("Please select a role.");
              return;
          }

          if (!jobDescription.trim()) {
              alert("Please enter a job description.");
              return;
          }
      }

      try {

          setLoading(true);

          let result;

          if (inputMode === "paste") {

              if (!resumeText.trim()) {
                  alert("Please paste your resume.");
                  return;
              }

              if (analysisMode === "match") {
                  result = await analyzeResumeText({
                      resume_text: resumeText,
                      jd_text: jobDescription,
                      role,
                  });
              } else {
                  result = await analyzeResumeQualityText({
                      resume_text: resumeText,
                  });
              }

          } else {

              if (!selectedFile) {
                  alert("Please upload a PDF.");
                  return;
              }

              const formData = new FormData();
              formData.append("resume_file", selectedFile);

              if (analysisMode === "match") {
                  formData.append("jd_text", jobDescription);
                  formData.append("role", role);
                  result = await analyzeResumePDF(formData);
              } else {
                  result = await analyzeResumeQualityPDF(formData);
              }

          }

          navigate("/results", {
            state: {
              analysis: result,
              analysisMode,
            }
          });

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
            Choose whether you want a JD-to-resume match or a standalone resume quality and ATS score.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <button
            type="button"
            onClick={() => setAnalysisMode("match")}
            className={`rounded-2xl border p-5 text-left transition ${
              analysisMode === "match"
                ? "bg-blue-600 text-white border-blue-600 shadow-lg"
                : "bg-white text-slate-700 border-slate-200 hover:border-blue-500 hover:shadow-md"
            }`}
          >
            <div className="text-lg font-semibold">JD Match</div>
            <div className={`mt-2 text-sm ${analysisMode === "match" ? "text-blue-100" : "text-slate-500"}`}>
              Compare your resume against a job description and role profile.
            </div>
          </button>

          <button
            type="button"
            onClick={() => setAnalysisMode("quality")}
            className={`rounded-2xl border p-5 text-left transition ${
              analysisMode === "quality"
                ? "bg-blue-600 text-white border-blue-600 shadow-lg"
                : "bg-white text-slate-700 border-slate-200 hover:border-blue-500 hover:shadow-md"
            }`}
          >
            <div className="text-lg font-semibold">Resume Quality / ATS</div>
            <div className={`mt-2 text-sm ${analysisMode === "quality" ? "text-blue-100" : "text-slate-500"}`}>
              Check resume structure, ATS friendliness, and quality without a JD.
            </div>
          </button>
        </div>

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

        {analysisMode === "match" && (
          <>
            <JobDescriptionInput
                jobDescription={jobDescription}
                setJobDescription={setJobDescription}
            />

            <RoleSelector
                role={role}
                setRole={setRole}
            />
          </>
        )}

        <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white py-4 rounded-xl text-lg font-semibold transition"
        >
            {loading
              ? "Analyzing..."
              : analysisMode === "match"
                ? "Analyze JD Match"
                : "Analyze Resume Quality"}
        </button>
      </div>
    </section>
  );
}

export default AnalysisForm;