import Link from "next/link";


export default function Navbar (){
    return (
        <nav className="px-16 py-2">
            <ul className="flex font-semibold justify-between items-center uppercase sfpro-medium text-xs tracking-[1.2px]">
                <li>
                    <Link href={"/"}>
                        Spotify<br/>Listening Intelligence
                    </Link>
                </li>
                <li>
                    <span aria-label="Spotify Listening Intelligence">SLI</span>
                </li>
                <li>
                    <Link href={"https://bento.me/jeffersonk"}>
                        @Jefferson.K
                    </Link>
                </li>
            </ul>
        </nav>
    )
}