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
    const ctx = canvas.getContext("2d")!;
    const bgImage = new Image();
    bgImage.src = turfImage;
    let raf: number;
    let t = 0;

    const COLORS = {
      matrix: "0, 255, 90",
      highlight: "0, 255, 90",
      bg: "#041c04",
    };

    let w: number, h: number;

    const nodes: Node[] = [];
    const pulses: Pulse[] = [];
    const rings: Ring[] = [];

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

    const init = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;

      nodes.length = 0;
      pulses.length = 0;
      rings.length = 0;

      for (let i = 0; i < 90; i++) nodes.push(new Node());
    };

    const drawScanlines = () => {
      ctx.fillStyle = "rgba(0,255,90,0.012)";
      for (let y = 0; y < h; y += 4) {
        ctx.fillRect(0, y, w, 1);
      }
    };

    const drawConnections = () => {
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.hypot(dx, dy);

          if (dist < 150) {
            ctx.strokeStyle = `rgba(${COLORS.matrix}, ${0.12 * (1 - dist / 150)})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();

            if (Math.random() > 0.9985) {
              pulses.push(new Pulse(nodes[i], nodes[j]));
            }
          }
        }

        if (mouseRef.current.active) {
          const dx = nodes[i].x - mouseRef.current.x;
          const dy = nodes[i].y - mouseRef.current.y;
          const d = Math.hypot(dx, dy);
          if (d < 200) {
            ctx.strokeStyle = `rgba(${COLORS.matrix}, 0.1)`;
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(mouseRef.current.x, mouseRef.current.y);
            ctx.stroke();
          }
        }
      }
    };

    const animate = () => {
      t += 0.02;

      // Draw turf image as base layer
      if (bgImage.complete) {
        ctx.drawImage(bgImage, 0, 0, w, h);
      } else {
        ctx.fillStyle = COLORS.bg;
        ctx.fillRect(0, 0, w, h);
      }

      // Darken + unify tone (critical for readability)
      ctx.fillStyle = "rgba(4, 32, 4, 0.68)";
      ctx.fillRect(0, 0, w, h);

      // Subtle desaturation pass (keeps detail, kills glare)
      ctx.fillStyle = "rgba(5, 33, 3, 0.64)";
      ctx.fillRect(0, 0, w, h);

      // drawConnections();

      nodes.forEach(n => {
        n.update();
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.size, 0, Math.PI * 1);
        ctx.fillStyle = `rgba(${COLORS.matrix}, ${n.baseOpacity + Math.sin(t + n.x) * 0.15})`;
        ctx.fill();
      });

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

      drawScanlines();

      raf = requestAnimationFrame(animate);
    };

    const onMouseMove = (e: MouseEvent) => {
      mouseRef.current = { x: e.clientX, y: e.clientY, active: true };
    };

    window.addEventListener("resize", init);
    window.addEventListener("mousemove", onMouseMove);

    init();
    animate();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", init);
      window.removeEventListener("mousemove", onMouseMove);
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
        style={{ filter: "contrast(1.27) brightness(2.8)" }}
      />
    </>
  );
}