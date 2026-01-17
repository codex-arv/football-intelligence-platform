"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface ExpandableTextProps {
  text: string;
  wordLimit?: number;
}

export default function ExpandableText({
  text,
  wordLimit = 150,
}: ExpandableTextProps) {
  const [expanded, setExpanded] = useState(false);

  const words = text.split(" ");
  const isTruncated = words.length > wordLimit;

  const previewText = words.slice(0, wordLimit).join(" ");
  const fullText = words.join(" ");

  return (
    <div className="text-lg text-white/90 font-lightbold leading-relaxed">
      <AnimatePresence initial={false}>
        <motion.p
        key={expanded ? "expanded" : "collapsed"}
        initial={{ opacity: 0, fontSize: "1.22rem" }}
        animate={{ opacity: 1, fontSize: "1.22rem" }}
        exit={{ opacity: 0 }}
        >

          {expanded || !isTruncated ? fullText : previewText}
          {!expanded && isTruncated && "..."}
        </motion.p>
      </AnimatePresence>

      {isTruncated && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="
            mt-2 text-m font-semibold text-white/90
            hover:text-white underline underline-offset-4
            transition-colors
          "
        >
          {expanded ? "Show less" : "See more"}
        </button>
      )}
    </div>
  );
}