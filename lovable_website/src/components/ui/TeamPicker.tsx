"use client";

import React, { useEffect, useMemo, useState, useRef } from "react";

type TeamPickerProps = {
  teamsDisplay: string[];
  selected?: string | null;
  otherSelected?: string | null;
  onSelect: (displayName: string) => void;
  title?: string;
};

const crestOverrides: Record<string, string> = {
  "Liverpool": "/crests/liverpoolcrest.png",
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

export default function TeamPicker({
  teamsDisplay,
  selected,
  otherSelected,
  onSelect,
  title = "Choose Team",
}: TeamPickerProps) {
  const teams = useMemo(() => teamsDisplay, [teamsDisplay]);

  const [index, setIndex] = useState(
    selected ? teams.indexOf(selected) : 0
  );
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const wrapperRef = useRef<HTMLDivElement>(null);

  // Default select
  useEffect(() => {
    if (!selected && teams.length > 0) {
      onSelect(teams[0]);
    }
  }, [teams]);

  // FEATURE: Collapse list when clicking anywhere outside the component
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent | TouchEvent) => {
      // 1. Check if the click target exists
      // 2. Check if the click is OUTSIDE the wrapperRef (which contains both button & menu)
      if (
        wrapperRef.current && 
        !wrapperRef.current.contains(event.target as Node)
      ) {
        setOpen(false);
        setSearch("");
      }
    };

    // Use mousedown instead of click for faster response
    // Add touchstart for mobile reliability
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
    };
  }, []);

  const visible = teams[index];
  const dataset = displayToDataset[visible] ?? visible;
  const src = crestOverrides[visible] ?? "/crests/" + slugify(dataset);
  const disabled = otherSelected === visible;

  const filtered = teams.filter((t) =>
    t.toLowerCase().includes(search.toLowerCase())
  );

  const selectTeam = (team: string) => {
    const i = teams.indexOf(team);
    if (i !== -1) {
      setIndex(i);
      onSelect(team);
      setOpen(false);
      setSearch("");
    }
  };

  const prev = () => {
    setOpen(false);
    const i = (index - 1 + teams.length) % teams.length;
    setIndex(i);
    onSelect(teams[i]);
  };

  const next = () => {
    setOpen(false);
    const i = (index + 1) % teams.length;
    setIndex(i);
    onSelect(teams[i]);
  };

  return (
    <div ref={wrapperRef} className="w-full flex flex-col items-center relative">

      <h3 className="text-xl font-semibold mb-4 italic">{title}</h3>

      {/* Trigger */}
      <button
        onClick={() => setOpen((s) => !s)}
        className="mb-3 px-4 py-2 rounded-xl bg-black/25
          hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.4)]
          shadow-[0_0_20px_rgba(255,255,255,0.4)] text-sm"
      >
        Select from List ▼
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute top-20 z-40 w-60 bg-black/70 backdrop-blur-xl border border-white/10 rounded-xl p-3">

          <input
            className="w-full px-3 py-2 rounded-lg bg-white/10 outline-none text-sm"
            placeholder="Search teams..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <div className="mt-2 max-h-56 overflow-y-auto pr-1">
            {filtered.map((team) => {
              const isDisabled = team === otherSelected;
              return (
                <button
                  key={team}
                  disabled={isDisabled}
                  onClick={() => selectTeam(team)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 ${
                    isDisabled
                      ? "bg-white/5 text-white/30 cursor-not-allowed"
                      : "bg-white/10 hover:bg-white/20"
                  }`}
                >
                  {team}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Carousel */}
      <div className="flex items-center gap-6 mt-0">

        <button onClick={prev} className="p-3 bg-transparent rounded-full hover:bg-black/25">❮</button>

        <div className="flex flex-col items-center">
          <button
            disabled={disabled}
            onClick={() => onSelect(visible)}
            className="w-44 h-44 flex items-center justify-center"
          >
            <img
              src={src}
              alt={visible}
              className="w-full h-full object-contain"
              style={{
                padding: 10,
                filter: disabled ? "grayscale(100%) opacity(0.35)" : "none",
              }}
            />
          </button>
          <div className="mt-4 text-center text-xl font-semibold">{visible}</div>
        </div>

        <button onClick={next} className="p-3 bg-transparent rounded-full hover:bg-black/25">❯</button>

      </div>
    </div>
  );
}