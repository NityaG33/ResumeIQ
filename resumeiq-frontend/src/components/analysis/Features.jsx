import {
    Brain,
    FileSearch,
    BarChart3
} from "lucide-react";

function Features() {

    const features = [
        {
            icon: <Brain size={36} className="text-blue-600" />,
            title: "Semantic Matching",
            description:
                "Advanced NLP compares resumes and job descriptions using semantic understanding instead of simple keyword matching."
        },
        {
            icon: <FileSearch size={36} className="text-green-600" />,
            title: "ATS Analysis",
            description:
                "Evaluate ATS compatibility with transparent scoring and actionable resume improvement suggestions."
        },
        {
            icon: <BarChart3 size={36} className="text-purple-600" />,
            title: "Explainable AI",
            description:
                "Understand every score with skill coverage, embeddings, role alignment and detailed insights."
        }
    ];

    return (
        <section className="py-20 bg-slate-50">

            <div className="max-w-7xl mx-auto px-6">

                <h2 className="text-4xl font-bold text-center mb-14">
                    Why ResumeIQ?
                </h2>

                <div className="grid md:grid-cols-3 gap-8">

                    {features.map((feature, index) => (

                        <div
                            key={index}
                            className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-xl transition duration-300"
                        >
                            {feature.icon}

                            <h3 className="text-2xl font-semibold mt-6">
                                {feature.title}
                            </h3>

                            <p className="text-slate-600 mt-4 leading-7">
                                {feature.description}
                            </p>

                        </div>

                    ))}

                </div>

            </div>

        </section>
    );
}

export default Features;