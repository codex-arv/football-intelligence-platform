"use client";

import { API_BASE_URL } from "../config/api";
import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import ListPicker from "@/components/ui/ListPicker";
import MatchStatsBasic from "@/components/stats/MatchStatsBasic";
import { useNavigate, useLocation } from "react-router-dom";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";

/* ---------------- CRESTS ---------------- */

const teamNameMap: Record<string, string> = {
  Brighton: "Brighton & Hove Albion",
  Tottenham: "Tottenham Hotspur",
  Liverpool: "Liverpool", // optional, in case API returns something like "Liverpool FC"
  // add more if needed
};

const crestOverrides: Record<string, string> = {
  Liverpool: "/crests/liverpoolcrest.png",
  "Tottenham Hotspur": "/crests/tottenhamcrest.png",
  "Brighton & Hove Albion": "/crests/brightoncrest.png",
};

const displayNameMap: Record<string, string> = {
  "Brighton": "Brighton",
  "Tottenham": "Spurs",
  "Liverpool": "Liverpool",
  "Wolves": "Wolves",
  "Man United": "Manchester United",
  "Man City": "Manchester City",
  "Nott'm Forest": "Nottingham Forest"  // add more mappings if API returns shorter/abbreviated names
};

function getDisplayName(teamName: string) {
  return displayNameMap[teamName] ?? teamName; // fallback to API name if not mapped
}

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

function getCrestSrc(teamName: string) {
  const actualName = teamNameMap[teamName] ?? teamName; // map API name to full name
  if (crestOverrides[actualName]) return crestOverrides[actualName];
  return `/crests/${slugify(actualName)}`;
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
  const statsRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (location.state?.season && location.state?.matchday) {
      setSeason(location.state.season);
      setMatchday(location.state.matchday);
    }
    if (location.state?.selectedMatch) setSelectedMatch(location.state.selectedMatch);
  }, [location.state]);

  const maxMatchday = season === 2025 ? 21 : 38;

  const fetchMatches = async () => {
    if (!season || !matchday) return;

    setLoading(true);
    setMatches([]);
    setSelectedMatch(null);
    setBasicStats(null);

    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/stats/matches?season=${season}&gameweek=${matchday}`);
      if (!res.ok) throw new Error("Failed to load matches");

      const data = await res.json();
      setMatches(data);

      // 👇 scroll ONLY here
      requestAnimationFrame(() => {
        setTimeout(() => {
          if (!statsRef.current) return;

          const yOffset = -80;
          const y =
            statsRef.current.getBoundingClientRect().top +
            window.pageYOffset +
            yOffset;

          window.scrollTo({ top: y });
        }, 0);
      });

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };


  useEffect(() => {
    if (matches.length === 0 || !statsRef.current) return;

    const yOffset = -80; // adjust for navbar height
    const y =
      statsRef.current.getBoundingClientRect().top +
      window.pageYOffset +
      yOffset;

    window.scrollTo({
      top: y,
      behavior: "smooth",
    });
  }, [matches]);

  const selectMatch = async (m: any) => {
    setSelectedMatch(m);
    setBasicStats(null);
    window.scrollTo(0, 0);

    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/stats/match/basic?season=${season}&gameweek=${matchday}&home=${m.HomeTeam}&away=${m.AwayTeam}`
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
      `/statistics/match/players?season=${season}&gameweek=${matchday}&home=${selectedMatch.HomeTeam}&away=${selectedMatch.AwayTeam}`,
      { state: { season, matchday, selectedMatch } }
    );
  };

  useEffect(() => {
    if (!selectedMatch || !season || !matchday) return;
    const fetchStats = async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/api/v1/stats/match/basic?season=${season}&gameweek=${matchday}&home=${selectedMatch.HomeTeam}&away=${selectedMatch.AwayTeam}`
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

      <div className="relative z-10 max-w-6xl mx-auto px-10 pt-28 pb-40 space-y-16 min-h-screen">
        {/* Hero */}
        {!selectedMatch && (
          <motion.section className="text-center space-y-10 animate-fade-in" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="text-5xl sm:text-4xl md:text-6xl font-extrabold uppercase italic bg-gradient-text bg-clip-text text-transparent leading-snug sm:leading-tight md:leading-[1.15] break-words">
              Historical Match and{" "}
              <span className="block leading-[1.35] sm:leading-[1.45]">
                Player Statistics
              </span>
            </h1>
            <p className="text-xl md:text-xl text-white/80 max-w-4xl px-6 sm:px-4 font-lightbold mx-auto text-center">
              Dive deep into Premier League fixtures with detailed match insights and comprehensive player performance data,
              including goals, assists, expected metrics and advanced statistical breakdowns.
            </p>
          </motion.section>
        )}

        {/* Pickers */}
        {!selectedMatch && (
          <motion.section className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
              <ListPicker
                title="SELECT SEASON"
                items={["2024–2025", "2025–2026"]}
                selected={season === 2024 ? "2024–2025" : season === 2025 ? "2025–2026" : null}
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
                items={Array.from({ length: maxMatchday }, (_, i) => `Matchday ${i + 1}`)}
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
                className={`relative px-7 py-3 rounded-full font-bold text-xs uppercase tracking-[0.3em]
                  border border-white/50 text-white hover:shadow-[0_0_8px_rgba(255,255,255,0.6),0_0_18px_rgba(255,255,255,0.4)]
                  hover:border-white/80 overflow-hidden transition-all duration-300
                  ${!season || !matchday || loading ? "opacity-40 cursor-not-allowed pointer-events-none" : "hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.1)] hover:shadow-[0_0_20px_rgba(255,255,255,0.5)]"}`}
              >
                {loading ? "LOADING!" : "VIEW MATCHES"}
              </button>
            </div>
          </motion.section>
        )}

        {/* Match Cards */}
        {!selectedMatch && matches.length > 0 && (
          <motion.section ref={statsRef} className="space-y-8">
            {matches.map((m) => (
              <motion.div
                key={m.match_id}
                layout
                onClick={() => selectMatch(m)}
                whileHover={{ scale: 1.03, boxShadow: "0 0 30px rgba(255, 255, 255, 0.78)" }}
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
                className="cursor-pointer rounded-3xl backdrop-blur-md p-5 flex items-center w-full transition-all duration-100 border border-white/50"
              >
                {/* Desktop */}
                <div className="relative hidden sm:flex items-center w-full">
                  <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 font-bold text-4xl pointer-events-none whitespace-nowrap">
                    {m.FTHG} – {m.FTAG}
                  </div>
                  <div className="flex items-center gap-4 flex-1 pr-24">
                    <img src={getCrestSrc(m.HomeTeam)} className="h-16 w-16 object-contain shrink-0" />
                    <span className="text-xl font-semibold whitespace-nowrap">{getDisplayName(m.HomeTeam)}</span>
                  </div>
                  <div className="flex items-center gap-4 flex-1 justify-end pl-24">
                    <span className="text-xl font-semibold whitespace-nowrap text-right">{getDisplayName(m.AwayTeam)}</span>
                    <img src={getCrestSrc(m.AwayTeam)} className="h-16 w-16 object-contain shrink-0" />
                  </div>
                </div>

                {/* Mobile */}
                <div className="flex sm:hidden items-center justify-between w-full px-4">
                  <img src={getCrestSrc(m.HomeTeam)} className="h-16 w-16 object-contain" />
                  <div className="font-extrabold text-2xl whitespace-nowrap">{m.FTHG} – {m.FTAG}</div>
                  <img src={getCrestSrc(m.AwayTeam)} className="h-16 w-16 object-contain" />
                </div>
              </motion.div>
            ))}
          </motion.section>
        )}

        {/* Selected Match */}
        {selectedMatch && (
          <motion.section className="space-y-12">
            {/* Desktop */}
            <div className="hidden sm:flex items-center justify-center gap-10 text-center">
              <div className="flex flex-col items-center relative">
                <div className="flex items-center gap-4">
                  <button onClick={() => setSelectedMatch(null)} className="transform -translate-x-[165px] px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)] hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] transition-all duration-500">Back to Matches</button>
                  <div className="h-24 w-24 flex items-center justify-center">
                    <img src={getCrestSrc(selectedMatch.HomeTeam)} className="max-h-full max-w-full object-contain" />
                  </div>
                </div>
              </div>
              <div className="text-5xl font-extrabold tracking-wide">{selectedMatch.FTHG} – {selectedMatch.FTAG}</div>
              <div className="flex flex-col items-center relative">
                <div className="flex items-center gap-4">
                  <div className="h-24 w-24 flex items-center justify-center">
                    <img src={getCrestSrc(selectedMatch.AwayTeam)} className="max-h-full max-w-full object-contain" />
                  </div>
                  <button onClick={viewPlayerStats} className="transform translate-x-[148px] px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)] hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] -mr-9 transition-all duration-500">View Player Statistics</button>
                </div>
              </div>
            </div>

            {/* Mobile */}
            <div className="sm:hidden flex flex-col items-center gap-6 text-center">

              {/* Buttons — stacked like PlayerStatistics.tsx */}
              <div className="flex flex-col gap-4 w-full max-w-xs">
                <button
                  onClick={() => setSelectedMatch(null)}
                  className="w-full px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white/50 hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.6)] transition-all duration-300"
                >
                  Back to Matches
                </button>

                <button
                  onClick={viewPlayerStats}
                  className="w-full px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white/50 hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.6)] transition-all duration-300 mb-6"
                >
                  View Player Statistics
                </button>
              </div>

              {/* Crests and Score */}
              <div className="flex items-center justify-center gap-6">
                <img src={getCrestSrc(selectedMatch.HomeTeam)} className="h-16 w-16 object-contain" />
                <div className="text-3xl font-extrabold whitespace-nowrap">{selectedMatch.FTHG} – {selectedMatch.FTAG}</div>
                <img src={getCrestSrc(selectedMatch.AwayTeam)} className="h-16 w-16 object-contain" />
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
