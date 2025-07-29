import Link from "next/link";


export default function Navbar (){
    return (
        <nav className="fixed top-0 left-0 w-screen px-8 sm:px-16 py-2 z-50">
            <ul className="flex font-semibold justify-between items-center uppercase sfpro-medium text-[10px] tracking-[1.2px] sm:text-xs">
                <li>
                    <Link href={"/"}>
                        Spotify<br/>Listening Intelligence
                    </Link>
                </li>
                <li>
                    <span 
                        aria-label="Spotify Listening Intelligence"
                        className="hidden sm:block"
                    >SLI</span>
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