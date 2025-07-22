import Image from "next/image"

export default function ArtistSelect() {
    return (
        <Image 
            src={'/images/freeze.png'}
            alt=""
            width={95}
            height={95}
            className="w-[95px] h-[95px] rounded-2xl backdrop-blur"
            style={{
                boxShadow: '0px 4px 9.7px rgba(0, 0, 0, 0.25)',
                backdropFilter: 'blur(2px)',
            }}
        />
    )
}