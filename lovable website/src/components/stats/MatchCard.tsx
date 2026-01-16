// "use client";
// import { motion } from "framer-motion";

// interface Props {
//   match: {
//     match_id: number;
//     HomeTeam: string;
//     AwayTeam: string;
//     FTHG: number;
//     FTAG: number;
//   };
//   onSelect: (matchId: number) => void;
// }

// const crestPath = (team: string) =>
//   `/public/crests/${team.replace(/\s+/g, "")}.svg`;

// const MatchCard = ({ match, onSelect }: Props) => {
//   return (
//     <motion.div
// //   layout
// //   onClick={onToggle}
// //   whileHover={{
// //     scale: 1.025,
// //     boxShadow: "0 0 25px rgba(109, 91, 91, 0.25)",
// //   }}
// //   transition={{
// //     type: "spring",
// //     stiffness: 300,
// //     damping: 22,
// //   }}
// //   className="cursor-pointer rounded-2xl border border-white/20
// //              bg-white/5 backdrop-blur-md p-5 space-y-4
// //              hover:border-white/75"
// // >
//       {/* HOME */}
//       <div className="flex items-center gap-4 w-1/3">
//         <img src={crestPath(match.HomeTeam)} className="w-10 h-10" />
//         <span className="font-semibold">{match.HomeTeam}</span>
//       </div>

//       {/* SCORE */}
//       <div className="text-2xl font-bold w-1/3 text-center">
//         {match.FTHG} – {match.FTAG}
//       </div>

//       {/* AWAY */}
//       <div className="flex items-center gap-4 justify-end w-1/3">
//         <span className="font-semibold">{match.AwayTeam}</span>
//         <img src={crestPath(match.AwayTeam)} className="w-10 h-10" />
//       </div>
//     </motion.div>
//   );
// };

// export default MatchCard;