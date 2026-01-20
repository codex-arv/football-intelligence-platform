import { motion, AnimatePresence } from "framer-motion";

/* ---------------- POSITION → STATS MAP ---------------- */

const POSITION_STATS: Record<string, string[]> = {
  Forward: [
    "total_shots",
    "final_third_passes",
    "shots_on_target",
    "chances_created",
    "xg",
    "touches",
    "xa", 
    "duels_won",
    "xgot",
    "duels_lost",
    "successful_dribbles",
    "minutes_played"
  ],
  Midfielder: [
    "total_shots",
    "touches",
    "xg",
    "recoveries",
    "xa", 
    "tackles",
    "successful_dribbles",
    "duels_won",
    "final_third_passes",
    "duels_lost",
    "chances_created",
    "minutes_played"
  ],
  Defender: [
    "total_shots",
    "fouls_committed",
    "xg",
    "recoveries",
    "xa",
    "tackles",
    "successful_dribbles",
    "duels_won",
    "clearances",
    "duels_lost",
    "touches",
    "minutes_played",
  ],
  Goalkeeper: [
    "total_shots",
    "xg",
    "xa",
    "shots_on_target",
    "successful_dribbles",
    "touches",
    "chances_created",
    "recoveries",
    "clearances",
    "tackles",
    "duels_won",
    "duels_lost",
    "fouls_committed",
    "minutes_played",
  ],
};

const POSITION_ABBR: Record<string, string> = {
  Forward: "FWD",
  Midfielder: "MID",
  Defender: "DEF",
  Goalkeeper: "GK",
};

const STAT_LABELS: Record<string, string> = {
  total_shots: "Total Shots",
  shots_on_target: "Shots on Target",

  xg: "Expected Goals ( xG )",
  xa: "Expected Assists ( xA )",
  xgot: "Expected Goals on Target ( xGOT )",

  successful_dribbles: "Successful Dribbles",
  touches: "Touches",
  touches_opposition_box: "Touches in Opp. Box",

  chances_created: "Chances Created",
  final_third_passes: "Final Third Passes",

  recoveries: "Recoveries",
  clearances: "Clearances",
  tackles: "Tackles",

  duels_won: "Duels Won",
  duels_lost: "Duels Lost",

  fouls_committed: "Fouls Committed",
  minutes_played: "Minutes Played",
};
/* ---------------- COMPONENT ---------------- */

interface PlayerCardProps {
  player: any;
  isExpanded: boolean;
  onToggle: () => void;
}

export default function PlayerCard({ player, isExpanded, onToggle }: PlayerCardProps) {
  const statsToShow = POSITION_STATS[player.position] ?? [];

  // Gap between goals and assists on mobile (in Tailwind units)
  const mobileGoalAssistGap = "gap-4"; // You can tweak this: "gap-2", "gap-4", "gap-6", etc.

  return (
    <motion.div
      layout
      onClick={onToggle}
      whileHover={{
        scale: 1.03,
        boxShadow: "0 0 30px rgba(255, 255, 255, 0.57)",
      }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 22,
      }}
      className="cursor-pointer rounded-2xl border border-white/50 p-4 sm:p-6 backdrop-blur-md transition-all duration-100 bg-transparent space-y-5 sm:space-y-4"
    >
      {/* ===== HEADER (POSITION + NAME) ===== */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
        <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-center sm:text-left">
          <span className="text-sm sm:text-md uppercase tracking-[0.005em] font-bold text-white/70">
            {POSITION_ABBR[player.position] ?? player.position.slice(0, 3).toUpperCase()}
          </span>
          <span className="text-lg sm:text-xl font-semibold tracking-[0.05em]">
            {player.first_name} {player.second_name}
          </span>
        </div>

        {/* Desktop Goals / Assists (unchanged) */}
        <div className="hidden sm:flex flex-row gap-6 text-sn sm:text-xl font-semibold text-white mt-1 sm:mt-0">
          <span>Goals: {player.goals}</span>
          <span>Assists: {player.assists}</span>
        </div>
      </div>

      {/* ===== MOBILE GOALS / ASSISTS ===== */}
      <div className={`flex sm:hidden justify-between text-white ${mobileGoalAssistGap}`}>
        <span className="font-semibold">Goals: {player.goals}</span>
        <span className="font-semibold">Assists: {player.assists}</span>
      </div>

      {/* ===== EXPANDABLE STATS ===== */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            layout
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.35, ease: "easeInOut" }}
            className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2 sm:gap-x-6 sm:gap-y-3 pt-4 sm:pt-5 border-t-2 border-white/50 text-white"
          >
            {statsToShow.map((key) => (
              <div
                key={key}
                className="flex justify-between items-center text-sm sm:text-base font-lightbold"
              >
                <span className="text-white/90">{STAT_LABELS[key] ?? key}</span>
                <span className="font-semibold">{player[key] ?? 0}</span>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}