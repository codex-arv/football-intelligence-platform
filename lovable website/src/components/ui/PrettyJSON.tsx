import React, { useState } from "react";

interface JSONRendererProps {
  data: any;
  level?: number;
}

const PrettyJSON: React.FC<JSONRendererProps> = ({ data, level = 0 }) => {
  if (data === null || data === undefined) return null;

  const indent = "ml-" + level * 4;

  // If primitive value
  if (typeof data !== "object") {
    return <span className="text-gray-800">{String(data)}</span>;
  }

  // If array
  if (Array.isArray(data)) {
    return (
      <ul className={`list-disc ml-6`}>
        {data.map((item, index) => (
          <li key={index}>
            <PrettyJSON data={item} level={level + 1} />
          </li>
        ))}
      </ul>
    );
  }

  // If object
  return (
    <div className={`space-y-2 ${indent}`}>
      {Object.entries(data).map(([key, value]) => (
        <ExpandableItem key={key} label={key} value={value} level={level} />
      ))}
    </div>
  );
};

const ExpandableItem = ({
  label,
  value,
  level,
}: {
  label: string;
  value: any;
  level: number;
}) => {
  const [open, setOpen] = useState(false);
  const isObject = typeof value === "object" && value !== null;

  return (
    <div>
      <button
        onClick={() => isObject && setOpen(!open)}
        className="flex items-center gap-2 font-semibold text-blue-700 hover:text-blue-900"
      >
        {isObject && (
          <span className="text-sm">{open ? "▾" : "▸"}</span>
        )}
        <span>{label}</span>
      </button>

      {isObject ? (
        open && (
          <div className="ml-4 border-l pl-3 mt-2">
            <PrettyJSON data={value} level={level + 1} />
          </div>
        )
      ) : (
        <div className="ml-6 text-gray-800">{String(value)}</div>
      )}
    </div>
  );
};

export default PrettyJSON;