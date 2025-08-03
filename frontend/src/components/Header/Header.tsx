import ArtistCard from "../ArtistCard";
import Button from "../Button";
import './_style.scss'

export default function Header() {
    return (
        <div className="containerHeader">
            <div className="flex flex-col gap-4 pt-[250px] sm:gap-8">
                <h1 className="text-[32px] text-center tracking-[-1.6px] sm:text-6xl">Listening Intelligence</h1>
                <h2 className="text-center text-sm sm:text-xl">Ce que tu écoutes te définit. Visualise-le.</h2>
                <div className="flex gap-5 justify-center">
                    <Button
                    text="Générer mon profil musical"
                    mode="simulate"
                    variant="primary"
                    />
                </div>
            </div>
            <div className="containerHeader__artistCard">
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
        </div>
    )
}