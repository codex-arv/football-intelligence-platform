import { useEffect, useRef } from "react";
import turfImage from "../../assets/turf3.png";

/**
 * STRATEGIC NEXUS BACKGROUND (Refined)
 * Prediction-focused, analytics-driven, legacy-aware.
 */

export default function MatrixBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: 0, y: 0, active: false });

  useEffect(() => {
    const canvas = canvasRef.current!;
    const SWEEP_COLOR = "252, 53, 3"; // freely changeable RGB
    const ctx = canvas.getContext("2d")!;
    const bgImage = new Image();
    bgImage.src = turfImage;
    let raf: number;
    let t = 0;

    // --- OFFSCREEN CANVAS FOR LIGHT SWEEPS (CRITICAL) ---
    const sweepCanvas = document.createElement("canvas");
    const sweepCtx = sweepCanvas.getContext("2d")!;

    const COLORS = {
      matrix: "0, 255, 90",
      highlight: "0, 255, 90",
      bg: "#041c04",
    };

    let w: number, h: number;

    const nodes: Node[] = [];
    const pulses: Pulse[] = [];
    const rings: Ring[] = [];
    const sweeps: Sweep[] = [];

    class Node {
      x: number; y: number; vx: number; vy: number;
      size: number; baseOpacity: number;

      constructor() {
        this.x = Math.random() * w;
        this.y = Math.random() * h;
        this.vx = (Math.random() - 0.5) * 0.75;
        this.vy = (Math.random() - 0.5) * 0.75;
        this.size = Math.random() * 1.5 + 0.6;
        this.baseOpacity = Math.random() * 0.35 + 0.15;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > w) this.vx *= -1;
        if (this.y < 0 || this.y > h) this.vy *= -1;
      }
    }

    class Pulse {
      a: Node;
      b: Node;
      progress: number;
      speed: number;

      constructor(a: Node, b: Node) {
        this.a = a;
        this.b = b;
        this.progress = 0;
        this.speed = Math.random() * 0.008 + 0.004;
      }

      update() {
        this.progress += this.speed;
      }

      draw() {
        if (this.progress > 1) return;

        const x = this.a.x + (this.b.x - this.a.x) * this.progress;
        const y = this.a.y + (this.b.y - this.a.y) * this.progress;

        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${COLORS.highlight}, 0.7)`;
        ctx.fill();
      }
    }

    class Ring {
      x: number; y: number; r: number; opacity: number;

      constructor() {
        this.x = Math.random() * w;
        this.y = Math.random() * h;
        this.r = 0;
        this.opacity = 0;
      }

      update() {
        this.r += 0.6;
        this.opacity -= 0.0008;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(${COLORS.matrix}, ${this.opacity})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }

    class Sweep {
      direction: "horizontal" | "vertical" | "diagonal";
      position: number;
      speed: number;
      width: number;
      opacity: number;

      constructor() {
        const dirs = ["horizontal", "vertical", "diagonal"] as const;
        this.direction = dirs[Math.floor(Math.random() * dirs.length)];
        this.position = -Math.max(w, h);
        this.speed = Math.random() * 0.35 + 0.25;
        this.width = Math.random() * 320 + 260;
        this.opacity = Math.random() * 0.45 + 0.35;
      }

      update() {
        this.position += this.speed;
      }

      draw() {
        let grad: CanvasGradient;

        if (this.direction === "horizontal") {
          grad = sweepCtx.createLinearGradient(
            0, this.position,
            0, this.position + this.width
          );
        } else if (this.direction === "vertical") {
          grad = sweepCtx.createLinearGradient(
            this.position, 0,
            this.position + this.width, 0
          );
        } else {
          grad = sweepCtx.createLinearGradient(
            this.position, this.position,
            this.position + this.width, this.position + this.width
          );
        }

        grad.addColorStop(0.35, `rgba(${SWEEP_COLOR}, 0)`);
        grad.addColorStop(0.5, `rgba(${SWEEP_COLOR}, ${this.opacity})`);
        grad.addColorStop(0.65, `rgba(${SWEEP_COLOR}, 0)`);

        sweepCtx.fillStyle = grad;
        sweepCtx.fillRect(0, 0, w, h);
      }
    }

    const init = () => {
      w = canvas.width = sweepCanvas.width = window.innerWidth;
      h = canvas.height = sweepCanvas.height = window.innerHeight;

      nodes.length = 0;
      pulses.length = 0;
      rings.length = 0;
      sweeps.length = 0;

      for (let i = 0; i < 90; i++) nodes.push(new Node());
    };

    const animate = () => {
      t += 0.02;

      // --- BASE IMAGE ---
      if (bgImage.complete) {
        ctx.drawImage(bgImage, 0, 0, w, h);
      } else {
        ctx.fillStyle = COLORS.bg;
        ctx.fillRect(0, 0, w, h);
      }

      // Darken + unify tone
      ctx.fillStyle = "rgba(5, 32, 7, 0.68)";
      ctx.fillRect(0, 0, w, h);

      // Subtle desaturation pass
      ctx.fillStyle = "rgba(6, 33, 3, 0.64)";
      ctx.fillRect(0, 0, w, h);

      // drawConnections();

      pulses.forEach(p => {
        p.update();
        p.draw();
      });
      pulses.splice(0, pulses.filter(p => p.progress <= 1).length);

      if (Math.random() > 0.995) rings.push(new Ring());
      rings.forEach(r => {
        r.update();
        r.draw();
      });
      rings.splice(0, rings.filter(r => r.opacity > 0).length);

      // drawScanlines();

      // === LIGHT SWEEPS (OFFSCREEN → SCREEN BLEND) ===
      // sweepCtx.clearRect(0, 0, w, h);

      // if (Math.random() > 0.992) {
      //   sweeps.push(new Sweep());
      // }

      // for (let i = sweeps.length - 1; i >= 0; i--) {
      //   const s = sweeps[i];
      //   s.update();
      //   s.draw();

      //   if (s.position > Math.max(w, h) * 2) {
      //     sweeps.splice(i, 1);
      //   }
      // }

      // ctx.save();
      // ctx.globalCompositeOperation = "screen";
      // ctx.drawImage(sweepCanvas, 0, 0);
      // ctx.restore();

      raf = requestAnimationFrame(animate);
    };

    window.addEventListener("resize", init);
    window.addEventListener("mousemove", (e) => {
      mouseRef.current = { x: e.clientX, y: e.clientY, active: true };
    });

    init();
    animate();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", init);
    };
  }, []);

  return (
    <>
      {/* Turf image background layer */}
      <div
        className="fixed inset-0 -z-20 pointer-events-none"
        style={{
          backgroundImage: `url(${turfImage})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          filter: "brightness(0.35) contrast(1.1) saturate(0.85)",
        }}
      />

      {/* Matrix animation layer (unchanged) */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 -z-10"
        style={{ filter: "contrast(1.27) brightness(2.5)" }}
      />
    </>
  );
}