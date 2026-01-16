export async function fetchMatches(
  season: number,
  gameweek: number
) {
  const res = await fetch(
    `http://localhost:5005/api/v1/stats/matches?season=${season}&gameweek=${gameweek}`
  )

  if (!res.ok) {
    throw new Error("Failed to load matches")
  }

  return res.json()
}
