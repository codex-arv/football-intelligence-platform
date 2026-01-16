import React from "react";

interface MatchStatsBasicProps {
  stats: Record<string, any> | null;
}

/* ---------- BASIC MATCH STATS ---------- */
const BASIC_STAT_ROWS = [
  { label: "Possession", home: "home_possession", away: "away_possession", suffix: "%" },
  { label: "Shots", home: "HS", away: "AS" },
  { label: "Shots on Target", home: "HST", away: "AST" },
  { label: "Expected Goals (xG)", home: "home_expected_goals_xg", away: "away_expected_goals_xg", decimals: 2 },
  { label: "Passes", home: "home_passes", away: "away_passes" },

  // already percentages — DO NOT multiply
  { label: "Pass Accuracy", home: "home_accurate_passes_pct", away: "away_accurate_passes_pct", suffix: "%" },
  { label: "Dribble Success", home: "home_successful_dribbles_pct", away: "away_successful_dribbles_pct", suffix: "%" },
  { label: "Tackle Success", home: "home_tackles_won_pct", away: "away_tackles_won_pct", suffix: "%" },

  { label: "Corners", home: "HC", away: "AC" },
  { label: "Fouls", home: "HF", away: "AF" },
  { label: "Yellow Cards", home: "HY", away: "AY" },
  { label: "Red Cards", home: "HR", away: "AR" },
  { label: "Interceptions", home: "home_interceptions", away: "away_interceptions" },
  { label: "Saves", home: "home_keeper_saves", away: "away_keeper_saves" },
  { label: "Duels Won", home: "home_duels_won", away: "away_duels_won" },
];

/* ---------- ROLLING (Last 5) — CIRCLES ---------- */
const CIRCLE_STATS = [
  { label: "Avg Goals For (Last 5)", home: "HT_AvgGF_L5", away: "AT_AvgGF_L5", decimals: 1 },
  { label: "Avg Goals Against (Last 5)", home: "HT_AvgGA_L5", away: "AT_AvgGA_L5", decimals: 1 },
  { label: "Avg Shots (Last 5)", home: "HT_AvgShots_L5", away: "AT_AvgShots_L5", decimals: 1 },

  // fractions → multiply by 100
  { label: "Shot Accuracy (Last 5)", home: "HT_ShotAccuracy_L5", away: "AT_ShotAccuracy_L5", pct: true },
  { label: "Clean Sheets (Last 5)", home: "HT_CS_L5", away: "AT_CS_L5", pct: true },
  { label: "Win Rate (Last 5)", home: "HT_WinRate_L5", away: "AT_WinRate_L5", pct: true },
];

/* ---------- FORMATTER ---------- */
const formatValue = (
  value: any,
  opts?: { pct?: boolean; decimals?: number }
) => {
  if (value === null || value === undefined) return "–";

  if (opts?.pct) return `${Math.round(value * 100)}%`;

  if (opts?.decimals !== undefined)
    return Number(value).toFixed(opts.decimals);

  return Math.round(value).toString();
};

/* ---------- CIRCLE ---------- */
const StatCircle = ({
  value,
  label,
  pct,
  decimals,
}: {
  value: number | null;
  label: string;
  pct?: boolean;
  decimals?: number;
}) => {
  let display = "–";

  if (value !== null && value !== undefined) {
    if (pct) {
      display = `${Math.round(value * 100)}%`;
    } else if (decimals !== undefined) {
      display = Number(value).toFixed(decimals);
    } else {
      display = Math.round(value).toString();
    }
  }

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="h-16 w-16 rounded-full border-2 border-white flex items-center justify-center text-xl font-semibold">
        {display}
      </div>
      <div className="text-base text-white/80 uppercase font-normal text-sm text-center tracking-[0.05em]">
        {label}
      </div>
    </div>
  );
};

const MatchStatsBasic: React.FC<MatchStatsBasicProps> = ({ stats }) => {
  if (!stats) {
    return (
      <div className="text-center py-20 text-white/60 text-xl">
        Loading match statistics…
      </div>
    );
  }

  return (
    <div className="relative">

      {/* ---------- LEFT CIRCLES ---------- */}
      <div className="absolute left-0 top-0 flex flex-col gap-10">
        {CIRCLE_STATS.map((row) => (
          <StatCircle
            key={row.label}
            value={stats[row.home]}
            label={row.label}
            pct={row.pct}
            decimals={row.decimals}
          />
        ))}
      </div>

      {/* ---------- RIGHT CIRCLES ---------- */}
      <div className="absolute right-0 top-0 flex flex-col gap-10">
        {CIRCLE_STATS.map((row) => (
          <StatCircle
            key={row.label}
            value={stats[row.away]}
            label={row.label}
            pct={row.pct}
            decimals={row.decimals}
          />
        ))}
      </div>

      {/* ---------- BASIC STATS ---------- */}
      <div className="grid grid-cols-3 gap-y-6 text-xl px-32">
        {BASIC_STAT_ROWS.map((row) => (
          <React.Fragment key={row.label}>
            <div className="text-right font-semibold">
              {formatValue(stats[row.home], {
                decimals: row.decimals,
              })}
              {row.suffix ?? ""}
            </div>

            <div className="text-center font-lightbold text-white/80 text-md font-normal uppercase">
              {row.label}
            </div>

            <div className="text-left font-semibold">
              {formatValue(stats[row.away], {
                decimals: row.decimals,
              })}
              {row.suffix ?? ""}
            </div>
          </React.Fragment>
        ))}
      </div>

    </div>
  );
};

export default MatchStatsBasic;