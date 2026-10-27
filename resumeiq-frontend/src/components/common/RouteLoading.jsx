
function RouteLoading() {
    const demoUrl = import.meta.env.VITE_DEMO_VIDEO_URL;
    const readmeUrl = import.meta.env.VITE_README_URL;

    return (
        <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4 py-8 text-white">
            <div className="w-full max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-6 text-center shadow-xl sm:p-8">
                {/* Branding */}
                <div className="mb-8 flex items-center justify-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500 text-xl font-bold">
                        R
                    </div>
                    <span className="text-xl font-bold tracking-tight">
                        ResumeIQ
                    </span>
                </div>

                {/* Loading indicator */}
                <div
                    className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full border-4 border-indigo-400/30 border-t-indigo-400"
                    role="status"
                    aria-label="Loading"
                >
                    <span className="text-lg font-bold text-indigo-300">
                        AI
                    </span>
                </div>

                <h1 className="mb-3 text-2xl font-bold tracking-tight">
                    Getting things ready
                </h1>

                <p className="mb-6 text-sm leading-6 text-slate-300">
                    We're checking your session and preparing your
                    ResumeIQ experience.
                </p>

                {/* Status */}
                <div className="mb-3 flex items-center justify-center gap-2 text-sm text-slate-300">
                    <span className="h-2 w-2 rounded-full bg-indigo-400" />
                    Connecting to ResumeIQ
                </div>

                <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-700">
                    <div className="h-full w-1/3 rounded-full bg-indigo-400" />
                </div>

                {/* Free-tier notice */}
                <p className="mt-5 text-xs leading-6 text-slate-400">
                    ResumeIQ runs on free hosting, so the backend may
                    take up to a minute to wake up after inactivity.
                    Thanks for your patience!
                </p>

                {/* Helpful links */}
                {(demoUrl || readmeUrl) && (
                    <div className="mt-6 border-t border-slate-700 pt-5">
                        <p className="mb-3 text-sm text-slate-300">
                            While you wait, explore the project:
                        </p>

                        <div className="flex flex-wrap justify-center gap-4">
                            {demoUrl && (
                                <a
                                    href={demoUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-sm font-semibold text-indigo-300 underline-offset-4 hover:text-indigo-200 hover:underline"
                                >
                                    Watch demo video ↗
                                </a>
                            )}

                            {readmeUrl && (
                                <a
                                    href={readmeUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-sm font-semibold text-indigo-300 underline-offset-4 hover:text-indigo-200 hover:underline"
                                >
                                    Read the README ↗
                                </a>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
}

export default RouteLoading;
