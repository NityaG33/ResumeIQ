import { CheckCircle, XCircle } from "lucide-react";

const sections = [
  {
    key: "structure",
    title: "Structure",
    description: "Sections, organization and resume layout",
  },
  {
    key: "contact",
    title: "Contact Information",
    description: "Email, phone, GitHub and LinkedIn",
  },
  {
    key: "content",
    title: "Content Quality",
    description: "Projects, quantified achievements and readability",
  },
  {
    key: "professional",
    title: "Professional Presence",
    description: "Professional profiles and resume completeness",
  },
];

function ProgressBar({ value, max }) {
  const percentage = (value / max) * 100;

  return (
    <div className="w-full bg-slate-200 rounded-full h-3 mt-3">
      <div
        className="h-3 rounded-full bg-blue-600"
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
}

function ResumeBreakdown({ report }) {
  const breakdown = report.score_breakdown;
  const diagnostics = report.ats_diagnostics || report.analysis;

  return (
    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-2">
        Resume Score Breakdown
      </h2>

      <p className="text-slate-500 mb-8">
        Your resume score is calculated using ATS best practices and resume quality metrics.
      </p>

      <div className="space-y-8">

        {sections.map((section) => {

          const score = breakdown[section.key].score;
          const max = breakdown[section.key].max_score;

          return (

            <div
              key={section.key}
              className="border rounded-xl p-6"
            >

              <div className="flex justify-between items-center">

                <div>

                  <h3 className="text-xl font-semibold">
                    {section.title}
                  </h3>

                  <p className="text-slate-500 mt-1">
                    {section.description}
                  </p>

                </div>

                <div className="text-right">

                  <p className="text-3xl font-bold">

                    {score}

                    <span className="text-slate-500 text-xl">
                      {" "} / {max}
                    </span>

                  </p>

                </div>

              </div>

              <ProgressBar
                value={score}
                max={max}
              />

              <div className="mt-6 space-y-3">

                {section.key === "structure" && (
                  <>
                    <InfoRow
                      ok={diagnostics.sections.skills}
                      text="Skills Section"
                    />

                    <InfoRow
                      ok={diagnostics.sections.projects}
                      text="Projects Section"
                    />

                    <InfoRow
                      ok={diagnostics.sections.education}
                      text="Education Section"
                    />

                    <InfoRow
                      ok={diagnostics.sections.experience}
                      text="Experience Section"
                    />
                  </>
                )}

                {section.key === "contact" && (
                  <>
                    <InfoRow
                      ok={diagnostics.contact_information.email}
                      text="Email Address"
                    />

                    <InfoRow
                      ok={diagnostics.contact_information.phone}
                      text="Phone Number"
                    />

                    <InfoRow
                      ok={diagnostics.contact_information.github}
                      text="GitHub Profile"
                    />

                    <InfoRow
                      ok={diagnostics.contact_information.linkedin}
                      text="LinkedIn Profile"
                    />
                  </>
                )}

                {section.key === "content" && (
                  <>
                    <InfoRow
                      ok={diagnostics.quantified_achievements.present}
                      text={`${diagnostics.quantified_achievements.count} quantified achievements`}
                    />

                    <InfoRow
                      ok={diagnostics.action_verbs.present}
                      text={`${diagnostics.action_verbs.count} strong action verbs`}
                    />

                    <InfoRow
                      ok={diagnostics.bullet_points.present}
                      text={`${diagnostics.bullet_points.count} bullet points`}
                    />

                    <InfoRow
                      ok={diagnostics.resume_length.category === "Good"}
                      text={`Resume Length: ${diagnostics.resume_length.category}`}
                    />
                  </>
                )}

                {section.key === "professional" && (
                  <>
                    <InfoRow
                      ok={diagnostics.contact_information.github}
                      text="GitHub Profile Present"
                    />

                    <InfoRow
                      ok={diagnostics.contact_information.linkedin}
                      text="LinkedIn Profile Present"
                    />
                  </>
                )}

              </div>

            </div>

          );

        })}

      </div>

      {/* ATS Checklist */}

      <div className="mt-12 border-t pt-8">

        <h2 className="text-2xl font-bold mb-2">
          ATS Compatibility Checklist
        </h2>

        <p className="text-slate-500 mb-6">
          These checks determine how well your resume follows ATS-friendly best practices.
        </p>

        <div className="space-y-3">

          <InfoRow
            ok={diagnostics.sections.skills}
            text="Skills section detected"
          />

          <InfoRow
            ok={diagnostics.sections.projects}
            text="Projects section detected"
          />

          <InfoRow
            ok={diagnostics.sections.education}
            text="Education section detected"
          />

          <InfoRow
            ok={diagnostics.sections.experience}
            text="Experience section detected"
          />

          <InfoRow
            ok={diagnostics.contact_information.email}
            text="Email address present"
          />

          <InfoRow
            ok={diagnostics.contact_information.phone}
            text="Phone number present"
          />

          <InfoRow
            ok={diagnostics.resume_length.category === "Good"}
            text="Resume length is optimal"
          />

          <InfoRow
            ok={diagnostics.bullet_points.present}
            text="Uses bullet points"
          />

        </div>

      </div>

    </div>
  );
}

function InfoRow({ ok, text }) {
  return (
    <div className="flex items-center gap-3">

      {ok ? (
        <CheckCircle
          className="text-green-600"
          size={18}
        />
      ) : (
        <XCircle
          className="text-red-500"
          size={18}
        />
      )}

      <p className="text-slate-700">
        {text}
      </p>

    </div>
  );
}

export default ResumeBreakdown;