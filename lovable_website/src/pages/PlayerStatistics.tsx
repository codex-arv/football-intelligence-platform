"use client";

import { API_BASE_URL } from "../config/api";
import { useEffect, useState } from "react";
import { useSearchParams, useNavigate, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import PlayerCard from "@/components/stats/PlayerCard";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";

/* ---------------- CRESTS & DISPLAY ---------------- */
const crestOverrides: Record<string, string> = {
  Liverpool: "/crests/liverpoolcrest.png",
  "Tottenham Hotspur": "/crests/tottenhamcrest.png",
  "Brighton & Hove Albion": "/crests/brightoncrest.png",
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

const teamAliases: Record<string, string> = {
  Spurs: "Tottenham",
  "Tottenham Hotspur": "Tottenham",
  Tottenham: "Tottenham",
  "Man Utd": "Man United",
  "Man United": "Man United",
  Wolves: "Wolves",
};

function normalizeTeamName(name: string) {
  return teamAliases[name] ?? name;
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

function getCrestSrc(displayName: string) {
  const dataset = displayToDataset[displayName] ?? displayName;
  return crestOverrides[displayName] ?? `/crests/${slugify(dataset)}`;
}

function displayName(dataset: string) {
  const found = Object.entries(displayToDataset).find(([, v]) => v === dataset);
  return found ? found[0] : dataset;
}

/* ---------------- COMPONENT ---------------- */
export default function MatchPlayerStatistics() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const location = useLocation();

  const navState = location.state as {
    season: number;
    matchday: number;
    selectedMatch: any;
  } | null;

  const season = Number(searchParams.get("season"));
  const gameweek = Number(searchParams.get("gameweek"));
  const home = searchParams.get("home")!;
  const away = searchParams.get("away")!;

  const [players, setPlayers] = useState<any[]>([]);
  const [score, setScore] = useState<{ FTHG: number; FTAG: number } | null>(null);
  const [loading, setLoading] = useState(true);

  const [expandedPlayerId, setExpandedPlayerId] = useState<number | null>(null);

  /* -------- FETCH MATCH SCORE -------- */
  useEffect(() => {
    const fetchMatchScore = async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/api/v1/stats/match/basic?season=${season}&gameweek=${gameweek}&home=${home}&away=${away}`
        );
        if (!res.ok) throw new Error("Failed to load match score");
        const data = await res.json();
        setScore({ FTHG: data.FTHG, FTAG: data.FTAG });
      } catch (err) {
        console.error(err);
      }
    };
    fetchMatchScore();
  }, [season, gameweek, home, away]);

  /* -------- FETCH PLAYERS -------- */
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/api/v1/stats/players?season=${season}&gameweek=${gameweek}&home=${home}&away=${away}`
        );
        if (!res.ok) throw new Error("Failed to load players");
        setPlayers(await res.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlayers();
  }, [season, gameweek, home, away]);

  const homeKey = normalizeTeamName(home);
  const awayKey = normalizeTeamName(away);

  const homePlayers = players.filter((p) => normalizeTeamName(p.name) === homeKey);
  const awayPlayers = players.filter((p) => normalizeTeamName(p.name) === awayKey);

  return (
    <div className="relative min-h-screen overflow-hidden">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-28 space-y-20">

        {/* ===== MATCH HEADER ===== */}
        <motion.section className="space-y-6 sm:space-y-10">

          {/* Desktop Header */}
          <div className="hidden sm:grid grid-cols-3 items-center">
            <div className="flex items-center justify-between">
              <button
                onClick={() => navigate("/statistics", { state: navState ? { season: navState.season, matchday: navState.matchday } : {} })}
                className="transform -translate-x-[-17px] px-6 py-2 rounded-full font-semibold
                  hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)]
                  hover:shadow-[0_0_20px_rgba(255,255,255,0.3)]
                  bg-transparent backdrop-blur-sm border border-white transition-all duration-500"
              >
                Back to Matches
              </button>
              <div className="h-24 w-24 flex transform translate-x-[90px] items-center justify-center">
                <img src={getCrestSrc(displayName(home))} className="max-h-full max-w-full object-contain" />
              </div>
            </div>

            <div className="text-5xl font-extrabold text-center">{score ? `${score.FTHG} – ${score.FTAG}` : "–"}</div>

            <div className="flex items-center justify-between">
              <div className="h-24 w-24 flex transform translate-x-[-90px] items-center justify-center">
                <img src={getCrestSrc(displayName(away))} className="max-h-full max-w-full object-contain" />
              </div>
              <button
                onClick={() => navigate("/statistics", { state: navState })}
                className="px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white
                  hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.9)] transition-all duration-500"
              >
                Back to Match Statistics
              </button>
            </div>
          </div>

          {/* Mobile Header */}
          <div className="sm:hidden flex flex-col items-center gap-6 text-center">
            <div className="flex flex-col gap-4 w-full max-w-xs">
              <button
                onClick={() => navigate("/statistics", { state: navState ? { season: navState.season, matchday: navState.matchday } : {} })}
                className="w-full px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white/50 hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.6)]"
              >
                Back to Matches
              </button>
              <button
                onClick={() => navigate("/statistics", { state: navState })}
                className="w-full px-6 py-2 rounded-full font-semibold bg-transparent backdrop-blur-sm border border-white/50 hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.6)] mb-6"
              >
                Back to Match Statistics
              </button>
            </div>

            <div className="flex items-center justify-center gap-6">
              <img src={getCrestSrc(displayName(home))} className="h-16 w-16 object-contain" />
              <div className="text-3xl font-extrabold">{score ? `${score.FTHG} – ${score.FTAG}` : "–"}</div>
              <img src={getCrestSrc(displayName(away))} className="h-16 w-16 object-contain" />
            </div>
          </div>

          <div className="text-center text-white/85 sm:text-white text-md sm:text-xl italic max-w-3xl mx-auto px-10">
          <p>
            Click on a player card to explore detailed, in-depth performance stats.
          </p>
        </div>

        </motion.section>

        {/* ===== PLAYERS ===== */}
        {loading && <div className="text-center text-white/60">Loading players...</div>}

        {!loading && (
          <motion.section className="max-w-4xl mx-auto space-y-12">

            {/* HOME TEAM */}
            {homePlayers.length > 0 && (
              <div className="space-y-5 sm:space-y-6">
                <h2 className="text-3xl -mt-8 sm:-mt-8 sm:text-4xl text-center sm:text-left font-bold uppercase tracking-[0.005em] bg-gradient-text bg-clip-text text-transparent leading-[1.15]">{displayName(home)}</h2>
                <div className="space-y-5 sm:space-y-6">
                  {homePlayers.map((p) => (
                    <PlayerCard
                      key={p.player_id}
                      player={p}
                      isExpanded={expandedPlayerId === p.player_id}
                      onToggle={() => setExpandedPlayerId(expandedPlayerId === p.player_id ? null : p.player_id)}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* AWAY TEAM */}
            {awayPlayers.length > 0 && (
              <div className="space-y-6">
                <h2 className="text-3xl -mt-6 sm:-mt-0 sm:text-4xl text-center sm:text-left font-bold uppercase tracking-[0.005em] bg-gradient-text bg-clip-text text-transparent leading-[1.15] mt-12">{displayName(away)}</h2>
                <div className="space-y-5 sm:space-y-6">
                  {awayPlayers.map((p) => (
                    <PlayerCard
                      key={p.player_id}
                      player={p}
                      isExpanded={expandedPlayerId === p.player_id}
                      onToggle={() => setExpandedPlayerId(expandedPlayerId === p.player_id ? null : p.player_id)}
                    />
                  ))}
                </div>
              </div>
            )}

          </motion.section>
        )}
      </div>

      <Footer />
    </div>
  );
}
