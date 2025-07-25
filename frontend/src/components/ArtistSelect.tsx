import Image from "next/image";

interface ArtistSelectProps {
  imageSrc: string;
  altText?: string;
  size?: number;
}

export default function ArtistSelect({
  imageSrc,
  altText = "",
  size = 95,
}: ArtistSelectProps) {
  return (
    <Image
      src={imageSrc}
      alt={altText}
      width={size}
      height={size}
      className={`w-[${size}px] h-[${size}px] rounded-2xl backdrop-blur`}
      style={{
        boxShadow: "0px 4px 9.7px rgba(0, 0, 0, 0.25)",
        backdropFilter: "blur(2px)",
      }}
    />
  );
}