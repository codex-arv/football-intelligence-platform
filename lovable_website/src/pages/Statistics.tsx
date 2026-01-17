"use client";

import { API_BASE_URL } from "../config/api";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import ListPicker from "@/components/ui/ListPicker";
import MatchStatsBasic from "@/components/stats/MatchStatsBasic";
import { useNavigate, useLocation } from "react-router-dom";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";

/* ---------------- CRESTS ---------------- */

const crestOverrides: Record<string, string> = {
  Liverpool: "/crests/liverpoolcrest.png",
  "Tottenham Hotspur": "/crests/tottenhamcrest.png",
  "Brighton & Hove Albion": "/crests/brightoncrest.png"
};

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

function slugify(name: string) {
  return (
    name
      .toLowerCase()
      .replace(/['’]/g, "")
      .replace(/&/g, "and")
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "") + ".svg"
  );
}

function getCrestSrc(displayName: string) {
  const dataset = displayToDataset[displayName] ?? displayName;
  return crestOverrides[displayName] ?? `/crests/${slugify(dataset)}`;
}

function displayName(dataset: string) {
  const found = Object.entries(displayToDataset).find(
    ([, v]) => v === dataset
  );
  return found ? found[0] : dataset;
}

/* ---------------- COMPONENT ---------------- */

const Statistics = () => {
  const [season, setSeason] = useState<number | null>(null);
  const [matchday, setMatchday] = useState<number | null>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [selectedMatch, setSelectedMatch] = useState<any | null>(null);
  const [basicStats, setBasicStats] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.season && location.state?.matchday) {
      setSeason(location.state.season);
      setMatchday(location.state.matchday);
    }

    if (location.state?.selectedMatch) {
      setSelectedMatch(location.state.selectedMatch);
    }
  }, [location.state]);

  const maxMatchday = season === 2025 ? 21 : 38;

  const fetchMatches = async () => {
    if (!season || !matchday) return;

    setLoading(true);
    setMatches([]);
    setSelectedMatch(null);
    setBasicStats(null);

    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/stats/matches?season=${season}&gameweek=${matchday}`
      );
      if (!res.ok) throw new Error("Failed to load matches");
      setMatches(await res.json());
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };


  const selectMatch = async (m: any) => {
    setSelectedMatch(m);
    setBasicStats(null);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });

    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/stats/match/basic` +
          `?season=${season}` +
          `&gameweek=${matchday}` +
          `&home=${m.HomeTeam}` +
          `&away=${m.AwayTeam}`
      );

      if (!res.ok) throw new Error("Failed to load stats");
      setBasicStats(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const viewPlayerStats = () => {
    if (!selectedMatch || !season || !matchday) return;

    navigate(
      `/statistics/match/players?season=${season}&gameweek=${matchday}` +
        `&home=${selectedMatch.HomeTeam}&away=${selectedMatch.AwayTeam}`,
      {
        state: {
          season,
          matchday,
          selectedMatch,
        },
      }
    );
  };

  useEffect(() => {
    if (!selectedMatch || !season || !matchday) return;

    const fetchStats = async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/api/v1/stats/match/basic` +
            `?season=${season}` +
            `&gameweek=${matchday}` +
            `&home=${selectedMatch.HomeTeam}` +
            `&away=${selectedMatch.AwayTeam}`
        );

        if (!res.ok) throw new Error("Failed to load stats");
        setBasicStats(await res.json());
      } catch (err) {
        console.error(err);
      }
    };

    fetchStats();
  }, [selectedMatch, season, matchday]);

  return (
    <div className="relative overflow-hidden">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />
      <div className="relative z-10 max-w-6xl mx-auto px-10 pt-28 pb-40 space-y-24 min-h-screen">
        {!selectedMatch && (
          <>
          <div className="relative left-1/2 -translate-x-1/2 w-screen overflow-visible">
            <motion.section
              className="text-center space-y-6 animate-fade-in"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ animationDelay: "0.2s", opacity: 0 }}
            >
              <h1
                className="
                  text-6xl font-extrabold uppercase italic
                  bg-gradient-text bg-clip-text text-transparent
                  whitespace-nowrap
                  leading-[1.15]
                "
              >
                Historical Match and
              </h1>
              <h1
                className="
                  text-6xl font-extrabold uppercase italic
                  bg-gradient-text bg-clip-text text-transparent
                  whitespace-nowrap
                  leading-[1.15]
                "
              >
                Player Statistics
              </h1>

              <p className="text-xl md:text-xl text-white/80 max-w-4xl font-lightbold mx-auto text-center">
                Dive deep into Premier League fixtures with detailed match insights and comprehensive player performance data,
                including goals, assists, expected metrics and advanced statistical breakdowns.
              </p>
            </motion.section>
          </div>
          </>
        )}

        {!selectedMatch && (
          <motion.section className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              <ListPicker
                title="SELECT SEASON"
                items={["2024–2025", "2025–2026"]}
                selected={
                  season === 2024
                    ? "2024–2025"
                    : season === 2025
                    ? "2025–2026"
                    : null
                }
                onSelect={(value) => {
                  setSeason(value === "2024–2025" ? 2024 : 2025);
                  setMatchday(null);
                  setMatches([]);
                  setSelectedMatch(null);
                  setBasicStats(null);
                }}
              />

              <ListPicker
                title="SELECT MATCHDAY"
                disabled={!season}
                items={Array.from(
                  { length: maxMatchday },
                  (_, i) => `Matchday ${i + 1}`
                )}
                selected={matchday ? `Matchday ${matchday}` : null}
                onSelect={(value) => {
                  setMatchday(Number(value.replace("Matchday ", "")));
                  setMatches([]);
                  setSelectedMatch(null);
                  setBasicStats(null);
                }}
              />
            </div>
            <div className="flex justify-center">
              <button
                onClick={fetchMatches}
                disabled={!season || !matchday || loading}
                className={`
                  relative px-7 py-3 rounded-full font-bold text-xs uppercase tracking-[0.3em]
                     border border-white/50 text-white
                     hover:shadow-[0_0_8px_rgba(255,255,255,0.6),0_0_18px_rgba(255,255,255,0.4)]
                     hover:border-white/80 overflow-hidden transition-all duration-300

                  ${!season || !matchday || loading
                    ? "opacity-40 cursor-not-allowed pointer-events-none"
                    : "hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.1)] hover:shadow-[0_0_20px_rgba(255,255,255,0.5)]"}
                `}
              >
                {loading ? "LOADING!" : "VIEW MATCHES"}
              </button>
            </div>

          </motion.section>
        )}

        {!selectedMatch && matches.length > 0 && (
        <motion.section className="space-y-8">
          {matches.map((m) => (
            <motion.div
              key={m.match_id}
              layout
              onClick={() => selectMatch(m)}
              whileHover={{
                scale: 1.03,
                boxShadow: "0 0 30px rgba(255, 255, 255, 0.78)",
              }}
              transition={{
                type: "spring",
                stiffness: 300,
                damping: 22,
              }}
              className="
                cursor-pointer
                rounded-3xl backdrop-blur-md
                p-5
                flex items-center w-full
                transition-all duration-100
                border border-white/30
              "
            >
              {/* LEFT — HOME */}
              <div className="w-1/3 flex justify-start">
                <div className="flex items-center gap-4">
                  <div className="h-18 w-18 md:h-20 md:w-20 flex items-center justify-center">
                    <img
                      src={getCrestSrc(displayName(m.HomeTeam))}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>
                  <span className="text-xl font-semibold">
                    {displayName(m.HomeTeam)}
                  </span>
                </div>
              </div>

              {/* CENTER — SCORE */}
              <div className="w-1/3 text-4xl font-bold text-center">
                {m.FTHG} – {m.FTAG}
              </div>

              {/* RIGHT — AWAY */}
              <div className="w-1/3 flex justify-end">
                <div className="flex items-center gap-4">
                  <span className="text-xl font-semibold">
                    {displayName(m.AwayTeam)}
                  </span>
                  <div className="h-18 w-18 md:h-20 md:w-20 flex items-center justify-center">
                    <img
                      src={getCrestSrc(displayName(m.AwayTeam))}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.section>
      )}


        {selectedMatch && (
          <motion.section className="space-y-12">
            <div className="flex items-center justify-center gap-10 text-center">
              <div className="flex flex-col items-center relative">
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => setSelectedMatch(null)}
                    className="transform -translate-x-[165px] px-6 py-2 rounded-full font-semibold
                              hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)]
                              hover:shadow-[0_0_20px_rgba(255,255,255,0.3)]
                              bg-transparent backdrop-blur-sm border border-white transition-all duration-500"
                  >
                    Back to Matches
                  </button>

                  <div className="h-24 w-24 flex items-center justify-center">
                    <img
                      src={getCrestSrc(displayName(selectedMatch.HomeTeam))}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>
                </div>
              </div>

              <div className="text-5xl font-extrabold tracking-wide">
                {selectedMatch.FTHG} – {selectedMatch.FTAG}
              </div>

              <div className="flex flex-col items-center relative">
                <div className="flex items-center gap-4">
                  <div className="h-24 w-24 flex items-center justify-center">
                    <img
                      src={getCrestSrc(displayName(selectedMatch.AwayTeam))}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>

                  <button
                    onClick={viewPlayerStats}
                    className="transform translate-x-[148px] px-6 py-2 rounded-full font-semibold
                              hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)]
                              hover:shadow-[0_0_20px_rgba(255,255,255,0.3)]
                              bg-transparent backdrop-blur-sm border border-white transition-all duration-500 -mr-9"
                  >
                    View Player Statistics
                  </button>
                </div>
              </div>
            </div>

            <MatchStatsBasic stats={basicStats} />
          </motion.section>
        )}

      </div>

      <Footer />
    </div>
  );
};

export default Statistics;