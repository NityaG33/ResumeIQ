function ScoreCard({ title, score }) {

    const color =
        score >= 80
            ? "bg-green-100 text-green-700"
            : score >= 60
            ? "bg-yellow-100 text-yellow-700"
            : "bg-red-100 text-red-700";

    return (

        <div className="bg-white rounded-2xl shadow-md p-6">

            <h3 className="text-slate-500 text-sm">

                {title}

            </h3>

            <div className={`mt-4 text-3xl font-bold ${color} inline-block px-4 py-2 rounded-xl`}>

                {score.toFixed(1)}%

            </div>

        </div>

    );

}

function ComponentScores({ scores }) {

    return (

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">

            <ScoreCard
                title="Skill Coverage"
                score={scores.skill_coverage}
            />

            <ScoreCard
                title="Embedding"
                score={scores.embedding_similarity}
            />

            <ScoreCard
                title="TF-IDF"
                score={scores.tfidf_similarity}
            />

            <ScoreCard
                title="Role Alignment"
                score={scores.role_alignment}
            />

        </div>

    );

}

export default ComponentScores;