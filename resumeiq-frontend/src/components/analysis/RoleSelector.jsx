import { Briefcase } from "lucide-react";
import { ROLE_OPTIONS } from "../../utils/constants";

function RoleSelector({ role, setRole }) {
    return (
        <div className="mb-8">

            <label className="flex items-center gap-2 text-sm font-semibold text-slate-800 mb-3">
                <Briefcase size={18} className="text-blue-600" />
                Target Role
            </label>

            <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="
                    w-full
                    px-4
                    py-3.5
                    bg-white
                    border
                    border-slate-200
                    rounded-xl
                    text-slate-700
                    outline-none
                    transition
                    focus:border-blue-500
                    focus:ring-2
                    focus:ring-blue-100
                    cursor-pointer
                "
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