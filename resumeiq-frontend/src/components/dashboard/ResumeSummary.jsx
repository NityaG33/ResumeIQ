function StatCard({ label, value }) {
  return (
    <div className="bg-slate-50 rounded-xl p-4 text-center">

      <p className="text-slate-500 text-sm">
        {label}
      </p>

      <h3 className="text-2xl font-bold mt-2">
        {value}
      </h3>

    </div>
  );
}

function ResumeSummary({ report }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-8">
        Resume Quality
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">

        <StatCard
          label="Resume Quality"
          value={`${report.resume_quality_score}%`}
        />

        <StatCard
          label="ATS Score"
          value={`${report.ats_score}%`}
        />

        <StatCard
          label="Grade"
          value={report.grade}
        />

        <StatCard
          label="Resume Length"
          value={report.analysis.resume_length.category}
        />

      </div>

      <div className="mt-8 bg-blue-50 rounded-xl p-6">

        <h3 className="font-semibold text-lg">
          Summary
        </h3>

        <p className="text-slate-700 mt-3 leading-7">
          {report.summary}
        </p>

      </div>

    </div>
  );
}

export default ResumeSummary;