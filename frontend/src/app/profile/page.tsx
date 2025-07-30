"use client"
import { useEffect, useState } from "react";
import Loading from "@/components/Loading/Loading";
import { fetchUserProfile, ProfileData } from "@/lib/api/profile";
import ProfilCardMain from "@/components/ProfilCardMain/ProfilCardMain";
import ProfilCardEmotion from "@/components/ProfilCardEmotion/ProfilCardEmotion";
import ProfilCardQuote from "@/components/ProfilCardQuote/ProfilCardQuote";
import Link from 'next/link'

export default function ProfilePage() {
  const [data, setData] = useState<ProfileData | null>(null);

  useEffect(() => {
    let attempts = 0;
    const maxAttempts = 5;
    const delay = 1500; 

    const fetchData = () => {
      const sessionId = localStorage.getItem('sessionId');
      if (!sessionId) {
        return;
      }

      fetchUserProfile(sessionId)
        .then(setData)
        .catch((e) => {
          if (attempts < maxAttempts && e.message.includes("404")) {
            attempts++;
            setTimeout(fetchData, delay);
          }
        });
    };

    fetchData();

    return () => {
      attempts = maxAttempts + 1; 
    };
  }, []);

  return (
    <>
      {!data && <Loading />}
      {data && (
        <>
          <h1 className="sm:text-5xl text-[24px] Sfpro-medium text-center mt-[100px] mb-4 col-span-12">Émotions dominantes de ta musique</h1>
          <h2 className="sm:text-xl text-sm text-center text-gray-666 px-[32px] mb-12 col-span-12">Chaque couleur reflète une facette de ton univers sonore. Voici ce qu’on y lit.</h2>

          <div className="flex gap-4 justify-center flex-wrap">
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
          <div className="w-full flex justify-center mt-12 mb-8">
            <Link
              href={"/"}
              className="px-6 py-4 bg-black text-white rounded-xl hover:bg-gray-800 transition max-w-[250px]"
            >
              Revenir à l’accueil
            </Link>
          </div>
          <p className="text-gray-300 text-xs relative bottom-2 left-[16px]">
            Design with <span className="text-red-400">♥</span> by <a href="https://www.instagram.com/kitana.ht/" target="_blank" className="underline hover:text-white">Kitana</a> & developed by <a href="https://jefferson-k.com" target="_blank" className="underline hover:text-white">Jefferson.K</a>
          </p>
        </>
      )}
    </>
  );
}