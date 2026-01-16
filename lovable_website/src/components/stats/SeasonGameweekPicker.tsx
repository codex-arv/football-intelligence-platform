// "use client";
// import { Button } from "@/components/ui/button";

// interface Props {
//   season: number;
//   gameweek: number;
//   setSeason: (s: number) => void;
//   setGameweek: (g: number) => void;
//   onSubmit: () => void;
// }

// const SeasonGameweekPicker = ({
//   season,
//   gameweek,
//   setSeason,
//   setGameweek,
//   onSubmit,
// }: Props) => {
//   return (
//     <div className="flex flex-col md:flex-row gap-6 items-center justify-center">

//       <select
//         value={season}
//         onChange={(e) => setSeason(Number(e.target.value))}
//         className="px-6 py-3 rounded-lg bg-black/40 border border-white/20 text-white"
//       >
//         <option value={2024}>2024–25</option>
//         <option value={2025}>2025–26</option>
//       </select>

//       <input
//         type="number"
//         min={1}
//         max={38}
//         value={gameweek}
//         onChange={(e) => setGameweek(Number(e.target.value))}
//         className="px-6 py-3 rounded-lg bg-black/40 border border-white/20 text-white w-32"
//         placeholder="Gameweek"
//       />

//       <Button
//         onClick={onSubmit}
//         className="border border-white text-black hover:scale-110 transition-all"
//       >
//         View Matches
//       </Button>
//     </div>
//   );
// };

// export default SeasonGameweekPicker;
