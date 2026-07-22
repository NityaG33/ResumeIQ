import { useLocation, Navigate } from "react-router-dom";
import Layout from "../components/common/Layout";
import MatchScore from "../components/dashboard/MatchScore";
import ComponentScores from "../components/dashboard/ComponentScores";
import SkillSection from "../components/dashboard/SkillSection";
import ResumeSummary from "../components/dashboard/ResumeSummary";
import StrengthSection from "../components/dashboard/StrengthSection";
import RecommendationSection from "../components/dashboard/RecommendationSection";
import ResumeBreakdown from "../components/dashboard/ResumeBreakdown";
import RoleAlignment from "../components/dashboard/RoleAlignment";

function Results() {
    const location = useLocation();

    const analysis = location.state?.analysis;

    if (!analysis) {
        return <Navigate to="/" replace />;
    }

    return (
        <Layout>
            <div className="max-w-7xl mx-auto py-12">

                <h1 className="text-4xl font-bold mb-8">
                    Resume Analysis
                </h1>

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

                <div className="mt-10">
                    <RoleAlignment
                        roleAlignment={analysis.jd_match.role_alignment}
                    />
                </div>

                <pre className="mt-10 bg-slate-900 text-green-400 p-6 rounded-xl overflow-auto">
                    {JSON.stringify(analysis, null, 2)}
                </pre>

            </div>
        </Layout>
    );
}

export default Results;