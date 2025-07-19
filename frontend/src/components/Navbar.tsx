import Link from "next/link";


export default function Navbar (){
    return (
        <nav className="bg-red-50">
            <ul className="flex justify-between items-center uppercase sfpro-medium text-xs tracking[10%]">
                <li>
                    <Link href={"/"}>
                        Spotify<br/>Listening Intelligence
                    </Link>
                </li>
                <li>
                    <span aria-label="Spotify Listening Intelligence">SLI</span>
                </li>
                <li>
                    <Link href={"/"}>
                        @Jefferson.K
                    </Link>
                </li>
            </ul>
        </nav>
    )
}