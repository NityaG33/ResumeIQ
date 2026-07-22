function SkillBadge({ skill, color }) {
  return (
    <span
      className={`px-3 py-2 rounded-full text-sm font-medium ${color}`}
    >
      {skill}
    </span>
  );
}

function SkillGroup({ title, skills, color }) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">{title}</h3>

      {skills.length === 0 ? (
        <p className="text-slate-500 italic">
          None
        </p>
      ) : (
        <div className="flex flex-wrap gap-3">
          {skills.map((skill) => (
            <SkillBadge
              key={skill}
              skill={skill}
              color={color}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function SkillSection({ skillCoverage }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-8">
        Skill Analysis
      </h2>

      <div className="space-y-10">

        <SkillGroup
          title="✅ Matched Skills"
          skills={skillCoverage.matched}
          color="bg-green-100 text-green-700"
        />

        <SkillGroup
          title="❌ Missing Skills"
          skills={skillCoverage.missing}
          color="bg-red-100 text-red-700"
        />

        <SkillGroup
          title="➕ Additional Skills"
          skills={skillCoverage.extra}
          color="bg-blue-100 text-blue-700"
        />

      </div>

    </div>
  );
}

export default SkillSection;