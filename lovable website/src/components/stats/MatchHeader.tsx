import React from "react";

interface MatchHeaderProps {
  match: any;
  getCrestSrc: (team: string) => string; // pass the same function from Statistics.tsx
}

const MatchHeader: React.FC<MatchHeaderProps> = ({ match, getCrestSrc }) => {
  return (
    <div className="flex items-center justify-center gap-6 text-2xl font-bold">
      <div className="flex items-center gap-3">
        <img
          src={getCrestSrc(match.HomeTeam)}
          alt={match.HomeTeam}
          className="w-12 h-12 object-contain"
        />
        {match.HomeTeam}
      </div>

      <span className="text-3xl">
        {match.FTHG} – {match.FTAG}
      </span>

      <div className="flex items-center gap-3">
        {match.AwayTeam}
        <img
          src={getCrestSrc(match.AwayTeam)}
          alt={match.AwayTeam}
          className="w-12 h-12 object-contain"
        />
      </div>
    </div>
  );
};

export default MatchHeader;