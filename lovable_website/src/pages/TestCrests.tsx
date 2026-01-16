export default function TestCrests() {
  const clubs = [
    { name: "Arsenal", logo: "/crests/Arsenal.svg" },
    { name: "Aston Villa", logo: "/crests/Aston_Villa.svg" },
    { name: "Bournemouth", logo: "/crests/Bournemouth.svg" },
    { name: "Brentford", logo: "/crests/Brentford.svg" },
    { name: "Brighton & Hove Albion", logo: "/crests/Brighton.svg" },
    { name: "Burnley", logo: "/crests/Burnley.svg" },
  ];

  return (
    <div style={{ padding: 40 }}>
      <h1 style={{ fontSize: 32, marginBottom: 20 }}>Crest Test</h1>

      <div style={{ display: "flex", gap: 40, flexWrap: "wrap" }}>
        {clubs.map((club) => (
          <div key={club.name} style={{ textAlign: "center" }}>
            <img
              src={club.logo}
              alt={club.name}
              width={100}
              height={100}
              style={{ marginBottom: 10 }}
            />
            <p>{club.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
