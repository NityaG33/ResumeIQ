import { CheckCircle } from "lucide-react";

function StrengthSection({ strengths }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-8">
        Resume Strengths
      </h2>

      <div className="space-y-4">

        {strengths.length === 0 ? (
          <p className="text-slate-500">
            No strengths available.
          </p>
        ) : (
          strengths.map((strength, index) => (
            <div
              key={index}
              className="flex items-start gap-3"
            >
              <CheckCircle
                className="text-green-600 mt-1"
                size={20}
              />

              <p className="text-slate-700">
                {strength}
              </p>
            </div>
          ))
        )}

      </div>

    </div>
  );
}

export default StrengthSection;