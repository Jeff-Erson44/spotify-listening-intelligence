import './style.scss'

export default function ProfilCardMain(){
    return (
        <div className="container__profilCard">
            <div className='container__profilCard--circle           bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500'>
            </div>
            <div className='container__profilCard--session'>
                <p className='sfpro-medium'>Profil Card</p>
                <p className='sfpro-light text-xs'>#000 044</p>
            </div>
            <div className='container__profilCard--blurCard'>
                <div className='container__profilCard--blurCard__genre'>
                    <p className='text-2xl'>Rap</p>
                    <p className='text-xl'>Pop</p>
                    <p className='text-xl'>Rap Cloud</p>
                </div>
                <div className='container__profilCard--blurCard__features'>
                    <p className='text-xs'>Énergie moyenne :</p>
                    <p className='text-xs'>Dançabilité moyenne :</p>
                </div>
            </div>
        </div>
    )
}