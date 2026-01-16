"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import TeamPicker from "@/components/ui/TeamPicker";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";


const API_BASE = "http://localhost:5005";

const displayToDataset: Record<string, string> = {
  "Brighton & Hove Albion": "Brighton",
  "Ipswich Town": "Ipswich",
  "Leeds United": "Leeds",
  "Leicester City": "Leicester",
  "Manchester City": "Man City",
  "Manchester United": "Man United",
  "Newcastle United": "Newcastle",
  "Nottingham Forest": "Nott'm Forest",
  "Tottenham Hotspur": "Tottenham",
  "Wolverhampton Wanderers": "Wolves",
};

function datasetName(display: string) {
  return displayToDataset[display] || display;
}

const teamsDisplay = [
  "Arsenal","Aston Villa","Bournemouth","Brentford","Brighton & Hove Albion",
  "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Ipswich Town",
  "Leeds United","Leicester City","Liverpool","Manchester City","Manchester United",
  "Newcastle United","Nottingham Forest","Southampton","Sunderland","Tottenham Hotspur",
  "West Ham","Wolverhampton Wanderers"
];

const teamColors: Record<string, string> = {
  "Arsenal": "#EF0107",
  "Aston Villa": "#670E36",
  "Bournemouth": "#DA291C",
  "Brentford": "#D20000",
  "Brighton & Hove Albion": "#0057B8",
  "Burnley": "#6b1d44ff",
  "Chelsea": "#0c478bff",
  "Crystal Palace": "#143774ff",
  "Everton": "#043fb5ff",
  "Fulham": "#000000",
  "Ipswich Town": "#005DAC",
  "Leeds United": "#f5cb26ff",
  "Leicester City": "#1453d2ff",
  "Liverpool": "#e10b0bff",
  "Manchester City": "#6CABDD",
  "Manchester United": "#e92f00ff",
  "Newcastle United": "#241F20",
  "Nottingham Forest": "#DD0000",
  "Southampton": "#870e13ff",
  "Sunderland": "#d44038ff",
  "Tottenham Hotspur": "#132257",
  "West Ham": "#692031ff",
  "Wolverhampton Wanderers": "#d1990eff"
};

const ProbabilitySegment = ({ probability, teamName, color, isDraw = false }) => {
  const prob = (probability * 100).toFixed(1);
  const pct = parseFloat(prob);
  const minInsideWidth = 12;

  const textColor =
    isDraw ||
    teamName === "Leeds United" ||
    teamName === "Wolverhampton Wanderers" ||
    teamName === "Bournemouth"
      ? "#000"
      : "#fff";

  return (
    <div
      className="relative flex items-center justify-center transition-all duration-500 p-1 font-bold"
      style={{
        width: `${prob}%`,
        minWidth: `${prob}%`,
        backgroundColor: color,
        color: textColor,
        overflow: "visible",
      }}
      title={`${teamName}: ${prob}%`}
    >
      {pct < minInsideWidth && (
        <span
          className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold px-2 py-0.5 rounded-md"
          style={{
            backgroundColor: "rgba(0,0,0,0.7)",
            whiteSpace: "nowrap",
            color: "#fff",
          }}
        >
          {isDraw ? "Draw" : teamName} — {prob}%
        </span>
      )}

      {pct >= minInsideWidth && (
        <div className="flex flex-col items-center leading-none font-bold">
          <span className="text-sm font-bold">{prob}%</span>
          <span className="text-xs hidden sm:block">{isDraw ? "Draw" : teamName}</span>
        </div>
      )}
    </div>
  );
};

const Prediction = () => {
  
  useEffect(() => {
      window.scrollTo(0, 0);
    }, []);

  const [homeTeam, setHomeTeam] = useState("Arsenal");
  const [awayTeam, setAwayTeam] = useState("Chelsea");

  const [predictedHomeTeam, setPredictedHomeTeam] = useState<string | null>(null);
  const [predictedAwayTeam, setPredictedAwayTeam] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState("");
  const [showRawScoreline, setShowRawScoreline] = useState(false);
  const [showRegression, setShowRegression] = useState(false);
  const [showClassification, setShowClassification] = useState(false);

  const handlePredict = async () => {
    
    if (!homeTeam || !awayTeam) return setError("Please select both teams!");
    if (homeTeam === awayTeam) return setError("Teams must be different!");

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/api/v1/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          home_team: datasetName(homeTeam),
          away_team: datasetName(awayTeam),
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Prediction failed");
      }

      const data = await res.json();
      setResult(data);

      setPredictedHomeTeam(homeTeam);
      setPredictedAwayTeam(awayTeam);

    } catch (err: any) {
      setError(err.message || "Server error. Check backend.");
    }

    setLoading(false);
  };

  return (
    <div className="relative overflow-hidden">
    <MatrixBackground />
    <MatrixGradientOverlay />
      {/* Background Animated Gradient (matches About section) */}
      <div
        className="absolute inset-0 opacity-40 animate-gradient-shift"
        style={{
          background:
            "linear-gradient(45deg, rgba(0,0,0,0.6), rgba(0,0,0,0.4), rgba(0,0,0,0.7), rgba(0,0,0,0.5))",
          backgroundSize: "400% 400%",
        }}
      />
      <Navigation />

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-24 space-y-16">

        {/* Title */}
        <motion.section
          className="text-center space-y-2 animate-fade-in"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ animationDelay: "0.2s", opacity: 0 }}
        >
          <h1 className="text-6xl uppercase italic font-bold mb-4 bg-gradient-text bg-clip-text text-transparent">
            Live Match Prediction
          </h1>

          <p className="text-xl md:text-xl text-semibold max-w-4xl mx-auto text-center">
            Select any two teams and let our AI model predict the outcome.
          </p>

          {error && <div className="text-red-400 font-semibold">{error}</div>}
        </motion.section>

        {/* Team Picker + Prediction System */}
        <motion.section
          className="space-y-10 animate-fade-in mb-8 -mt-24 md:-mt-32 lg:-mt-20" // moved the margin here
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ animationDelay: "0.35s", opacity: 0 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            <TeamPicker
              teamsDisplay={teamsDisplay}
              selected={homeTeam}
              otherSelected={awayTeam}
              onSelect={setHomeTeam}
              title="HOME TEAM"
            />
            <TeamPicker
              teamsDisplay={teamsDisplay}
              selected={awayTeam}
              otherSelected={homeTeam}
              onSelect={setAwayTeam}
              title="AWAY TEAM"
            />
          </div>

          <div className="text-center -mt-6 mb-24">
            <button
              onClick={handlePredict}
              disabled={loading}
              className="relative px-7 py-3 rounded-full font-bold text-xs uppercase tracking-[0.3em]
                     border border-white/50 text-white
                     hover:shadow-[0_0_8px_rgba(255,255,255,0.6),0_0_18px_rgba(255,255,255,0.4)]
                     hover:border-white/80 overflow-hidden transition-all duration-300"
            >
              {loading ? "CALCULATING!" : "START PREDICTION"}
            </button>
          </div>



          {/* Results */}
          {result && predictedHomeTeam && predictedAwayTeam && (
            <motion.div
              className="mt-12 pb-10 grid grid-cols-1 gap-6"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <h4 className="text-3xl md:text-4xl font-bold
              tracking-[0.004em] bg-gradient-text bg-clip-text text-transparent text-center pb-2">
                {result.predicted_winner_blended === "Draw"
                  ? "MATCH DRAWN!"
                  : `WINNER: ${result.predicted_winner_blended}`}
              </h4>

              {/* Prediction Bar */}
              <div className="w-full h-18 rounded-xl overflow-hidden shadow-inner flex border border-white/30">
                <ProbabilitySegment
                  probability={result.blended_probabilities.home_win}
                  teamName={predictedHomeTeam}
                  color={teamColors[predictedHomeTeam]}
                />

                <ProbabilitySegment
                  probability={result.blended_probabilities.draw}
                  teamName="Draw"
                  color="#ffffff"
                  isDraw
                />

                <ProbabilitySegment
                  probability={result.blended_probabilities.away_win}
                  teamName={predictedAwayTeam}
                  color={teamColors[predictedAwayTeam]}
                />
              </div>

              {/* Extra Info Buttons */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">

                {/* Raw Scoreline */}
                <div className="flex flex-col items-center">
                  <button
                    onClick={() => setShowRawScoreline(!showRawScoreline)}
                    className="px-6 py-2 text-lg rounded-full font-lightbold border border-white text-white bg-transparent backdrop-blur-sm transition-all duration-500 
                    hover:shadow-[0_0_10px_rgba(255,255,255,0.9)]"
                  >
                    Check out: Raw Scoreline
                  </button>

                  {showRawScoreline && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="mt-2 p-4 bg-transparent backdrop-blur-sm rounded-lg border border-white/0 text-center"
                    >
                      <p className="ml-8 list-disc text-white/90 text-lg font-lightbold">
                        {predictedHomeTeam}{" "}
                        {result.raw_scoreline
                          .split("-")
                          .map((x) => parseFloat(x).toFixed(3))
                          .join(" - ")}{" "}
                        {predictedAwayTeam}
                      </p>
                    </motion.div>
                  )}
                </div>

                {/* Regression Probabilities */}
                <div className="flex flex-col items-center">
                  <button
                    onClick={() => setShowRegression(!showRegression)}
                    className="px-6 py-2 text-lg rounded-full font-lightbold border border-white text-white bg-transparent backdrop-blur-sm transition-all duration-500 
                    hover:shadow-[0_0_10px_rgba(255,255,255,0.9)]"                  >
                    Check out: Regression Probabilities
                  </button>

                  {showRegression && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="mt-2 p-4 bg-transparent backdrop-blur-sm rounded-lg"
                    >
                      <ul className="ml-8 list-disc text-white/80 text-lg font-lightbold">
                        <li>{predictedHomeTeam}: {(result.regression_probabilities.home_win * 100).toFixed(1)}%</li>
                        <li>Draw: {(result.regression_probabilities.draw * 100).toFixed(1)}%</li>
                        <li>{predictedAwayTeam}: {(result.regression_probabilities.away_win * 100).toFixed(1)}%</li>
                      </ul>
                    </motion.div>
                  )}
                </div>

                {/* Classification Probabilities */}
                <div className="flex flex-col items-center">
                  <button
                    onClick={() => setShowClassification(!showClassification)}
                    className="px-6 py-2 text-lg rounded-full font-lightbold border border-white text-white bg-transparent backdrop-blur-sm transition-all duration-500 
                    hover:shadow-[0_0_10px_rgba(255,255,255,0.9)]"                  >
                    Check out: Classification Probabilities
                  </button>

                  {showClassification && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="mt-2 p-4 bg-transparent backdrop-blur-sm rounded-lg"
                    >
                      <ul className="ml-8 list-disc text-white/80 text-lg font-lightbold">
                        <li>{predictedHomeTeam}: {(result.probabilities_original.home_win * 100).toFixed(1)}%</li>
                        <li>Draw: {(result.probabilities_original.draw * 100).toFixed(1)}%</li>
                        <li>{predictedAwayTeam}: {(result.probabilities_original.away_win * 100).toFixed(1)}%</li>
                      </ul>
                    </motion.div>
                  )}
                </div>

              </div>
            </motion.div>
          )}
        </motion.section>
      </div>

      <Footer />
    </div>
  );
};

export default Prediction;