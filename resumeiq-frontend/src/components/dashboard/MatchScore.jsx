function MatchScore({ score, confidence }) {
  const color =
    score >= 80
      ? "text-green-600"
      : score >= 60
      ? "text-yellow-500"
      : "text-red-500";

  const ring =
    score >= 80
      ? "border-green-500"
      : score >= 60
      ? "border-yellow-500"
      : "border-red-500";

  return (
    <div className="bg-white rounded-2xl shadow-md p-10">

      <h2 className="text-2xl font-bold text-center">
        JD Match Score
      </h2>

      <div
        className={`w-48 h-48 mx-auto mt-8 rounded-full border-8 ${ring}
                    flex items-center justify-center`}
      >
        <span className={`text-5xl font-bold ${color}`}>
          {Math.round(score)}%
        </span>
      </div>

      <p className="text-center mt-8 text-lg">

        Confidence:

        <span className="font-semibold ml-2">

          {confidence}

        </span>

      </p>

    </div>
  );
}

export default MatchScore;