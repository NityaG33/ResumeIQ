import { useState } from "react";
import {
    Target,
    Sparkles,
    ShieldCheck,
} from "lucide-react";

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

        // Validation

        if (inputMode === "paste" && !resumeText.trim()) {
            alert("Please paste your resume.");
            return;
        }

        if (inputMode === "upload" && !selectedFile) {
            alert("Please upload a PDF.");
            return;
        }

        if (analysisMode === "match") {

            if (!jobDescription.trim()) {
                alert("Please enter a job description.");
                return;
            }

            if (!role) {
                alert("Please select a role.");
                return;
            }
        }

        try {

            setLoading(true);

            let result;

            // Text input

            if (inputMode === "paste") {

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

            }

            // PDF input

            else {

                const formData = new FormData();

                formData.append(
                    "resume_file",
                    selectedFile
                );

                if (analysisMode === "match") {

                    formData.append(
                        "jd_text",
                        jobDescription
                    );

                    formData.append(
                        "role",
                        role
                    );

                    result = await analyzeResumePDF(
                        formData
                    );

                } else {

                    result = await analyzeResumeQualityPDF(
                        formData
                    );

                }
            }

            navigate("/results", {
                state: {
                    analysis: result,
                    analysisMode,
                },
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

        <section className="pb-20">

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

                {/* Header */}

                <div className="px-8 pt-8 pb-6 border-b border-slate-100">

                    <div className="flex items-center gap-3">

                        <div className="w-11 h-11 rounded-xl bg-blue-100 flex items-center justify-center">
                            <Sparkles
                                size={23}
                                className="text-blue-600"
                            />
                        </div>

                        <div>
                            <h2 className="text-2xl font-bold text-slate-900">
                                Analyze Your Resume
                            </h2>

                            <p className="text-sm text-slate-500 mt-1">
                                Choose an analysis type and provide your resume.
                            </p>
                        </div>

                    </div>

                </div>

                <div className="p-8">

                    {/* Analysis Mode */}

                    <div className="mb-10">

                        <div className="flex items-center gap-2 mb-4">
                            <Target
                                size={18}
                                className="text-blue-600"
                            />

                            <h3 className="text-sm font-semibold text-slate-800">
                                Analysis Type
                            </h3>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                            <button
                                type="button"
                                onClick={() =>
                                    setAnalysisMode("match")
                                }
                                className={`
                                    rounded-xl
                                    border
                                    p-5
                                    text-left
                                    transition
                                    ${
                                        analysisMode === "match"
                                            ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500"
                                            : "border-slate-200 hover:border-blue-300 hover:bg-slate-50"
                                    }
                                `}
                            >

                                <div className="flex items-center justify-between">

                                    <div>
                                        <div className="font-semibold text-slate-900">
                                            JD Match
                                        </div>

                                        <div className="text-sm text-slate-500 mt-1">
                                            Compare your resume against a specific job description.
                                        </div>
                                    </div>

                                    {analysisMode === "match" && (
                                        <div className="w-3 h-3 rounded-full bg-blue-600" />
                                    )}

                                </div>

                            </button>

                            <button
                                type="button"
                                onClick={() =>
                                    setAnalysisMode("quality")
                                }
                                className={`
                                    rounded-xl
                                    border
                                    p-5
                                    text-left
                                    transition
                                    ${
                                        analysisMode === "quality"
                                            ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500"
                                            : "border-slate-200 hover:border-blue-300 hover:bg-slate-50"
                                    }
                                `}
                            >

                                <div className="flex items-center justify-between">

                                    <div>
                                        <div className="font-semibold text-slate-900">
                                            Resume Quality / ATS
                                        </div>

                                        <div className="text-sm text-slate-500 mt-1">
                                            Evaluate structure, ATS readiness and resume quality.
                                        </div>
                                    </div>

                                    {analysisMode === "quality" && (
                                        <div className="w-3 h-3 rounded-full bg-blue-600" />
                                    )}

                                </div>

                            </button>

                        </div>

                    </div>

                    {/* Resume */}

                    <div className="border-t border-slate-100 pt-8">

                        <ResumeInput
                            inputMode={inputMode}
                            setInputMode={setInputMode}
                            selectedFile={selectedFile}
                            setSelectedFile={setSelectedFile}
                            resumeText={resumeText}
                            setResumeText={setResumeText}
                        />

                    </div>

                    {/* JD Match Inputs */}

                    {analysisMode === "match" && (
                        <div className="border-t border-slate-100 pt-8">

                            <JobDescriptionInput
                                jobDescription={jobDescription}
                                setJobDescription={setJobDescription}
                            />

                            <RoleSelector
                                role={role}
                                setRole={setRole}
                            />

                        </div>
                    )}

                    {/* Submit */}

                    <div className="border-t border-slate-100 pt-8">

                        <button
                            onClick={handleAnalyze}
                            disabled={loading}
                            className="
                                w-full
                                bg-blue-600
                                hover:bg-blue-700
                                disabled:bg-blue-300
                                disabled:cursor-not-allowed
                                text-white
                                py-4
                                rounded-xl
                                text-base
                                font-semibold
                                transition
                                shadow-sm
                                hover:shadow-md
                            "
                        >
                            {loading
                                ? "Analyzing your resume..."
                                : analysisMode === "match"
                                    ? "Analyze JD Match"
                                    : "Analyze Resume Quality"
                            }
                        </button>

                        <div className="flex items-center justify-center gap-2 mt-4 text-xs text-slate-400">
                            <ShieldCheck size={15} />
                            Your analysis is processed securely.
                        </div>

                    </div>

                </div>

            </div>

        </section>
    );
}

export default AnalysisForm;