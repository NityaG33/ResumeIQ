import { Link } from "react-router-dom";
import { FileSearch, History } from "lucide-react";
import Layout from "../components/common/Layout";
import AnalysisForm from "../components/analysis/AnalysisForm";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
    const { user } = useAuth();

    return (
        <Layout>
            <div className="bg-slate-50 min-h-full">

                <div className="max-w-7xl mx-auto px-6 py-12">

                    {/* Header */}

                    <div className="mb-10">
                        <p className="text-blue-600 font-semibold text-sm uppercase tracking-wide">
                            ResumeIQ Workspace
                        </p>

                        <h1 className="text-4xl font-bold text-slate-900 mt-2">
                            Analyze Your Resume
                        </h1>

                        <p className="text-slate-500 mt-3 max-w-2xl">
                            Evaluate your resume against a job description
                            or analyze its overall quality and ATS readiness.
                        </p>
                    </div>

                    {/* Quick Actions */}

                    <div className="grid md:grid-cols-2 gap-5 mb-10">

                        <Link
                            to="/analyses"
                            className="bg-white border border-slate-200 rounded-2xl p-6 hover:shadow-md transition"
                        >
                            <History
                                className="text-blue-600"
                                size={28}
                            />

                            <h2 className="text-xl font-semibold mt-4">
                                Analysis History
                            </h2>

                            <p className="text-slate-500 mt-2">
                                View and manage your previous resume analyses.
                            </p>
                        </Link>

                        <div className="bg-white border border-slate-200 rounded-2xl p-6">
                            <FileSearch
                                className="text-purple-600"
                                size={28}
                            />

                            <h2 className="text-xl font-semibold mt-4">
                                Resume Analysis
                            </h2>

                            <p className="text-slate-500 mt-2">
                                Choose between JD matching and resume quality analysis below.
                            </p>
                        </div>

                    </div>

                    {/* Analysis Form */}

                    <AnalysisForm />

                </div>

            </div>
        </Layout>
    );
}

export default Dashboard;