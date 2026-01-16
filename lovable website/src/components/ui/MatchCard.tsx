// interface Props {
//   home: string
//   away: string
//   homeGoals: number
//   awayGoals: number
//   onClick: () => void
// }

// export default function MatchCard({
//   home,
//   away,
//   homeGoals,
//   awayGoals,
//   onClick
// }: Props) {
//   return (
//     <button
//       onClick={onClick}
//       className="flex items-center justify-between p-4 bg-zinc-900 rounded-xl hover:bg-zinc-800 transition"
//     >
//       <div className="flex items-center gap-3">
//         <img src={`/crests/${home}.svg`} className="w-8 h-8" />
//         <span>{home}</span>
//       </div>

//       <span className="text-xl font-bold">
//         {homeGoals} – {awayGoals}
//       </span>

//       <div className="flex items-center gap-3">
//         <span>{away}</span>
//         <img src={`/crests/${away}.svg`} className="w-8 h-8" />
//       </div>
//     </button>
//   )
// }
