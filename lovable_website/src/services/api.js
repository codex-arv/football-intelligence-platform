import { API_BASE_URL } from "../config/api";

export async function fetchHealth(){
  const res = await fetch(`${API_BASE_URL}/`);
  if(!res.ok){
    throw new Error("API is not reachable.");
  }
  return res.json();
}

export async function fetchTeams(){
  const res = await fetch(`${API_BASE_URL}/api/v1/teams}`)
  if(!res.ok){
    throw new Error("Unable to fetch teams.");
  }
  return res.json();
}

export async function fetchMatchStats(season, gameweek){
  const url = new URL(`${API_BASE_URL}/api/v1/stats/matches`);
  url.searchParams.set("season", season);
  url.searchParams.set("gameweek", gameweek);
  const res = await fetch(url);
  if(!res.ok){
    throw new Error("Unable to fetch match list.");
  }
  return res.json();
}

export async function fetchBasicMatchStats(
  season, gameweek, home, away){
    const url = new URL(`${API_BASE_URL}/api/v1/stats/match/basic`);
    url.searchParams.set("season", season);
    url.searchParams.set("gameweek", gameweek);
    url.searchParams.set("home", home);
    url.searchParams.set("away", away);
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error("Unable to fetch basic match stats");
    }
    return res.json();
  }

export async function fetchPlayerStats(
  season, gameweek, home, away){
    const url = new URL(`${API_BASE_URL}/api/v1/stats/players`);
    url.searchParams.set("season", season);
    url.searchParams.set("gameweek", gameweek);
    url.searchParams.set("home", home);
    url.searchParams.set("away", away);
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error("Unable to fetch player match stats");
    }
    return res.json();
  }

export async function fetchClubData(club){
  const url = new URL(`${API_BASE_URL}/api/v1/clubs`);
  url.searchParams.set(club=club);
  
}