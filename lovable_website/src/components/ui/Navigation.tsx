"use client";
import { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLocation, useNavigate } from "react-router-dom";
import icon1 from "../ui/matrix90.png";

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inHero, setInHero] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  const navLinks = [
    { name: "Home", href: "#home" },
    { name: "About", href: "#about" },
    { name: "Workflow", href: "/workflow" },
    { name: "Prediction", href: "/prediction" },
    { name: "Statistics", href: "/statistics" },
    { name: "Clubs", href: "/knowclubs" },
    { name: "Contact", href: "/contact" },
  ];

  const scrollToSection = (hash: string) => {
  const element = document.querySelector(hash);
  if (!element) return;

  let yOffset = 75; // default offset

  if (hash === "#home") {
    yOffset = 0; // or smaller value if you want hero fully visible
  }

  if (hash === "#about") {
    yOffset = -69; // tighter spacing for About section
  }

  const y =
    element.getBoundingClientRect().top + window.pageYOffset - yOffset;

  window.scrollTo({
    top: y,
    behavior: "smooth",
  });
};


  const handleNavigation = (href: string) => {
    setIsOpen(false);

    const isHash = href.startsWith("#");

    if (location.pathname !== "/" && isHash) {
      // Go home first
      navigate("/");
      setTimeout(() => scrollToSection(href), 300);
    } 
    else if (isHash) {
      scrollToSection(href);
    } 
    else {
      navigate(href);
    }
  };

  // Hero observer
  useEffect(() => {
    if (location.pathname !== "/") {
      setInHero(false);
      return;
    }

    const hero = document.querySelector("#home");
    if (!hero) return;

    const observer = new IntersectionObserver(
      ([entry]) => setInHero(entry.isIntersecting),
      { threshold: 0.5 }
    );

    observer.observe(hero);
    return () => observer.disconnect();
  }, [location.pathname]);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 border-b border-white/10 
      ${inHero
        ? "bg-black/30 backdrop-blur-sm"
        : "bg-[linear-gradient(to_right,var(--gradient-sections))] backdrop-blur-md shadow-lg"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">

          {/* LOGO */}
          <button
            onClick={() => handleNavigation("#home")}
            className="flex items-center hover:opacity-80 transition-opacity"
            aria-label="Home"
          >
            <img 
              src={icon1}
              alt="90th Minute Logo" 
              className="h-16 w-auto object-contain"
            />

          </button>

          {/* DESKTOP NAV */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <button
                key={link.name}
                onClick={() => handleNavigation(link.href)}
                className="text-foreground transition-all duration-300 hover:text-white hover:drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]"
              >
                {link.name}
              </button>
            ))}
          </div>

          {/* MOBILE BUTTON */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden bg-transparent text-white hover:bg-transparent hover:text-white" // ✅ updated here
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="h-6 w-6 text-white" /> : <Menu className="h-6 w-6 text-white" />}
          </Button>

        </div>
      </div>

      {/* MOBILE NAV */}
      {isOpen && (
        <div className="md:hidden bg-black/95 backdrop-blur-lg border-t border-white/10 animate-fade-in">
          <div className="px-4 pt-2 pb-4 space-y-1">
            {navLinks.map((link) => (
              <button
                key={link.name}
                onClick={() => handleNavigation(link.href)}
                className="block w-full text-left px-3 py-2 text-foreground hover:text-white hover:bg-white/5 rounded-md transition-all duration-300"
              >
                {link.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;