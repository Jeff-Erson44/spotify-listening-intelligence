"use client"
import { useRouter } from "next/navigation";
import { createSession } from "@/lib/api/create-session";

interface ButtonProps {
  text: string;
  mode: "spotify" | "simulate";
  variant?: "primary" | "outline";
}

export default function Button({ text, mode, variant ="primary" }: ButtonProps) {
  const router = useRouter();

  const handleClick = async () => {
    localStorage.removeItem("sessionId");
    const { sessionId } = await createSession();
    localStorage.setItem("sessionId", sessionId);
    router.push(mode === "spotify" ? "/spotify/login" : "/simulate");
  };

  const baseClasses = " w-[160px] text-xs rounded border border-black font-semibold transition duration-300 py-6 sm:w-[240px] sm:px-6 py-4";
  const variantClasses =
    variant === "primary"
      ? "bg-black text-white hover:bg-gray-800"
      : "bg-white text-black hover:bg-gray-300 hover:text-white hover:border-gray-300";

  return (
    <button
      onClick={handleClick}
      className={`${baseClasses} ${variantClasses}`}
    >
      {text}
    </button>
  );
}