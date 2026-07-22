function Badge({ skill, color }) {
  return (
    <span
      className={`px-3 py-2 rounded-full text-sm font-medium ${color}`}
    >
      {skill}
    </span>
  );
}

function RoleAlignment({ roleAlignment }) {

  return (

    <div className="bg-white rounded-2xl shadow-md p-8">

      <h2 className="text-2xl font-bold mb-8">
        Role Alignment
      </h2>

      <div className="mb-8">

        <p className="text-slate-500">

          Target Role

        </p>

        <h3 className="text-3xl font-bold">

          {roleAlignment.role}

        </h3>

      </div>

      <div className="mb-8">

        <p className="text-slate-500 mb-3">

          Matching Role Skills

        </p>

        <div className="flex flex-wrap gap-3">

          {roleAlignment.matched_role_skills.map((skill) => (

            <Badge
              key={skill}
              skill={skill}
              color="bg-green-100 text-green-700"
            />

          ))}

        </div>

      </div>

      <div>

        <p className="text-slate-500 mb-3">

          Suggested Technologies

        </p>

        <div className="flex flex-wrap gap-3">

          {roleAlignment.additional_technologies.map((skill) => (

            <Badge
              key={skill}
              skill={skill}
              color="bg-blue-100 text-blue-700"
            />

          ))}

        </div>

      </div>

    </div>

  );

}

export default RoleAlignment;