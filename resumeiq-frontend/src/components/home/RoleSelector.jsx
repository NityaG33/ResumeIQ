import { ROLE_OPTIONS } from "../../utils/constants";

function RoleSelector({ role, setRole }) {
    return (
        <div className="mb-8">

            <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="..."
            >
            <option value="">Select a role</option>

            {ROLE_OPTIONS.map((roleOption) => (
                <option
                key={roleOption.value}
                value={roleOption.value}
                >
                {roleOption.label}
                </option>
            ))}
            </select>

        </div>
    );
}

export default RoleSelector;