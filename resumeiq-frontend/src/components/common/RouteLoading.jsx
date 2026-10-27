
function RouteLoading() {
    const demoUrl = import.meta.env.VITE_DEMO_VIDEO_URL;
    const readmeUrl = import.meta.env.VITE_README_URL;

    return (
        <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-8 text-slate-900">
            <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm sm:p-8">
                <div className="mb-8 flex items-center justify-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-xl font-bold text-blue-600">
                        R
                    </div>
                    <span className="text-xl font-bold tracking-tight text-slate-900">
                        ResumeIQ
                    </span>
                </div>

                <div
                    className="mx-auto mb-6 h-12 w-12 rounded-full border-4 border-blue-100 border-t-blue-600 motion-safe:animate-spin"
                    role="status"
                    aria-label="Loading"
                />

                <h1 className="mb-3 text-2xl font-bold tracking-tight text-slate-900">
                    Getting things ready
                </h1>

                <div className="mb-3 flex items-center justify-center gap-2 text-sm text-slate-600">
                    <span className="h-2 w-2 rounded-full bg-blue-600" />
                    Connecting to ResumeIQ
                </div>

                <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full w-1/3 rounded-full bg-blue-600 motion-safe:animate-pulse" />
                </div>

                <p className="mt-5 text-xs leading-6 text-slate-500">
                    ResumeIQ runs on free hosting, so the backend may
                    take up to a minute to wake up after inactivity.
                    Thanks for your patience!
                </p>

                {(demoUrl || readmeUrl) && (
                    <div className="mt-6 border-t border-slate-200 pt-5">
                        <p className="mb-3 text-sm text-slate-600">
                            While you wait, explore the project:
                        </p>

                        <div className="flex flex-wrap justify-center gap-4">
                            {demoUrl && (
                                <a
                                    href={demoUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-sm font-semibold text-blue-600 underline-offset-4 hover:text-blue-700 hover:underline"
                                >
                                    Watch demo video ↗
                                </a>
                            )}

                            {readmeUrl && (
                                <a
                                    href={readmeUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-sm font-semibold text-blue-600 underline-offset-4 hover:text-blue-700 hover:underline"
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
