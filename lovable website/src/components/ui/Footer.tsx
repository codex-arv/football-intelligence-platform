import { motion } from "framer-motion";
import { Github, Instagram, Linkedin, Mail, ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link, useLocation, useNavigate } from "react-router-dom";

const Footer = () => {
  const quickLinks = [
    { name: "Home", href: "#home" },
    { name: "About", href: "#about" },
    { name: "Prediction", href: "/prediction" },
    { name: "Statistics", href: "/statistics" },
    { name: "Clubs", href: "/knowclubs" },
    { name: "Contact", href: "/contact" },
  ];

  const socialLinks = [
    { icon: Github, href: "https://github.com/codex-arv", label: "GitHub" },
    { icon: Linkedin, href: "https://linkedin.com/in/aarav-srivastava1", label: "LinkedIn" },
    { icon: Instagram, href: "https://instagram.com/21spiderx", label: "Instagram" },
    { icon: Mail, href: "mailto:aarav.srivastava@aol.com", label: "Email" },
  ];


  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const navigate = useNavigate();
  const location = useLocation();

  const handleLinkClick = (href: string) => {
    // If it's a hash link
    if (href.startsWith("#")) {
      if (location.pathname !== "/") {
        // First go to homepage
        navigate("/");
        // Then scroll after navigation
        setTimeout(() => {
          const el = document.querySelector(href);
          el?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      } else {
        const el = document.querySelector(href);
        el?.scrollIntoView({ behavior: "smooth" });
      }
    } else {
      // Normal route
      navigate(href);
    }
  };


  return (
    <footer
  className="
    relative 
    overflow-hidden 
    border-t border-white/80
    bg-black
  "
>
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Top Glowing Divider */}
        <motion.div
          initial={{ scaleX: 0, opacity: 0 }}
          whileInView={{ scaleX: 1, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          viewport={{ once: true }}
          className="h-px w-full bg-gradient-to-r from-transparent via-primary/50 to-transparent mb-12"
        />

        {/* Main Footer Content - 3 Columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          {/* Brand Column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="space-y-4"
          >
            <h3 className="text-4xl font-bold bg-gradient-text bg-clip-text text-transparent italic">
              The 90<span className="text-xl align-super">th</span> Minute
            </h3>
            <p className="text-foreground/80 text-md leading-relaxed">
              Every minute. Every match. Every goal, predicted.
            </p>
            <p className="text-foreground/70 text-md leading-relaxed">
              Powered by AI. Inspired by the beautiful game.
            </p>
          </motion.div>

          {/* Quick Links Column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="space-y-4"
          >
            <h4 className="text-2xl font-semibold text-foreground">Quick Links</h4>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <button
                    onClick={() => handleLinkClick(link.href)}
                    className="text-left text-foreground/70 text-md hover:text-primary transition-colors duration-300 relative group"
                  >
                    {link.name}
                    <span className="absolute bottom-0 left-0 w-0 h-px bg-primary group-hover:w-full transition-all duration-300" />
                  </button>
                    <span className="absolute bottom-0 left-0 w-0 h-px bg-primary group-hover:w-full transition-all duration-300" />
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Social & Scroll to Top Column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
            className="space-y-6"
          >
            <div className="space-y-4">
              <h4 className="text-2xl font-semibold text-foreground">Social Links</h4>
              <div className="flex gap-4">
                {socialLinks.map((social) => (
                  <motion.a
                    key={social.label}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={social.label}
                    whileHover={{ scale: 1.15, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="group relative"
                  >
                    <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center backdrop-blur-xl border border-white/10 transition-all duration-300 group-hover:shadow-glow-white">
                    <social.icon className="w-6 h-6 text-foreground group-hover:text-white transition-colors duration-300" />
                     </div>

                    {/* Tooltip */}
                    <span
                      className="
                        absolute -bottom-2 left-1/2 -translate-x-1/2
                        px-3 py-1 rounded-md text-xs font-medium
                        bg-black/80 text-white
                        opacity-0 group-hover:opacity-100
                        translate-y-2 group-hover:translate-y-0
                        transition-all duration-200
                        pointer-events-none
                        backdrop-blur-sm border border-white/10
                        whitespace-nowrap
                      "
                    >
                      {social.label}
                    </span>

                  </motion.a>
                ))}
              </div>
            </div>

            {/* Scroll to Top Button */}
            <div>
              <button
                onClick={scrollToTop}
                className="
                  group relative inline-flex items-center justify-center gap-2
                  px-8 py-3
                  rounded-full
                  font-lightbold text-xs uppercase tracking-[0.2em]
                  text-white
                  border border-white/30
                  transition-all duration-300

                  hover:border-white/90
                "
              >
                <ArrowUp className="w-4 h-4" />
                Back to Top

                {/* Border glow layer */}
                <span
                  className="
                    pointer-events-none
                    absolute inset-0 rounded-full
                    opacity-0
                    transition-opacity duration-300
                    group-hover:opacity-100
                    [box-shadow:0_0_10px_rgba(255,255,255,0.7),0_0_20px_rgba(255,255,255,0.4)]
                  "
                />
              </button>


            </div>
          </motion.div>
        </div>

        {/* Bottom Glowing Divider */}
        <motion.div
          initial={{ scaleX: 0, opacity: 0 }}
          whileInView={{ scaleX: 1, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          viewport={{ once: true }}
          className="h-px w-full bg-gradient-to-r from-transparent via-primary/50 to-transparent mb-8"
        />

        {/* Copyright */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center text-foreground/80 text-sm"
        >
          © 2025 The 90<sup>th</sup> Minute. All rights reserved.
        </motion.div>

        {/* Disclaimer */}
        <p className="mt-2 italic tracking-[0.05em] text-center text-sm leading-relaxed text-foreground/60 max-w-3xl mx-auto">
          Predictions, statistics and club information are provided for informational and research purposes only.  
        </p>
        <p className="italic tracking-[0.05em] text-center text-sm leading-relaxed text-foreground/60 max-w-3xl mx-auto">
          Model outputs and aggregated data may contain inaccuracies, delays or limitations.
        </p>
      </div>
    </footer>
  );
};

export default Footer;