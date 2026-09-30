import { useState } from "react";
import { useDropzone } from "react-dropzone";
import {
    UploadCloud,
    FileText,
    CheckCircle,
    Trash2,
    AlertCircle,
    ClipboardPaste,
} from "lucide-react";

function ResumeInput({
    inputMode,
    setInputMode,
    selectedFile,
    setSelectedFile,
    resumeText,
    setResumeText,
}) {
    const [error, setError] = useState("");

    const onDrop = (acceptedFiles, rejectedFiles) => {
        setError("");

        if (rejectedFiles.length > 0) {
            setError("Only PDF files up to 5 MB are allowed.");
            return;
        }

        if (acceptedFiles.length > 0) {
            setSelectedFile(acceptedFiles[0]);
        }
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        multiple: false,
        accept: {
            "application/pdf": [".pdf"],
        },
        maxSize: 5 * 1024 * 1024,
    });

    const removeFile = () => {
        setSelectedFile(null);
        setError("");
    };

    return (
        <div className="mb-8">

            <label className="flex items-center gap-2 text-sm font-semibold text-slate-800 mb-3">
                <FileText size={18} className="text-blue-600" />
                Resume
            </label>

            {/* Input mode toggle */}

            <div className="inline-flex bg-slate-100 p-1 rounded-xl mb-5">

                <button
                    type="button"
                    onClick={() => {
                        setInputMode("upload");
                        setResumeText("");
                    }}
                    className={`
                        flex items-center gap-2
                        px-4 py-2.5
                        rounded-lg
                        text-sm font-medium
                        transition
                        ${
                            inputMode === "upload"
                                ? "bg-white text-blue-600 shadow-sm"
                                : "text-slate-500 hover:text-slate-700"
                        }
                    `}
                >
                    <UploadCloud size={17} />
                    Upload PDF
                </button>

                <button
                    type="button"
                    onClick={() => {
                        setInputMode("paste");
                        removeFile();
                    }}
                    className={`
                        flex items-center gap-2
                        px-4 py-2.5
                        rounded-lg
                        text-sm font-medium
                        transition
                        ${
                            inputMode === "paste"
                                ? "bg-white text-blue-600 shadow-sm"
                                : "text-slate-500 hover:text-slate-700"
                        }
                    `}
                >
                    <ClipboardPaste size={17} />
                    Paste Resume
                </button>

            </div>

            {/* Upload mode */}

            {inputMode === "upload" && (
                <div>

                    {!selectedFile ? (

                        <div
                            {...getRootProps()}
                            className={`
                                border-2
                                border-dashed
                                rounded-2xl
                                p-12
                                text-center
                                cursor-pointer
                                transition
                                ${
                                    isDragActive
                                        ? "border-blue-500 bg-blue-50"
                                        : "border-slate-300 bg-slate-50 hover:border-blue-400 hover:bg-blue-50/40"
                                }
                            `}
                        >

                            <input {...getInputProps()} />

                            <div className="w-14 h-14 mx-auto rounded-2xl bg-blue-100 flex items-center justify-center">
                                <UploadCloud
                                    size={28}
                                    className="text-blue-600"
                                />
                            </div>

                            <h3 className="text-lg font-semibold text-slate-800 mt-5">
                                {isDragActive
                                    ? "Drop your PDF here"
                                    : "Upload your resume"}
                            </h3>

                            <p className="text-slate-500 mt-2">
                                Drag & drop your PDF or click to browse
                            </p>

                            <p className="text-xs text-slate-400 mt-4">
                                PDF only · Maximum size 5 MB
                            </p>

                        </div>

                    ) : (

                        <div className="border border-green-200 rounded-2xl p-5 bg-green-50 flex items-center justify-between">

                            <div className="flex items-center gap-4">

                                <div className="w-11 h-11 rounded-xl bg-green-100 flex items-center justify-center">
                                    <CheckCircle
                                        size={24}
                                        className="text-green-600"
                                    />
                                </div>

                                <div>
                                    <p className="font-semibold text-slate-800 break-all">
                                        {selectedFile.name}
                                    </p>

                                    <p className="text-sm text-slate-500 mt-1">
                                        {(selectedFile.size / 1024).toFixed(1)} KB
                                    </p>
                                </div>

                            </div>

                            <button
                                type="button"
                                onClick={removeFile}
                                className="p-2 text-red-500 hover:bg-red-100 rounded-lg transition"
                            >
                                <Trash2 size={20} />
                            </button>

                        </div>
                    )}

                    {error && (
                        <div className="mt-4 flex items-center gap-2 text-red-600 text-sm">
                            <AlertCircle size={17} />
                            <span>{error}</span>
                        </div>
                    )}

                </div>
            )}

            {/* Paste mode */}

            {inputMode === "paste" && (
                <div>

                    <textarea
                        rows={11}
                        value={resumeText}
                        onChange={(e) => setResumeText(e.target.value)}
                        placeholder="Paste your resume content here..."
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
                        Paste the complete text of your resume for analysis.
                    </p>

                </div>
            )}

        </div>
    );
}

export default ResumeInput;