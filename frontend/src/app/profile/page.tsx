"use client"
import { useEffect, useState } from "react";
import { fetchUserProfile, ProfileData } from "@/lib/api/profile";
import ProfilCardMain from "@/components/ProfilCardMain/ProfilCardMain";
import ProfilCardEmotion from "@/components/ProfilCardEmotion/ProfilCardEmotion";
import ProfilCardQuote from "@/components/ProfilCardQuote/ProfilCardQuote";

export default function ProfilePage() {
  const [data, setData] = useState<ProfileData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let attempts = 0;
    const maxAttempts = 5;
    const delay = 1500; 

    const fetchData = () => {
      setError(null);
      const sessionId = localStorage.getItem('sessionId');
      console.log("Session ID from localStorage:", sessionId);
      if (!sessionId) {
        setError("Session ID not found in localStorage");
        return;
      }

      fetchUserProfile(sessionId)
        .then(setData)
        .catch((e) => {
          if (attempts < maxAttempts && e.message.includes("404")) {
            attempts++;
            setTimeout(fetchData, delay);
          } else {
            setError(e.message);
          }
        });
    };

    fetchData();

    return () => {
      attempts = maxAttempts + 1; 
    };
  }, []);

  if (error) {
    return <div>Erreur : {error}</div>;
  }

  if (!data) {
    return <div>Chargement des données, veuillez patienter...</div>;
  }

  return (
    <div className=""> 
      <h1 className="sm:text-5xl text-[24px] Sfpro-medium text-center mt-[100px] mb-4 col-span-12">Émotions dominantes de ta musique</h1>
      <h2 className="sm:text-xl text-sm text-center text-gray-666 px-[32px] mb-8 col-span-12">Chaque couleur reflète une facette de ton univers sonore. Voici ce qu’on y lit.</h2>

      <div className="flex gap-4 justify-center">
        <ProfilCardMain
          topGenres={data.top_3_genres}
          energie_moyenne={data.energie_moyenne}
          danse_moyenne={data.danse_moyenne}
          emotionColors={Object.values(data.emotion_colors)}
        />
        <div className=" flex flex-col justify-between">
          <ProfilCardEmotion
            top_3_emotions={data.top_3_emotions}
            emotion_colors={data.emotion_colors}
          />

          <ProfilCardQuote
            description={data.description_auto}
          />
        </div>
      </div>
    </div>
  );
}