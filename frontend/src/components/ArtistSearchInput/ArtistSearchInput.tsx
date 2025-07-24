'use client';

import Image from "next/image";
import './_style.scss';

interface Props {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function ArtistSearchInput({ value, onChange }: Props) {
  return (
    <div className="container__artistSearchInput">
      <Image 
        src={"/icone/search.svg"}
        alt=""
        width={24}
        height={24}
        priority
      />
      <input
        type="text"
        placeholder="Michael Jackson"
        value={value}
        onChange={onChange}
        className="ml-2 flex-1 bg-transparent placeholder-gray-400 focus:outline-none text-sm"
      />
    </div>
  );
}