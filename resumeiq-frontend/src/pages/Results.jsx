import { useEffect, useState } from "react";
import {
    useLocation,
    useParams,
    Navigate,
} from "react-router-dom";

import Layout from "../components/common/Layout";
import MatchScore from "../components/dashboard/MatchScore";
import ComponentScores from "../components/dashboard/ComponentScores";
import SkillSection from "../components/dashboard/SkillSection";
import ResumeSummary from "../components/dashboard/ResumeSummary";
import StrengthSection from "../components/dashboard/StrengthSection";
import RecommendationSection from "../components/dashboard/RecommendationSection";
import ResumeBreakdown from "../components/dashboard/ResumeBreakdown";
import RoleAlignment from "../components/dashboard/RoleAlignment";

import { getAnalysis } from "../services/api";

function Results() {
    const location = useLocation();
    const { analysisId } = useParams();

    const [analysis, setAnalysis] = useState(
        location.state?.analysis || null
    );

    const [analysisMode, setAnalysisMode] = useState(
        location.state?.analysisMode ||
        (location.state?.analysis?.jd_match ? "match" : "quality")
    );

    const [loading, setLoading] = useState(
        Boolean(analysisId && !location.state?.analysis)
    );

    const [error, setError] = useState("");

    // Fetch saved analysis when opened from History
    useEffect(() => {
        if (!analysisId || analysis) {
            return;
        }

        const fetchAnalysis = async () => {
            try {
                const data = await getAnalysis(analysisId);

                setAnalysis(data.result);

                setAnalysisMode(
                    data.analysis_type === "jd_match"
                        ? "match"
                        : "quality"
                );
            } catch (err) {
                setError(
                    err.response?.data?.detail ||
                    "Failed to load analysis."
                );
            } finally {
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, [analysisId, analysis]);

    // Loading state
    if (loading) {
        return (
            <Layout>
                <div className="max-w-7xl mx-auto py-20 text-center">
                    <p className="text-slate-500">
                        Loading analysis...
                    </p>
                </div>
            </Layout>
        );
    }

    // Error state
    if (error) {
        return (
            <Layout>
                <div className="max-w-7xl mx-auto py-20 text-center">
                    <p className="text-red-600">
                        {error}
                    </p>
                </div>
            </Layout>
        );
    }

    // No analysis available
    if (!analysis) {
        return <Navigate to="/" replace />;
    }

    const isJDMatchMode = analysisMode === "match";

    return (
        <Layout>
            <div className="max-w-7xl mx-auto py-12">

                <h1 className="text-4xl font-bold mb-8">
                    {isJDMatchMode
                        ? "JD Match Analysis"
                        : "Resume Quality Analysis"}
                </h1>

                {isJDMatchMode ? (
                    <>
                        <MatchScore
                            score={analysis.jd_match.score}
                            confidence={analysis.jd_match.confidence}
                        />

                        <div className="mt-10">
                            <ComponentScores
                                scores={analysis.jd_match.component_scores}
                            />
                        </div>

                        <div className="mt-10">
                            <SkillSection
                                skillCoverage={analysis.jd_match.skill_coverage}
                            />
                        </div>

                        <div className="mt-10">
                            <RoleAlignment
                                roleAlignment={analysis.jd_match.role_alignment}
                            />
                        </div>
                    </>
                ) : (
                    <>
                        <div className="mt-10">
                            <ResumeSummary
                                report={analysis.resume_report}
                            />
                        </div>

                        <div className="mt-10">
                            <StrengthSection
                                strengths={analysis.resume_report.strengths}
                            />
                        </div>

                        <div className="mt-10">
                            <RecommendationSection
                                recommendations={analysis.recommendations}
                            />
                        </div>

                        <div className="mt-10">
                            <ResumeBreakdown
                                report={analysis.resume_report}
                            />
                        </div>
                    </>
                )}

                <pre className="mt-10 bg-slate-900 text-green-400 p-6 rounded-xl overflow-auto">
                    {JSON.stringify(analysis, null, 2)}
                </pre>

            </div>
        </Layout>
    );
}

export default Results;