"use client";

import { useRef, useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import TeamPicker from "@/components/ui/TeamPicker";
import ExpandableText from "@/components/ui/expandableText";
import { Trophy, MapPin, Users, Calendar, Shield, User } from "lucide-react";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";

/* ---------------- DATA & UTILS ---------------- */
const teamsDisplay = [
  "Arsenal","Aston Villa","Bournemouth","Brentford","Brighton & Hove Albion",
  "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Ipswich Town",
  "Leeds United","Leicester City","Liverpool","Manchester City","Manchester United",
  "Newcastle United","Nottingham Forest","Southampton","Sunderland",
  "Tottenham Hotspur","West Ham","Wolverhampton Wanderers"
];

const crestOverrides: Record<string, string> = {
  Liverpool: "/crests/liverpoolcrest.png",
  "Tottenham Hotspur": "/crests/tottenhamcrest.png",
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

const CLUB_MAP: Record<string, {
  json: string;
  crest: string;
  stadium: string;
  crestExt?: "png" | "svg";
}> = {
  Arsenal: {
    json: "arsenal",
    crest: "arsenal",
    stadium: "arsenal"
  },
  "Aston Villa": {
    json: "astonvilla",
    crest: "aston_villa",
    stadium: "astonvilla"
  },
  "Leeds United": {
    json: "leedsunited",
    crest: "leeds",
    stadium: "leedsunited"
  },
  Bournemouth: {
    json: "bournemouth",
    crest: "bournemouth",
    stadium: "bournemouth"
  },
  "Brighton & Hove Albion": {
    json: "brightonhovealbion",
    crest: "brightoncrest",
    stadium: "brightonhovealbion",
    crestExt: "png"
  },
  "Manchester United": {
    json: "manchesterunited",
    crest: "man_united",
    stadium: "manchesterunited"
  },
  "Manchester City": {
    json: "manchestercity",
    crest: "man_city",
    stadium: "manchestercity"
  },
  "Wolverhampton Wanderers": {
    json: "wolverhamptonwanderers",
    crest: "wolves",
    stadium: "wolverhamptonwanderers"
  },
  "Nottingham Forest": {
    json: "nottinghamforest",
    crest: "nottm_forest",
    stadium: "nottinghamforest"
  },
  "Crystal Palace": {
    json: "crystalpalace",
    crest: "crystal_palace",
    stadium: "crystalpalace"
  },
  "Ipswich Town": {
    json: "ipswichtown",
    crest: "ipswich",
    stadium: "ipswichtown"
  },
  "Tottenham Hotspur": {
    json: "tottenhamhotspur",
    crest: "tottenhamcrest",
    stadium: "tottenhamhotspur",
    crestExt: "png"
  },
  "Leicester City":{
    json: "leicestercity",
    crest: "leicester",
    stadium: "leicestercity"
  },
  "West Ham": {
    json: "westham",
    crest: "west_ham",
    stadium: "westham"
  },
  "Newcastle United": {
    json: "newcastleunited",
    crest: "newcastle",
    stadium: "newcastleunited"
  },
  "Fulham": {
    json: "fulham",
    crest: "fulham",
    stadium: "fulham"
  },
  "Chelsea": {
    json: "chelsea",
    crest: "chelsea",
    stadium: "chelsea"
  },
  "Everton": {
    json: "everton",
    crest: "everton",
    stadium: "everton"
  },
  "Liverpool": {
    json: "liverpool",
    crest: "liverpoolcrest",
    stadium: "liverpool",
    crestExt: "png"
  },
  "Brentford": {
    json: "brentford",
    crest: "brentford",
    stadium: "brentford"
  },
  "Burnley": {
    json: "burnley",
    crest: "burnley",
    stadium: "burnley"
  },
  "Southampton": {
    json: "southampton",
    crest: "southampton",
    stadium: "southampton"
  },
  "Sunderland": {
    json: "sunderland",
    crest: "sunderland",
    stadium: "sunderland"
  }
};


function getClubAssets(club: string) {
  return CLUB_MAP[club] || null;
}

const clubDataFiles = import.meta.glob("../data/clubs/*.json", { eager: true });

/* ---------------- REFINED RIVAL CREST ---------------- */
function RivalCrest({ club }: { club: string }) {
  const [imgError, setImgError] = useState(false);

  const assets = getClubAssets(club);

  // If we don't have this club at all → show fallback
  if (!assets || imgError) {
    return (
      <div className="flex flex-col items-center gap-2 w-24 shrink-0">
        <div
          className="w-16 h-16 flex items-center justify-center
                     rounded-full bg-white/10 border border-white/20
                     text-white/60 text-xl"
        >
          ⚽
        </div>

        <span className="text-sm text-center text-white/85 font-semibold leading-tight">
          {club}
        </span>
      </div>
    );
  }

  const ext = assets.crestExt || "svg";

  return (
    <div className="flex flex-col items-center gap-2 w-24 shrink-0">
      <img
        src={`/crests/${assets.crest}.${ext}`}
        alt={club}
        onError={() => setImgError(true)}
        className="w-16 h-16 object-contain"
      />

      <span className="text-sm text-center text-white/85 font-semibold leading-tight">
        {club}
      </span>
    </div>
  );
}


export default function KnowYourClubs() {
  const stadiumRef = useRef<HTMLElement | null>(null);
  const [selectedClub, setSelectedClub] = useState<string | null>(null);
  const [clubData, setClubData] = useState<any | null>(null);
  const loadClubData = (club: string) => {
  const assets = getClubAssets(club);
  if (!assets) return;
  const key = `../data/clubs/${assets.json}.json`;
  const file = clubDataFiles[key] as any;
  setClubData(file ? file.default : null);
};



  useEffect(() => {
    if (!clubData || !stadiumRef.current) return;

    const img = stadiumRef.current.querySelector("img");
    if (!img) return;

    const SCROLL_OFFSET = 48;   // ← tweak this

    const scroll = () => {
      const y =
        stadiumRef.current!.getBoundingClientRect().top +
        window.scrollY -
        SCROLL_OFFSET;

      window.scrollTo({ top: y, behavior: "smooth" });
    };

    if (img.complete) {
      scroll();
    } else {
      img.onload = scroll;
    }
  }, [clubData]);



   return (
    <div className="relative min-h-screen overflow-x-hidden">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />
      {/* ---------------- TOP GRADIENT CONTENT ---------------- */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 pt-28 pb-20 space-y-12 sm:space-y-8">

        {/* Header */}
        <motion.div
          className="text-center space-y-4"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-5xl leading-[1.2] sm:text-6xl font-extrabold uppercase italic bg-gradient-text bg-clip-text text-transparent">
            Hall of Clubs
          </h1>
          <p className="sm:leading-[2.5] text-lg sm:text-xl px-7 sm:px-0 font-lightbold text-white/80 max-w-3xl mx-auto">
            Explore Premier League clubs in depth — history, identity, achievements and legacy.
          </p>
        </motion.div>

        {/* Team Picker */}
        <div className="max-w-xl mx-auto -mt-6">
          <TeamPicker
            teamsDisplay={teamsDisplay}
            selected={selectedClub}
            otherSelected={null}
            onSelect={(club) => {
              setSelectedClub(club);
              setClubData(null);
            }}
            title="SELECT CLUB"
          />

          {/* ENTER BUTTON */}
          <div className="text-center">
            <button
              disabled={!selectedClub}
              onClick={() => loadClubData(selectedClub!)}
              className="
                relative px-7 py-3 rounded-full font-bold text-xs uppercase tracking-[0.3em]
                     border border-white/50 text-white mt-6
                     hover:shadow-[0_0_8px_rgba(255,255,255,0.6),0_0_18px_rgba(255,255,255,0.4)]
                     hover:border-white/80 overflow-hidden transition-all duration-300
                disabled:opacity-40
                disabled:cursor-not-allowed
              "
            >
              Enter Club
            </button>
          </div>
        </div>
      </div>

      {/* ---------------- STADIUM IMMERSION ---------------- */}
      <AnimatePresence>
        {clubData && selectedClub && (
          <motion.section
            ref={stadiumRef}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative w-full h-[90vh] sm:h-[95vh] overflow-hidden border-y border-white/10"
          >
            <div className="absolute inset-0 z-10 bg-gradient-to-b from-[#050505] via-transparent to-[#050505]" />
            <div className="absolute inset-0 z-10 bg-black/40" />
            <motion.img
              initial={{ scale: 1.3 }}
              animate={{ scale: 1 }}
              transition={{ duration: 1.2 }}
              src={`/assets/stadiums/${getClubAssets(selectedClub).stadium}.jpg`}
              style={{ filter: "brightness(1.15) contrast(1.3)" }}
              alt={clubData["Home Stadium"]?.Name}
              className="absolute inset-0 w-full h-full object-cover object-center bg-gradient-hero"
            />
            <div className="relative z-20 h-full flex flex-col justify-end max-w-6xl mx-auto px-8 pb-20">
              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }}>
                <h2 className="
                text-4xl sm:text-6xl md:text-7xl
                text-white/80 font-black uppercase
                tracking-tight
                leading-tight sm:leading-[0.8]
                mb-4 sm:mb-6
                break-words
              ">
                  {clubData["Club Name"]}
                </h2>
                <div className="flex flex-wrap items-center gap-6">
                   <div className="flex items-center gap-2 text-white/60">
                     <MapPin className="w-5 h-5" />
                     <span className="text-md sm:text-lg uppercase tracking-widest font-bold">{clubData["Home Stadium"]?.Name}</span>
                   </div>
                   <div className="h-4 w-[1px] bg-white/20 hidden md:block" />
                   <div className="flex items-center gap-2 text-white/60">
                     <Users className="w-5 h-5" />
                     <span className="text-md sm:text-lg uppercase tracking-widest font-bold">{clubData["Home Stadium"]?.Capacity?.toLocaleString()} Capacity</span>
                   </div>
                </div>
              </motion.div>
            </div>
          </motion.section>
        )}
      </AnimatePresence>

      {/* ---------------- MAIN CONTENT ---------------- */}
      <main className="relative z-10 max-w-6xl mx-auto px-6 py-32">
        {clubData && (
          <div className="space-y-40">
            
            {/* GRID INFO CARDS */}
            <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-12 gap-x-16">
              {[
                { label: "Full Name", value: clubData["Full Official Name"], icon: Shield },
                { label: "Founded", value: clubData["Founded Year"], icon: Calendar },
                { label: "Manager", value: clubData["Current Manager"], icon: User },
                { label: "Location", value: clubData["Location (City, Country)"], icon: MapPin },
                { label: "Motto", value: clubData["Motto"], icon: Trophy },
                { label: "Nicknames", value: clubData["Nickname(s)"]?.join(", "), icon: Users },
              ].map(
                (item, i) =>
                  item.value && (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: i * 0.1 }}
                      className="group"
                    >
                      <div className="flex items-center gap-3 mb-3 text-white transition-colors">
                        <item.icon className="w-6 h-6" />
                        <span className="text-2xl sm:text-3xl font-semibold sm:font-bold uppercase tracking-wide bg-gradient-text bg-clip-text text-transparent">
                          {item.label}
                        </span>
                      </div>
                      <p className="text-lg sm:text-xl font-semibold tracking-[0.02em] text-white/90">{item.value}</p>
                    </motion.div>
                  )
              )}
            </section>


            {/* ABOUT THE CLUB SECTION */}
            <section className="w-full max-w-6xl">
              <div className="flex items-center gap-4 mb-8">
                <h3 className="text-4xl font-bold italic uppercase tracking-wide whitespace-nowrap bg-gradient-text bg-clip-text text-transparent">
                  About the Club
                </h3>
              </div>
              <div className="font-normal text-white/90 px-2">
                <ExpandableText text={clubData["About the Club"]} wordLimit={100} />
              </div>
            </section>

            {/* ICONIC MOMENTS */}
            <section className="space-y-16">
              <h3 className="text-4xl font-bold italic uppercase tracking-wide bg-gradient-text bg-clip-text text-transparent">
                Iconic Moments
              </h3>
              <div className="relative space-y-24">
                {clubData["Most Iconic Moments"]?.map((moment: string, i: number) => {
                  const yearRangeRegex = /\b(18|19|20)\d{2}(?:[–-]\d{2})?\b/;
                  const match = moment.match(yearRangeRegex);
                  const year = match ? match[0] : "—";

                  return (
                    <motion.div
                      key={i}
                      className="relative md:pl-28 group"
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true, margin: "-100px" }}
                    >
                      <div className="absolute left-0 top-0 hidden md:flex w-24 h-24 items-center justify-center rounded-full border border-white/75 group-hover:shadow-[0_0_20px_rgba(255,255,255,0.5)] group-hover:backdrop-blur-md transition-all">
                        <span className="text-white font-bold text-xl group-hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.8)]">
                          {year}
                        </span>
                      </div>
                      <div className="space-y-4">
                        <span className="md:hidden text-white font-semibold text-lg">{year}</span>
                        <p className="text-lg sm:text-xl font-lightbold sm:font-semibold leading-relaxed text-white/85 max-w-3xl">
                          {moment}
                        </p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </section>


            {/* SILVERWARE CABINET */}
            <section className="py-6">
              <div className="flex items-center gap-4 mb-10">
                <h3 className="text-4xl font-bold italic uppercase tracking-wide bg-gradient-text bg-clip-text text-transparent">
                  Silverware Cabinet
                </h3>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {clubData["Total Trophies Won"]
                ?.split("\n")
                .slice(1)
                .filter(line => line.includes(":")) // skip invalid lines like Bournemouth's last line
                .map((line: string, i: number) => {
                  const [competition, count] = line.split(":");
                  const value = count.trim();
                  // Extract number and optiona l (…)
                  const match = value.match(/^(\d+)\s*(\(.*\))?$/);
                  const mainNumber = match?.[1] || value;   // 1, 12, 23, etc
                  const bracketPart = match?.[2] || null;   // (5 runners-up), etc

                  return (
                    <div
                      key={i}
                      className={`
                        group relative flex flex-col justify-between items-center
                        bg-transparent rounded-3xl p-8
                        hover:-translate-y-2 transition-all duration-500 ease-out
                        min-h-[220px]  /* uniform height for all cards */
                      `}
                    >
                      {/* Trophy Icon */}
                      <div
                        className="
                          relative transform
                          text-white
                          transition-all duration-500
                          mb-4
                          group-hover:scale-110
                          group-hover:drop-shadow-[0_0_14px_rgba(255,255,255,0.7)]
                        "
                      >
                        <Trophy className="w-12 h-12" strokeWidth={1} />
                      </div>


                      {/* Number of trophies */}
                      <span className="text-2xl sm:text-4xl font-bold text-white mb-1 tracking-tighter">
                        {mainNumber}
                      </span>

                      {bracketPart && (
                        <span className="text-xl font-lightbold text-white/80 tracking-tighter">
                          {bracketPart}
                        </span>
                      )}


                      {/* Competition name */}
                      <p
                        className="
                          text-sm sm:text-lg
                          font-semibold uppercase
                          tracking-[0.08em] sm:tracking-[0.12em]
                          text-white/90 text-center
                          leading-snug sm:leading-relaxed
                          max-w-full 
                          break-words sm:break-normal
                          group-hover:text-white/100
                          transition-colors
                        "
                      >
                        {competition.trim()}
                      </p>
                    </div>
                  );
                })
              }

              </div>
            </section>


            {/* RIVALRIES */}
            <section>
              <h3
                className="
                  text-4xl font-bold italic uppercase tracking-wide
                  whitespace-nowrap bg-gradient-text bg-clip-text text-transparent
                  mb-10
                  relative z-10
                "
              >
                Club Rivalries
              </h3>

              <div className="space-y-6">
                {clubData["Major Rivalries"]?.map((r: any, i: number) => (
                  <motion.div 
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, ease: "easeOut" }}
                    className="
                    flex items-center gap-8
                    bg-transparent backdrop-blur-xs
                    rounded-2xl p-6
                    border border-white/0
                    transition-all duration-300
                  "

                  >
                    {/* Crest + Club */}
                    <RivalCrest club={r.Club} />

                    {/* Text Content */}
                    <div className="flex-1">
                      <h4 className="text-2xl font-semibold text-white italic mb-1 tracking-[0.015em]">
                        {r["Rivalry Name"]}
                      </h4>

                      <p className="font-lightbold text-white/80 text-lg leading-relaxed">
                        {r.Notes}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </section>



          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}