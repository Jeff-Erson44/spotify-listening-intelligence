import './_style.scss'

export default function ProfilCardEmotion () {
    return(
        <div className="container_profilCardEmotion bg-gray-11">
            <ul className="container_profilCardEmotion--list sfpro-light">
                <li>
                    <p className='text-gray-666'>#9C79D4</p>
                </li>
                <li className="container_profilCardEmotion--list__emotion">
                    <p>Mélancolie</p>
                    <span className='w-[50px]'></span>
                </li>
            </ul>
        </div>
    )
}