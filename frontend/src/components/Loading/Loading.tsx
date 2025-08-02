"use client";
import React, { useEffect, useState } from "react";
import "./_style.scss";

export default function Loading() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => (prev < 100 ? prev + 1 : 100));
    }, 50); 
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-white">
      <h1 className="text-5xl font-bold relative overflow-hidden text-center animated-text">
        <span className="text-fill leading-[64px]">Listening Intelligence</span>
      </h1>
      <p className="mt-4 text-sm">{`Profil généré à ${progress}%`}</p>
    </div>
  );
}