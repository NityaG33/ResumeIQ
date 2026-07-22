import { Lightbulb } from "lucide-react";

function RecommendationList({ title, recommendations }) {
  return (
    <div>

      <h3 className="text-xl font-semibold mb-5">
        {title}
      </h3>

      {recommendations.length === 0 ? (
        <p className="text-slate-500 italic">
          No recommendations.
        </p>
      ) : (
        <div className="space-y-4">

          {recommendations.map((item, index) => (

            <div
              key={index}
              className="flex items-start gap-3"
            >

              <Lightbulb
                className="text-yellow-500 mt-1"
                size={20}
              />

              <p className="text-slate-700">
                {item}
              </p>

            </div>

          ))}

        </div>
      )}

    </div>
  );
}

function RecommendationSection({ recommendations }) {

  return (

    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-8">

        Recommendations

      </h2>

      <div className="space-y-10">

        <RecommendationList
          title="📄 Resume Improvements"
          recommendations={recommendations.resume}
        />

        <RecommendationList
          title="🎯 Job Match Improvements"
          recommendations={recommendations.job_match}
        />

      </div>

    </div>

  );
}

export default RecommendationSection;