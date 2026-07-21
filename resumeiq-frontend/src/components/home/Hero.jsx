import { ArrowRight } from "lucide-react";

function Hero() {
  return (
    <section className="bg-linear-to-b from-blue-50 via-white to-slate-50 py-24">
      <div className="max-w-5xl mx-auto px-6 text-center">
        <h1 className="text-6xl font-bold text-slate-900 leading-tight">
          AI-Powered
          <span className="text-blue-600">
            {" "}Resume Intelligence
          </span>
        </h1>
        <p className="mt-8 text-xl text-slate-600 leading-9 max-w-3xl mx-auto">
          Match your resume against any Job Description using
          semantic AI, ATS evaluation, resume quality analysis,
          and explainable recommendations.
        </p>

        <button className="mt-12 bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold flex items-center gap-2 mx-auto transition">
          Analyze Resume
          <ArrowRight size={20} />
        </button>
      </div>
    </section>
  );
}

export default Hero;