import { FileText } from "lucide-react";

function JobDescriptionInput({
    jobDescription,
    setJobDescription,
}) {
    return (
        <div className="mb-8">

            <label className="flex items-center gap-2 text-sm font-semibold text-slate-800 mb-3">
                <FileText size={18} className="text-blue-600" />
                Job Description
            </label>

            <textarea
                rows={9}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="
                    w-full
                    bg-slate-50
                    border
                    border-slate-200
                    rounded-xl
                    p-5
                    text-slate-700
                    placeholder:text-slate-400
                    resize-none
                    outline-none
                    transition
                    focus:bg-white
                    focus:border-blue-500
                    focus:ring-2
                    focus:ring-blue-100
                "
            />

            <p className="text-xs text-slate-400 mt-2">
                Include the complete job description for more accurate matching.
            </p>

        </div>
    );
}

export default JobDescriptionInput;