"use client";
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

export default function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    if ("scrollRestoration" in window.history) {
      window.history.scrollRestoration = "manual";
    }

    const scroll = () => {
      window.scrollTo(0, 0);
    };

    // Run AFTER render cycle (critical for iOS)
    requestAnimationFrame(() => {
      setTimeout(scroll, 0);
    });

  }, [pathname]);

  return null;
}
