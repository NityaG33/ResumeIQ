import Layout from "../components/common/Layout";
import Hero from "../components/analysis/Hero";
import Features from "../components/analysis/Features";
import AnalysisForm from "../components/analysis/AnalysisForm";

function Home() {
    return (
        <Layout>
            <Hero />
            <Features />
        </Layout>
    );
}

export default Home;