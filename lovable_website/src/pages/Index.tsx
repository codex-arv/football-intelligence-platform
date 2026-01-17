import { Card, CardContent } from "@/components/ui/card";
import stadiumHero from "@/assets/stadiumimage.png";
import { Zap, BarChart3, Trophy, ChartNoAxesColumnIncreasing, Crown, Volleyball, Heart } from "lucide-react";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";

const Index = () => {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />
      {/* Hero Section - Full Screen with Stadium Background */}
      <section 
        id="home"
        className="relative z-10 h-screen flex items-center justify-center overflow-hidden"
      >
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-center bg-cover"
          style={{
            backgroundImage: `url(${stadiumHero})`,
            filter: "brightness(1.2) contrast(1) saturate(1.5) sepia(0.1)", // ↓ darken, ↑ contrast
          }}
        />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-hero opacity-50" />
        
        {/* Hero Content */}
        <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
          <h1 className="text-6xl md:text-8xl font-extrabold italic uppercase tracking-[0.02em] mb-6 
          bg-gradient-text bg-clip-text text-transparent animate-fade-in-up inline-block whitespace-nowrap px-6"
              style={{ animationDelay: "0.2s", opacity: 0 }}
          >
            The 90<span className="text-5xl md:text-5xl align-super">th</span> Minute
          </h1>
          <p className="text-2xl md:text-3xl text-foreground font-lightbold mb-4 animate-fade-in-up"
            style={{ animationDelay: "0.5s", opacity: 0 }}
          >
            Every minute. Every match. Every goal, predicted.
          </p>
          <p className="text-2xl md:text-3xl text-foreground font-lightbold mb-4 animate-fade-in-up"
            style={{ animationDelay: "1s", opacity: 0 }}
          >
            Powered by AI. Inspired by the beautiful game.
          </p>
        </div>
      </section>


      {/* About Section */}
      <section id="about" className="relative z-10 py-24 px-4">
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <div 
            className="mb-16 animate-fade-in"
            style={{ animationDelay: "0.2s", opacity: 0 }}
          >
            <div className="h-px w-32 bg-gradient-to-r from-transparent via-secondary to-transparent mx-auto mb-12" />
            
            <h2 className="text-4xl md:text-6xl uppercase italic tracking-[0.02em] font-bold mb-6 text-foreground bg-gradient-text bg-clip-text text-transparent">
              About the Project
            </h2>
            
            <p className="text-lg md:text-xl text-foreground/80 leading-relaxed mb-6 tracking-[0.01em]">
              Tired of predictions based on gut feelings, biased commentators, or arbitrary streaks?<br />
              The 90<sup>th</sup> Minute is the data-driven revolution in football analysis.
            </p>
            
            <p className="text-lg md:text-xl text-foreground/80 leading-relaxed mb-6 tracking-[0.01em]">
              Our project originated from a single frustration: why do conventional prediction models still miss so many upsets and late-game shifts? We solved this by treating every match not as a linear sequence, but as a complex classification problem. Utilizing over 25 years of historical Premier League data — from team formation and possession metrics to complex shot conversion rates — we leverage advanced machine learning models (specifically designed for multi-class classification) to provide deep, non-emotional match forecasts.
            </p>
            
            <p className="text-lg md:text-xl text-foreground/80 leading-relaxed mb-6 tracking-[0.01em]">
              This isn't crystal-ball gazing. This is data science applied directly to the beautiful game, giving you the classified certainty of the match outcome before the referee blows the final whistle.
            </p>
            
            <p className="text-lg md:text-xl text-foreground/80 leading-relaxed tracking-[0.01em]">
              Welcome to the precision of
            </p>

            <p className="text-lg md:text-xl text-foreground/80 font-semibold italic leading-relaxed tracking-[0.01em]">
              The 90<sup>th</sup> Minute
            </p>
            
            <div className="h-px w-32 bg-gradient-to-r from-transparent via-secondary to-transparent mx-auto mt-12" />
          </div>

          {/* Core Features Heading */}
          <h2 className="text-4xl md:text-6xl font-bold uppercase italic tracking-[0.02em] text-foreground bg-gradient-text bg-clip-text text-transparent mt-16 mb-12">
            Core Features
          </h2>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={
                <div className="group-hover:animate-icon-spin transition-transform duration-500">
                  <Volleyball className="w-10 h-10" />
                </div>
              }
              title="Live Match Prediction"
              description="Forecast match outcomes and precise scorelines using ML models — analyzing team form, using historical data and match dynamics."
              delay="0.3s"
              hoverShadow="hover:shadow-glow-white"
            />
            
            <FeatureCard
              icon={
                <div className="group-hover:animate-bounce transition-transform duration-500">
                  <ChartNoAxesColumnIncreasing className="w-10 h-10" />
                </div>
              }
              title="Match & Player Statistics"
              description="Dive into match & player statistics from the 2024 and 2025 seasons — uncovering team trends and individual performances."
              delay="0.5s"
              hoverShadow="hover:shadow-glow-white"
            />
            
            <FeatureCard
              icon={
                <div className="group-hover:animate-pulse-glow transition-transform duration-500">
                  <Heart className="w-10 h-10" />
                </div>
              }              
              title="Hall of Clubs"
              description="Explore Premier League clubs from 2024 and 2025 seasons in depth — uncover their background, legacy, historic achievements, iconic moments and major rivalries."
              delay="0.7s"
              hoverShadow="hover:shadow-glow-white"
            />
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  delay: string;
  hoverShadow: string;
}

const FeatureCard = ({ icon, title, description, delay, hoverShadow }: FeatureCardProps) => {
  const featureLinks: Record<string, string> = {
    "Live Match Prediction": "/prediction",
    "Match & Player Statistics": "/statistics",
    "Hall of Clubs": "/knowclubs",
  };

  const buttonTexts: Record<string, string> = {
    "Live Match Prediction": "Execute Prediction",
    "Match & Player Statistics": "Analyze Statistics",
    "Hall of Clubs": "Explore Archives",
  };

  const handleClick = () => {
    const url = featureLinks[title];
    if (url) window.location.href = url;
  };

  return (
      <Card
        className={`group relative overflow-hidden transition-all 
                    bg-transparent backdrop-blur-md border border-white/50
                    scale-110 ${hoverShadow}
                    animate-scale-in opacity-0`}
        style={{ animationDelay: delay, animationFillMode: "forwards" }}
      >
        {/* Premium Shimmer Effect Overlay */}
        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-1000 pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-tr -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
        </div>

        <CardContent className="relative p-8 flex flex-col items-center text-center h-full z-20">
          {/* Icon with Glass Circle */}
          <div
            className="
              relative inline-flex items-center justify-center w-20 h-20 rounded-2xl 
              mb-8 transition-all duration-500 scale-110
              shadow-[0_0_15px_rgba(255,255,255,0.50)]
              hover:shadow-[0_0_30px_rgba(255,255,255,0.4)]
            "
          >

            <div className="text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.15)]">
              {icon}
            </div>
            
            {/* Subtle glow behind icon */}
            <div className="absolute inset-0 bg-white/0 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          </div>

          {/* Title with extra letter spacing for premium feel */}
          <h3 className="text-2xl font-bold mb-4 text-white tracking-tight group-hover:tracking-[0.04em] transition-all duration-500">
            {title}
          </h3>

          {/* Description with refined opacity */}
          <p className="text-white/80 leading-relaxed mb-10 text-md font-lightbold">
            {description}
          </p>

          {/* Extraordinary Button: Ghost style with white-out hover */}
          <button
            onClick={handleClick}
            className="relative mt-auto w-full py-3 px-6 rounded-lg font-semibold text-xs uppercase tracking-[0.18em]
                      border border-white/20 text-white/100
                      hover:shadow-[0_0_8px_rgba(255,255,255,0.6),0_0_18px_rgba(255,255,255,0.4)]
                      hover:border-white/80 overflow-hidden transition-all duration-300"
          >
            <span
              className="
                relative z-10 text-white transition-all duration-300
              "
            >
              {buttonTexts[title]}
            </span>


            {/* Background fill animation */}
            <div className="absolute inset-0 bg-white translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 ease-out" />
          </button>
        </CardContent>
      </Card>
  );
};

export default Index;