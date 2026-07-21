function JobDescriptionInput({
    jobDescription,
    setJobDescription,
}) {
    return (
        <div className="mb-8">

            <label className="text-lg font-semibold text-slate-800">
                Job Description
            </label>

            <textarea
                rows={10}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="
                    w-full
                    mt-4
                    border
                    rounded-2xl
                    p-5
                    resize-none
                    focus:outline-none
                    focus:ring-2
                    focus:ring-blue-500
                "
            />

        </div>
    );
}

export default JobDescriptionInput;