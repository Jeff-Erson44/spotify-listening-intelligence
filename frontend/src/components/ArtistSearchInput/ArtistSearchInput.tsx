'use client';

import Image from "next/image";
import './_style.scss'

interface Props {
  query: string;
  onChange: (value: string) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

export default function ArtistSearchInput({ query, onChange, onKeyDown }: Props) {
  return (
    <div className="container__artistSearchInput">
      <Image 
        src={"/icone/search.svg"}
        alt=""
        width={24}
        height={24}
      />
      <input
        type="text"
        placeholder="Michael Jackson"
        value={query}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={onKeyDown}
        className=""
      />
    </div>
  );
}