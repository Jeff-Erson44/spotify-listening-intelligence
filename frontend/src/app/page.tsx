'use client';
import ArtistCard from "@/components/ArtistCard";
import Button from "@/components/Button";

export default function Home() {
  return (
    <>
      <div className="flex flex-col gap-8 mt-[200px]">
        <h1 className="tracking-[-1.6px] text-6xl text-center">Spotify Listening Intelligence</h1>
        <h2 className="text-xl text-center">Ce que tu écoutes te définit. Visualise-le.</h2>
        <div className="flex gap-5 justify-center">
          <Button 
            text="Commencer avec Spotify"
            mode="spotify"
          />
          <Button
            text="Essayer sans compte"
            mode="simulate"
            variant="outline"
          />
        </div>
      </div>

      <div className="">
        <ArtistCard 
          src="/images/luciano.png"
        />
        <ArtistCard 
          src="/images/rihanna.png"
        />
        <ArtistCard 
          src="/images/freeze.png"
        />
      </div>
      
      

      <div className="app-grid">
        <div className="col-span-4 bg-red-100">Colonne 1 à 4</div>
        <div className="col-span-8 bg-green-100">Colonne 5 à 12</div>
        <div className="col-span-4 bg-blue-100">Colonne 13 à 16</div>
      </div>
    </>
  );
}