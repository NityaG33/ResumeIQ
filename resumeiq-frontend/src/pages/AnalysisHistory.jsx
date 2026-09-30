import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/common/Layout";
import {
    getAnalyses,
    deleteAnalysis,
} from "../services/api";

function AnalysisHistory() {
    const [analyses, setAnalyses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchAnalyses = async () => {
            try {
                const data = await getAnalyses();
                setAnalyses(data);
            } catch (err) {
                setError(
                    err.response?.data?.detail ||
                    "Failed to load analysis history."
                );
            } finally {
                setLoading(false);
            }
        };

        fetchAnalyses();
    }, []);

    const handleDelete = async (analysisId) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this analysis?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteAnalysis(analysisId);

            setAnalyses((prev) =>
                prev.filter(
                    (analysis) => analysis.id !== analysisId
                )
            );
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Failed to delete analysis."
            );
        }
    };

    const getAnalysisTitle = (analysis) => {
        if (analysis.analysis_type === "jd_match") {
            return "Resume-JD Match";
        }

        return "Resume Quality Analysis";
    };

    const getAnalysisDescription = (analysis) => {
        if (analysis.analysis_type === "jd_match") {
            return "Resume compatibility with a target job description";
        }

        return "Resume quality, ATS readiness and improvement insights";
    };

    if (loading) {
        return (
            <Layout>
                <div className="min-h-[70vh] flex items-center justify-center">
                    <p className="text-slate-500">
                        Loading your analysis history...
                    </p>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="bg-slate-50 min-h-[calc(100vh-80px)]">
                <div className="max-w-7xl mx-auto px-6 py-12">

                    {/* Header */}
                    <div className="mb-10">
                        <p className="text-blue-600 font-semibold text-sm uppercase tracking-wide">
                            Your Workspace
                        </p>

                        <h1 className="text-4xl font-bold text-slate-900 mt-2">
                            Analysis History
                        </h1>

                        <p className="text-slate-500 mt-3 max-w-2xl">
                            View and manage your previous ResumeIQ analyses.
                            Your results are securely associated with your account.
                        </p>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">
                            {error}
                        </div>
                    )}

                    {/* Empty State */}
                    {!error && analyses.length === 0 && (
                        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm">

                            <div className="w-16 h-16 mx-auto rounded-full bg-blue-50 flex items-center justify-center">
                                <span className="text-2xl">📊</span>
                            </div>

                            <h2 className="text-xl font-semibold text-slate-900 mt-5">
                                No analyses yet
                            </h2>

                            <p className="text-slate-500 mt-2 max-w-md mx-auto">
                                Run your first resume analysis and your results
                                will appear here.
                            </p>

                            <Link
                                to="/dashboard"
                                className="inline-block mt-6 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
                            >
                                Analyze Resume
                            </Link>
                        </div>
                    )}

                    {/* Analysis List */}
                    {analyses.length > 0 && (
                        <div className="space-y-5">

                            {analyses.map((analysis) => (
                                <div
                                    key={analysis.id}
                                    className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition"
                                >

                                    <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">

                                        {/* Analysis Information */}
                                        <div className="flex-1">

                                            <div className="flex items-center gap-3">
                                                <span
                                                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                                        analysis.analysis_type === "jd_match"
                                                            ? "bg-blue-50 text-blue-600"
                                                            : "bg-purple-50 text-purple-600"
                                                    }`}
                                                >
                                                    {analysis.analysis_type === "jd_match"
                                                        ? "JD MATCH"
                                                        : "RESUME QUALITY"}
                                                </span>

                                                <span className="text-xs text-slate-400">
                                                    {analysis.input_type.toUpperCase()}
                                                </span>
                                            </div>

                                            <h2 className="text-xl font-semibold text-slate-900 mt-3">
                                                {getAnalysisTitle(analysis)}
                                            </h2>

                                            <p className="text-sm text-slate-500 mt-1">
                                                {getAnalysisDescription(analysis)}
                                            </p>

                                            <div className="flex flex-wrap gap-x-6 gap-y-2 mt-4 text-sm text-slate-400">
                                                <span>
                                                    Created{" "}
                                                    {new Date(
                                                        analysis.created_at
                                                    ).toLocaleString()}
                                                </span>

                                                {analysis.input_type === "pdf" && (
                                                    <span>
                                                        Resume:{" "}
                                                        {analysis.resume_filename || "Resume deleted"}
                                                    </span>
                                                )}
                                            </div>

                                        </div>

                                        {/* Actions */}
                                        <div className="flex items-center gap-3">

                                            <Link
                                                to={`/results/${analysis.id}`}
                                                className="px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
                                            >
                                                View Result
                                            </Link>

                                            <button
                                                onClick={() =>
                                                    handleDelete(analysis.id)
                                                }
                                                className="px-5 py-2.5 border border-red-200 text-red-600 font-medium rounded-lg hover:bg-red-50 transition"
                                            >
                                                Delete
                                            </button>

                                        </div>

                                    </div>
                                </div>
                            ))}

                        </div>
                    )}

                </div>
            </div>
        </Layout>
    );
}

export default AnalysisHistory;