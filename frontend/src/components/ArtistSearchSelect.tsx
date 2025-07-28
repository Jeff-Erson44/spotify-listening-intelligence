import Image from "next/image";

interface Artist {
  id: string;
  name: string;
  genres: string[];
  image?: string;
}

export default function ArtistSearchSelect({ artist,onSelect,}: {
  artist: Artist;
  onSelect: (artist: Artist) => void; }) {
  const genres = artist.genres.length > 0 ? artist.genres : ["pop"];

  return (
    <li
      className=" h-fit p-[16px] rounded-lg cursor-pointer transition flex border gap-4"
      onClick={() => onSelect(artist)}
    >
      <div className="flex justify-between items-center gap-4">
        {artist.image && artist.image.length > 0 && (
          <Image
            src={artist.image}
            alt={artist.name}
            width={40}
            height={40}
            className="w-[40px] h-[40px] rounded-xl object-cover"
          />
        )}
        </div>
        <div>
          <p className="font-bold">{artist.name}</p>
          <p className="text-sm text-gray-700">
            {genres.map((genre, idx) => (
              <span key={idx} className="after:content-[' '] last:after:content-none px-1">
                {genre}
              </span>
            ))}
          </p>
        </div>
      
    </li>
  );
}