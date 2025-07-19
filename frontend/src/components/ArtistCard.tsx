import Image from "next/image"

export default function ArtistCard() {
    return (
            <Image 
                src="/images/rihanna.png"
                height={300}
                width={300}
                alt="card artiste rihanna"
                className="rounded-lg border-[5px] border-black"
        />
    )
}