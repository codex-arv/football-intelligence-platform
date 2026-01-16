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
          <h1 className="text-7xl md:text-7xl uppercase italic font-bold bg-gradient-text bg-clip-text text-transparent mb-12">
            How It Works
          </h1>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed">
            Our match predictions are generated using a dual-model system trained on Premier League data from the 
            2024 and 2025 seasons. The system blends classification probabilities with regression-based scoreline estimates 
            to provide a more stable and realistic forecast.
          </p>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed">
            <br></br>To build this engine, we processed over two years of granular match statistics including 
            concrete match statistics, rolling form trends, xG/xGA patterns, and home–away performance splits. 
            Each match is treated as an independent data point, enriched with over 40 engineered features created from 
            historical form, momentum shifts and chance creation metrics.
          </p>

          <p className="text-lg md:text-xl text-foreground/80 leading-relaxed">
            <br></br>Rather than relying on a single algorithm, the prediction engine uses an ensemble structure where classification 
            and regression models work together. The classifier determines the most likely match outcome (W/D/L), 
            while the regressors estimate expected goals for each club. These outputs are then combined into a blended prediction 
            that rewards probability stability while still responding to meaningful statistical deviations in team performance.
          </p>
        </motion.div>

        {/* STEPS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          <PipelineCard icon={<Database />} title="Data Collection & Cleaning" num="01">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md">
            Historical Premier League matches and player performance data is ingested and normalized to ensure each fixture exists
             on the same analytical timeline.</p>
          </PipelineCard>

          <PipelineCard icon={<Activity />} title="Feature Engineering" num="02">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md">
            Rolling form, xG / xA, home–away splits, squad efficiency, momentum signals and similar other engineered features are encoded into over 40 features.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Cpu />} title="Model Training Pipeline" num="03" full>
            <p className="mb-4 text-lg text-white/70">
              A 75/25 training-validation split ensures strong generalization.
            </p>
            <p className="text-white/100 tracking-[0.06em] font-semibold text-lg">Classification Engine</p>
            <p className="text-white/70 mb-4">XGBoost (eXtreme Gradient Boosting) classification model predicts win / draw / loss probabilities.</p>
            <p className="text-white/100 tracking-[0.06em] font-semibold text-lg">Regression Engines</p>
            <p className="text-white/70">Two Random Forest regression models estimate raw, expected goals for each team.</p>
          </PipelineCard>

          <PipelineCard icon={<Network />} title="Prediction Fusion" num="04">
            <p className="text-white/85 tracking-[0.02em] font-lightbold text-md">
            60% outcome probability weighting blended with 40% scoreline realism for stable, high-confidence forecasts.
            </p>
          </PipelineCard>

          <PipelineCard icon={<Info />} title="Model Philosophy" num="05">
          <p className="text-white/85 tracking-[0.02em] font-lightbold text-md">
            Predictions are driven strictly by structured match data — not injuries, hype, or media narratives.
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

            <h2 className="text-4xl md:text-4xl font-bold uppercase italic bg-gradient-text bg-clip-text text-transparent mb-6">
              Data Sources & Attribution
            </h2>

            <p className="text-white/90 leading-relaxed max-w-3xl mb-6">
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
      className={`${full ? "md:col-span-2" : ""} group relative p-10 rounded-2xl bg-transparent backdrop-blur-md border border-white/50 hover:border-white/100 hover:shadow-glow-white transition-all duration-500`}
    >
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <div className="text-white/35 group-hover:text-white/70 transition">{icon}</div>
          <h3 className="text-2xl font-bold uppercase italic bg-gradient-text bg-clip-text text-transparent">{title}</h3>
        </div>
        <span className="text-3xl font-black italic text-white/30 group-hover:text-white/60 transition">{num}</span>
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
          <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-3">
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

          <p className="text-md text-white/60 leading-relaxed">
            {description}
          </p>
        </div>
      </div>
    </a>
  );
}

