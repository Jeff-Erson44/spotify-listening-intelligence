import Image from "next/image"

interface ArtistCardProps {
    src: string;
}
export default function ArtistCard({src}: ArtistCardProps) {
    return (
        <Image 
            src={src}
            height={300}
            width={300}
            alt="card artiste rihanna"
            className="object-cover rounded-lg border-[5px] border-[#E0E0E080]"
        />
    )
}