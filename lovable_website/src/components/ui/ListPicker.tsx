"use client";
import { useEffect, useState, useRef } from "react";

type ListPickerProps<T extends string | number> = {
  title: string;
  items: T[];
  selected?: T | null;
  disabled?: boolean;
  placeholder?: string;
  onSelect: (value: T) => void;
};

export default function ListPicker<T extends string | number>({
  title,
  items,
  selected,
  disabled,
  placeholder = "Select from list",
  onSelect,
}: ListPickerProps<T>) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const wrapperRef = useRef<HTMLDivElement>(null);  
  const filtered = items.filter((item) =>
    item.toString().toLowerCase().includes(search.toLowerCase())
  );
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setOpen(false);
        setSearch("");
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);


  return (
    <div ref={wrapperRef} className="w-full flex flex-col items-center relative">
      <h3 className="text-xl font-semibold mb-4 italic">{title}</h3>

      {/* Trigger */}
      <button
        onClick={() => setOpen((s) => !s)}
        className="mb-3 px-4 py-3 rounded-xl bg-transparent
          hover:drop-shadow-[0_0_10px_rgba(255,255,255,0.4)]
          shadow-[0_0_20px_rgba(255,255,255,0.4)] text-sm"
      >
        {selected || "Select from List"} ▼
      </button>


      {/* Dropdown */}
      {open && !disabled && (
        <div className="absolute top-20 z-40 w-64 bg-black/70 backdrop-blur-xl border border-white/10 rounded-xl p-3">

          {/* Search */}
          <input
            className="w-full px-3 py-2 rounded-lg bg-white/10 outline-none text-sm mb-2"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          {/* Items */}
          <div className="max-h-56 overflow-y-auto pr-1">
            {filtered.map((item) => (
              <button
                key={item.toString()}
                onClick={() => {
                  onSelect(item);
                  setOpen(false);
                  setSearch("");
                }}
                className="w-full text-left px-3 py-2 rounded-lg text-sm mb-1 bg-white/10 hover:bg-white/20 transition-all"
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
