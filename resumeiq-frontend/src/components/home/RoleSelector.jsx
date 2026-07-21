function RoleSelector({ role, setRole }) {
    return (
        <div className="mb-8">

            <label className="text-lg font-semibold text-slate-800">
                Target Role
            </label>

            <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="
                    w-full
                    mt-4
                    border
                    rounded-xl
                    p-4
                    focus:ring-2
                    focus:ring-blue-500
                    outline-none
                "
            >
                <option value="">Select a role</option>
                <option value="backend">Backend Developer</option>
                <option value="frontend">Frontend Developer</option>
                <option value="fullstack">Full Stack Developer</option>
                <option value="datascience">Data Scientist</option>
            </select>

        </div>
    );
}

export default RoleSelector;