import './_style.scss'

interface Props {
  topGenres: string[];
  energie_moyenne: number;
  danse_moyenne: number;
  emotionColors: string[];
}

export default function ProfilCardMain({ topGenres, energie_moyenne, danse_moyenne, emotionColors }: Props){
    return (
        <div className="container__profilCard ">
            <div
              className='container__profilCard--circle'
              style={{
                backgroundImage: `linear-gradient(45deg, ${emotionColors[0]}, ${emotionColors[1]}, ${emotionColors[2]})`,
                animation: 'chaoticSpin 12s linear infinite',
              }}
            >
            </div>
            <div className='container__profilCard--session'>
                <p className='sfpro-medium'>Profil Card</p>
                <p className='sfpro-light text-xs'>#000 044</p>
            </div>
            <div className='container__profilCard--blurCard'>
                <div className='container__profilCard--blurCard__genre capitalize flex flex-col gap-2'>
                    <p className='text-[24px] text-gray-666'>{topGenres?.[0]}</p>
                    <p className='text-[18px] text-gray-666'>{topGenres?.[1]}</p>
                    <p className='text-[18px] text-gray-666'>{topGenres?.[2]}</p>
                </div>
                <div className='container__profilCard--blurCard__features'>
                    <p className='text-[12px] text-gray-666'>Énergie moyenne : {(energie_moyenne * 100).toFixed(1)}</p>
                    <p className='text-[12px] text-gray-666'>Dançabilité moyenne : {(danse_moyenne * 100).toFixed(1)}</p>
                </div>
            </div>
        </div>
    )
}