import { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  pulsePhase: number;
}

interface MatrixDrop {
  x: number;
  y: number;
  speed: number;
  length: number;
  opacity: number;
}

export default function MatrixBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d")!;
    let animationId: number;

    let t = 0;
    const MATRIX_GREEN = "0,169,21";
    const AURORA_GREEN = "0,101,29";

    const particles: Particle[] = [];
    const matrixDrops: MatrixDrop[] = [];

    let cssW = 0;
    let cssH = 0;

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;

      cssW = window.innerWidth;
      cssH = window.innerHeight;

      canvas.width = cssW * dpr;
      canvas.height = cssH * dpr;
      canvas.style.width = cssW + "px";
      canvas.style.height = cssH + "px";

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      initParticles();
      initMatrixDrops();
    };

    resize();
    window.addEventListener("resize", resize);

    function initParticles() {
      particles.length = 0;
      const particleCount = Math.floor((cssW * cssH) / 15000);
      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * cssW,
          y: Math.random() * cssH,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 2 + 1,
          opacity: Math.random() * 0.5 + 0.3,
          pulsePhase: Math.random() * Math.PI * 2,
        });
      }
    }

    function initMatrixDrops() {
      matrixDrops.length = 0;
      const dropCount = Math.floor(cssW / 80);
      for (let i = 0; i < dropCount; i++) {
        matrixDrops.push({
          x: Math.random() * cssW,
          y: Math.random() * cssH - cssH,
          speed: Math.random() * 2,
          length: Math.random() * 80 + 40,
          opacity: Math.random() * 0.3 + 0.1,
        });
      }
    }

    // FIXED CENTERED PITCH
    function drawPitch() {
      const pitchW = cssW * 1;
      const pitchH = cssH * 1;
      const px = (cssW - pitchW) / 2;
      const py = (cssH - pitchH) / 2;

      ctx.strokeStyle = `rgba(${MATRIX_GREEN},0.35)`;
      ctx.lineWidth = 1;

      ctx.strokeRect(px, py, pitchW, pitchH);

      ctx.beginPath();
      ctx.moveTo(px + pitchW / 2, py);
      ctx.lineTo(px + pitchW / 2, py + pitchH);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px + pitchW / 2, py + pitchH / 2, pitchH * 0.15, 0, Math.PI * 2);
      ctx.stroke();

      const boxW = pitchW * 0.18;
      const boxH = pitchH * 0.32;

      ctx.strokeRect(px, py + pitchH / 2 - boxH / 2, boxW, boxH);
      ctx.strokeRect(px + pitchW - boxW, py + pitchH / 2 - boxH / 2, boxW, boxH);
    }

    function drawParticles() {
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x = cssW;
        if (p.x > cssW) p.x = 0;
        if (p.y < 0) p.y = cssH;
        if (p.y > cssH) p.y = 0;

        p.pulsePhase += 0.05;
        const pulse = Math.sin(p.pulsePhase) * 0.3 + 0.7;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${MATRIX_GREEN},${p.opacity * pulse * 0.6})`;
        ctx.fill();

        for (let j = 0; j < 6; j++) {
          const p2 = particles[(Math.random() * particles.length) | 0];
          const dx = p2.x - p.x;
          const dy = p2.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120 && dist > 0) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(${MATRIX_GREEN},${(1 - dist / 120) * 0.15 * pulse})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      });
    }

    function drawMatrixRain() {
      matrixDrops.forEach((drop) => {
        drop.y += drop.speed;

        if (drop.y > cssH + drop.length) {
          drop.y = -drop.length;
          drop.x = Math.random() * cssW;
        }

        const gradient = ctx.createLinearGradient(drop.x, drop.y, drop.x, drop.y + drop.length);
        gradient.addColorStop(0, `rgba(${MATRIX_GREEN},${drop.opacity})`);
        gradient.addColorStop(0.5, `rgba(${MATRIX_GREEN},${drop.opacity * 0.5})`);
        gradient.addColorStop(1, `rgba(${MATRIX_GREEN},0)`);

        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(drop.x, drop.y);
        ctx.lineTo(drop.x, drop.y + drop.length);
        ctx.stroke();
      });
    }

    function drawScanline() {
      const scanY = ((t * 50) % (cssH + 200)) - 100;
      const grad = ctx.createLinearGradient(0, scanY - 100, 0, scanY + 100);
      grad.addColorStop(0, `rgba(${MATRIX_GREEN},0)`);
      grad.addColorStop(0.5, `rgba(${MATRIX_GREEN},0.03)`);
      grad.addColorStop(1, `rgba(${MATRIX_GREEN},0)`);

      ctx.fillStyle = grad;
      ctx.fillRect(0, scanY - 100, cssW, 200);
    }

    function drawAurora() {
      const bandCount = 4;

      for (let i = 0; i < bandCount; i++) {
        const baseY = cssH * 0.2 + i * (cssH / bandCount);
        const wave = Math.sin(t * 0.4 + i * 2) * 120;
        const y = baseY + wave;

        const grad = ctx.createLinearGradient(0, y - 200, 0, y + 200);

        grad.addColorStop(0, `rgba(${AURORA_GREEN},0)`);
        grad.addColorStop(0.4, `rgba(${AURORA_GREEN},0.06)`);
        grad.addColorStop(0.5, `rgba(${AURORA_GREEN},0.06)`);
        grad.addColorStop(0.6, `rgba(${AURORA_GREEN},0.06)`);
        grad.addColorStop(1, `rgba(${AURORA_GREEN},0)`);

        ctx.fillStyle = grad;

        ctx.fillRect(0, y - 250, cssW, 500);
      }
    }


    const draw = () => {
      t += 0.016;

      ctx.fillStyle = "#000700";
      ctx.fillRect(0, 0, cssW, cssH);

      drawPitch();
      drawAurora();
      drawMatrixRain();
      drawParticles();
      drawScanline();
    //   drawLightSweeps();

      animationId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 -z-10" />;
}