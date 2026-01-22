import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import { motion } from "framer-motion";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";
import { Cpu, Database, Network, Activity, Info, ExternalLink } from "lucide-react";

export default function PipelinePage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />

      {/* Cinematic gradient veil — SAME as other pages */}
      <div
        className="absolute inset-0 opacity-40 animate-gradient-shift pointer-events-none"
        style={{
          background:
            "linear-gradient(45deg, rgba(0,0,0,0.6), rgba(0,0,0,0.4), rgba(0,0,0,0.7), rgba(0,0,0,0.5))",
          backgroundSize: "400% 400%",
        }}
      />

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-32 space-y-20">

        {/* HEADER */}
        <motion.div
          className="text-center max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-5xl sm:text-7xl md:text-7xl uppercase italic font-extrabold bg-gradient-text bg-clip-text text-transparent mb-12">
            How It Works
          </h1>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed px-2 sm:px-0">
            Our match predictions are generated using a dual-model system trained on Premier League data from the 
            2024 and 2025 seasons. The system blends classification probabilities with regression-based scoreline estimates 
            using dynamically computed weights to account for team quality, match context, and competitive balance.
          </p>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed px-2 sm:px-0">
            <br></br>We processed over two years of granular match statistics, including long-term performance trends, xG/xGA patterns, 
            home–away splits, and contextual modifiers. Each match is treated as an independent data point, enriched with over 150 engineered 
            features derived from a 15-match EWMA to capture long-term form rather than short-term fluctuations.
          </p>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed px-2 sm:px-0">
            <br></br>The prediction engine uses an ensemble structure: the classifier estimates the most likely match outcome (W/D/L), 
            while the regressors simulate expected goals for home and away teams. Outputs are blended using dynamically assigned weights 
            based on elite status, ELO differences and mismatch intensity. Poisson-based scoreline simulation and temperature-scaled sharpening 
            ensure stable yet responsive predictions.
          </p>
        </motion.div>

        {/* STEPS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          <PipelineCard icon={<Database />} title="Data Collection & Normalization" num="01">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md sm:text-lg">
              Historical Premier League match and performance data is aggregated, cleaned, and normalized into a unified timeline 
              to ensure consistent feature extraction and reliable statistical baselines.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Activity />} title="Feature Engineering" num="02">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md sm:text-lg">
              Features are generated using EWMA to capture long-term team trends, home–away contextual modifiers, 
              strength-of-schedule (SoS) adjustments, ELO-based quality scaling and derived momentum indicators reflecting attacking intensity 
              and chance creation.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Cpu />} title="Dual-Model Training Architecture" num="03" full>
            <p className="mb-4 text-md sm:text-lg text-white/80">
              The prediction engine uses complementary learning paths and heterogenous blended machine learning models to balance prediction stability and responsiveness.
            </p>
            <p className="text-white/100 tracking-[0.06em] font-semibold text-md sm:text-lg">Classification Engine</p>
            <p className="text-white/70 mb-4 text-md sm:text-lg">
              An XGBoost classifier estimates probabilities for home win, draw or away win, considering long-term team form and contextual features.
            </p>
            <p className="text-white/100 tracking-[0.06em] font-semibold text-md sm:text-lg">Regression Engines</p>
            <p className="text-white/70 text-md sm:text-lg">
              Two Random Forest regressors independently predict expected goals for each team, enabling realistic scoreline simulation.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Network />} title="Adaptive Prediction Fusion" num="04">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md sm:text-lg">
              Classification and regression outputs are blended using dynamic class weights that adapt to team quality, ELO gaps and match context. 
              Poisson-based scoreline simulation and temperature scaling sharpen probabilities while respecting the underlying statistical evidence.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Info />} title="Model Philosophy" num="05">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md sm:text-lg">
              The model prioritizes long-term trends over short-term anomalies, capturing team “class” and sustainable performance patterns 
              rather than reacting to one-off results. This ensures predictions are statistically sound, robust and reflective of true team quality.
            </p>
          </PipelineCard>
        </div>

        {/* DATA SOURCES */}
        <motion.section
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-5xl mx-auto"
        >
          <div className="relative p-12 rounded-2xl bg-transparent border border-white/50 backdrop-blur-md overflow-hidden">
            <div className="absolute inset-0 opacity-30 pointer-events-none bg-gradient-to-br from-white/5 via-transparent to-transparent" />

            <h2 className="text-3xl sm:text-4xl md:text-4xl font-bold uppercase italic bg-gradient-text bg-clip-text text-transparent mb-6">
              Data Sources & Attribution
            </h2>

            <p className="text-white/80 text-lg leading-relaxed max-w-3xl mb-6">
              All predictions are built on publicly available football data that has been cleaned, transformed and
              integrated into our proprietary modeling pipeline. We acknowledge and credit the original data providers
              below.
            </p>

            <div className="grid md:grid-cols-2 gap-6">
              <SourceCard
                name="Football - Data"
                description="This dataset provides historical match results and core fixture statistics, a multi-decade archive of all Premier League fixtures, 
                serving as the primary ground-truth & data source for our predictive model training & evaluation."
                href="https://www.football-data.co.uk"
              />

              <SourceCard
                name="FPL Core Insights (GitHub)"
                description="A specialized repository providing actual player performance metrics and 
                match insights combining 3 powerful data sources including FPL API,
                providing unparalleled insights into player and team performance."
                href="https://github.com/olbauday/FPL-Core-Insights"
              />
            </div>
          </div>
        </motion.section>
        
      </div>
      <Footer />
    </div>
  );
}

function PipelineCard({ icon, title, num, children, full = false }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className={`${full ? "md:col-span-2" : ""} group relative p-8 sm:p-10 rounded-2xl bg-transparent backdrop-blur-md border border-white/50 hover:border-white/100 hover:shadow-glow-white transition-all duration-500`}
    >
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-4">
          <div className="text-white/50 group-hover:text-white/75 transition">{icon}</div>
          <h3 className="text-xl sm:text-2xl font-bold uppercase italic bg-gradient-text bg-clip-text text-transparent">{title}</h3>
        </div>
        <span className="text-2xl sm:text-3xl font-black italic text-white/50 group-hover:text-white/75 transition">{num}</span>
      </div>
      <div className="text-white/80 leading-relaxed">{children}</div>
    </motion.div>
  );
}

function SourceCard({ name, description, href }: any) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="group relative p-8 rounded-md border border-white/50 bg-transparent hover:border-white hover:shadow-glow-white transition-all duration-300"
    >
      <div className="flex items-start justify-between gap-8">
        <div>
          <h3 className="text-lg sm:text-xl font-semibold text-white mb-2 flex items-center gap-3">
            {name}

            {/* LINK ICON */}
            <span className="relative inline-flex">
              <ExternalLink
                className="
                  w-5 h-5
                  text-white/80 
                  group-hover:text-white 
                  transition-all duration-300
                  group-hover:drop-shadow-[0_0_6px_rgba(255,255,255,0.8)]
                "
              />
            </span>
          </h3>

          <p className="text-md text-white/75 sm:text-white/80 leading-relaxed">
            {description}
          </p>
        </div>
      </div>
    </a>
  );
}

