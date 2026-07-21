import Layout from "../components/common/Layout";
import Hero from "../components/home/Hero";
import Features from "../components/home/Features";
import AnalysisForm from "../components/home/AnalysisForm";

function Home() {
    return (
        <Layout>
            <Hero />
            <Features />
            <AnalysisForm />
        </Layout>
    );
}

export default Home;