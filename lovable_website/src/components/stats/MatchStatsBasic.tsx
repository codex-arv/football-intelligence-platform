import React from "react";

interface MatchStatsBasicProps {
  stats: Record<string, any> | null;
}

/* ---------- BASIC MATCH STATS ---------- */
const BASIC_STAT_ROWS = [
  { label: "Possession", home: "home_possession", away: "away_possession", suffix: "%" },
  { label: "Shots", home: "HS", away: "AS" },
  { label: "Shots on Target", home: "HST", away: "AST" },
  { label: "Expected Goals", home: "home_expected_goals_xg", away: "away_expected_goals_xg", decimals: 2 },
  { label: "Passes", home: "home_passes", away: "away_passes" },
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

/* ---------- ROLLING STATS ---------- */
const CIRCLE_STATS = [
  { label: "Avg Goals For (LAST 5)", home: "HT_AvgGF_L5", away: "AT_AvgGF_L5", decimals: 1 },
  { label: "Avg Goals Against (LAST 5)", home: "HT_AvgGA_L5", away: "AT_AvgGA_L5", decimals: 1 },
  { label: "Avg Shots (LAST 5)", home: "HT_AvgShots_L5", away: "AT_AvgShots_L5", decimals: 1 },
  { label: "Shot Accuracy (LAST 5)", home: "HT_ShotAccuracy_L5", away: "AT_ShotAccuracy_L5", pct: true },
  { label: "Clean Sheets (LAST 5)", home: "HT_CS_L5", away: "AT_CS_L5", pct: true },
  { label: "Win Rate (LAST 5)", home: "HT_WinRate_L5", away: "AT_WinRate_L5", pct: true },
];

const formatValue = (value: any, opts?: { pct?: boolean; decimals?: number }) => {
  if (value === null || value === undefined) return "–";
  if (opts?.pct) return `${Math.round(value * 100)}%`;
  if (opts?.decimals !== undefined) return Number(value).toFixed(opts.decimals);
  return Math.round(value).toString();
};

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
}) => (
  <div className="flex flex-col items-center gap-2 min-w-[72px]">
    <div className="h-14 w-14 sm:h-16 sm:w-16 rounded-full border-2 border-white/75 flex items-center justify-center text-md sm:text-xl font-semibold">
      {formatValue(value, { pct, decimals })}
    </div>
    <div className="text-sm sm:text-md uppercase text-white/70 sm:text-white/80 text-center tracking-wide">
      {label}
    </div>
  </div>
);

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

      {/* ===================== DESKTOP (UNCHANGED) ===================== */}
      <div className="hidden sm:block">

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

        <div className="grid grid-cols-3 gap-y-6 text-xl px-32">
          {BASIC_STAT_ROWS.map((row) => (
            <React.Fragment key={row.label}>
              <div className="text-right text-xl font-semibold">
                {formatValue(stats[row.home], row)}
              </div>
              <div className="text-center uppercase text-white/80 text-md">
                {row.label}
              </div>
              <div className="text-left text-xl font-semibold">
                {formatValue(stats[row.away], row)}
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* ===================== MOBILE (NEW) ===================== */}
      <div className="sm:hidden space-y-10">

        {/* ===================== MOBILE (new desktop-like layout) ===================== */}
        <div className="sm:hidden grid grid-cols-[1fr_auto_1fr] gap-x-8 gap-y-6 text-md px-4">
          {BASIC_STAT_ROWS.map((row) => (
            <React.Fragment key={row.label}>
              <div className="text-right text-xl text-white/90 font-semibold">
                {formatValue(stats[row.home], row)}
              </div>
              <div className="text-center uppercase text-white/75 text-md">
                {row.label}
              </div>
              <div className="text-left text-xl text-white/90 font-semibold">
                {formatValue(stats[row.away], row)}
              </div>
            </React.Fragment>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-x-4 gap-y-6 px-4">
          {CIRCLE_STATS.map((row) => (
            <React.Fragment key={row.label}>
              <StatCircle
                value={stats[row.home]}
                label={row.label}
                pct={row.pct}
                decimals={row.decimals}
              />
              <StatCircle
                value={stats[row.away]}
                label={row.label}
                pct={row.pct}
                decimals={row.decimals}
              />
            </React.Fragment>
          ))}
        </div>
      </div>

    </div>
  );
};

export default MatchStatsBasic;