"use client";
import { motion } from "framer-motion";
import Navigation from "@/components/ui/Navigation";
import Footer from "@/components/ui/Footer";
import { Mail, Linkedin, Github, Brain, Code, Database, Cpu, Server } from "lucide-react";
import MatrixBackground from "@/components/ui/MatrixComponent";
import MatrixGradientOverlay from "@/components/ui/MatrixGradientOverlay";


const Contact = () => {
  return (
    <div className="relative min-h-screen">
      <MatrixBackground />
      <MatrixGradientOverlay />
      <Navigation />
      <div className="relative z-10 max-w-6xl mx-auto px-6 py-24 sm:py-28 space-y-16 sm:space-y-24 overflow-visible">

        {/* ================= PAGE TITLE ================= */}
        <motion.section
          className="text-center space-y-4"
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-6xl font-extrabold bg-gradient-text bg-clip-text text-transparent leading-[1.15]
          uppercase italic tracking-[0.01em]">
            Get In Touch
          </h1>

          <p className="text-xl md:text-2xl italic font-lightbold tracking-[0.0em] text-white/80 max-w-2xl mx-auto">
            Open to internship opportunities, collaborations and discussions.
          </p>
        </motion.section>

        {/* ================= CONTEXT ================= */}
        <motion.section
          className="space-y-14 overflow-visible"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
        >
          {/* Background */}
          <div className="space-y-0 sm:space-y-3 overflow-visible">
            <h2 className="text-2xl sm:text-3xl font-bold uppercase tracking-[0.05em] bg-gradient-text bg-clip-text text-transparent leading-[1.3] pb-1">
              Background
            </h2>
            <p className="text-lg text-white/80 tracking-[0.03em] leading-relaxed">
              I am <strong>Aarav Srivastava</strong>, a B.Tech <strong>Computer Science & Engineering</strong> student, in my 6th semester at <strong>KIIT University</strong>,
              currently maintaining a <strong>CGPA of 9.72</strong>. I am driven by a strong interest in
              machine learning and data analytics, with a focus on applying data-driven
              approaches to practical, real-world problems. My academic and project
              experience includes exposure to end-to-end ML workflows, performance-focused model evaluation and relevant research publications in IEEE.
            </p>
          </div>

          {/* Technical Focus */}
          <div className="space-y-0 sm:space-y-3 overflow-visible">
            <h2 className="text-2xl sm:text-3xl font-bold uppercase tracking-[0.05em] bg-gradient-text bg-clip-text text-transparent leading-[1.3] pb-1">
              Technical Focus
            </h2>
            <p className="text-lg text-white/80 tracking-[0.03em] leading-relaxed">
              My technical focus lies at the intersection of Machine Learning, Data Science & Deep Learning. I also have hands-on experience with supervised and
              unsupervised learning techniques, data engineering and analysis pipelines and applied model
              development using Python-based ML libraries.
            </p>
            <p className="text-lg text-white/90 tracking-[0.03em] leading-relaxed">
              Additionally, I actively explore backend development using FastAPI, RESTful
              APIs, and web scraping to build data-centric applications. I place strong
              emphasis on clean code, scalable design, and core computer science
              fundamentals, while continuously expanding my practical exposure through
              projects and research-driven work.
            </p>
          </div>
        </motion.section>

        {/* ================= TECH STACK FEATURE CARDS ================= */}
        <motion.section
          className="space-y-4 sm:space-y-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.25 }}
        >
          <h2 className="text-2xl sm:text-3xl font-bold uppercase tracking-[0.05em] bg-gradient-text bg-clip-text text-transparent">
            Technical Skillsets
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-8">
            {[{
              icon: Brain, title: "Machine Learning & AI", description:
                "Experience with supervised and unsupervised learning, model evaluation, and applied ML workflows using real datasets.",
              stack: "Scikit-learn, TensorFlow, PyTorch, NumPy, Pandas",
            }, {
              icon: Code, title: "Programming Languages", description:
                "Strong command over problem-solving and implementation using multiple programming paradigms.",
              stack: "Python, C/C++, Java",
            }, {
              icon: Database, title: "Data & Analytics", description:
                "Hands-on experience in data cleaning, analysis, visualization, and structured querying.",
              stack: "SQL, PostgreSQL, NumPy, Pandas, Matplotlib, Jupyter",
            }, {
              icon: Server, title: "Backend & APIs", description:
                "Experience designing and consuming RESTful APIs with a focus on clean structure and scalability.",
              stack: "FastAPI, Web Scraping, API Design",
            }, {
              icon: Cpu, title: "Core CS Foundations", description:
                "Strong conceptual understanding of essential computer science subjects supporting scalable systems.",
              stack: "DSA, OOP, Operating Systems, Data Mining & Warehousing, Computer Networks",
            }].map((item, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.05 }}
                className="group relative overflow-hidden
                           bg-transparent backdrop-blur-xl
                           border border-white/50
                           rounded-2xl p-6
                           transition-all duration-500
                           hover:border-white/70
                           hover:shadow-[0_0_25px_rgba(255,255,255,0.5)]"
              >
                <div className="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-10 transition-opacity duration-500 pointer-events-none" />
                <div className="relative">
                  <div className="flex items-center gap-4 mb-4">
                    <item.icon className="h-7 w-7 text-white/80 transition-all duration-300
                                           group-hover:text-white
                                           group-hover:drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]" />
                    <h3 className="text-xl font-semibold text-white">{item.title}</h3>
                  </div>
                  <p className="text-white/80 text-md leading-relaxed mb-4">{item.description}</p>
                  <p className="text-md text-white/75">
                    <span className="text-white/80 font-semibold font-medium">Tech:</span> {item.stack}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* ================= CONTACT FEATURE CARDS ================= */}
        <motion.section
          className="space-y-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.35 }}
        >
          <h2 className="text-3xl font-bold uppercase tracking-[0.04em] bg-gradient-text bg-clip-text text-transparent">
            Contact & Profiles
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-8">
            {[
              { icon: Mail, title: "Work Email", href: "mailto:2305670@kiit.ac.in" },
              { icon: Mail, title: "Personal Email", href: "mailto:aarav.srivastava@aol.com" },
              { icon: Linkedin, title: "LinkedIn", href: "https://linkedin.com/in/aarav-srivastava1" },
              { icon: Github, title: "GitHub", href: "https://github.com/codex-arv" },
            ].map((item, index) => (
              <motion.a
                key={index}
                href={item.href}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.05 }}
                className="group relative overflow-hidden
                           bg-transparent backdrop-blur-xl
                           border border-white/30
                           rounded-2xl p-6
                           transition-all duration-500
                           hover:border-white/70
                           hover:shadow-[0_0_25px_rgba(255,255,255,0.5)]
                           cursor-pointer"
              >
                <div className="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-10 transition-opacity duration-500 pointer-events-none" />
                <div className="relative flex items-center gap-4">
                  <item.icon className="h-7 w-7 text-white/80 transition-all duration-300
                                         group-hover:text-white
                                         group-hover:drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]" />
                  <h3 className="text-lg tracking-[0.02em] font-lightbold text-white">{item.title}</h3>
                </div>
              </motion.a>
            ))}
          </div>
        </motion.section>

      </div>

      <Footer />
    </div>
  );
};

export default Contact;