import Image from "next/image"

interface ArtistCardProps {
    src: string;
}
export default function ArtistCard({src}: ArtistCardProps) {
    return (
        <Image 
            src={src}
            height={320}
            width={320}
            alt="image d'un artiste pour illustrer le concept"
            className="object-cover rounded-lg border-[5px] border-[#E0E0E080] max-w-[200px] max-h-[200px] sm:max-w-[320px] sm:max-h-[320px]"
        />
    )
}