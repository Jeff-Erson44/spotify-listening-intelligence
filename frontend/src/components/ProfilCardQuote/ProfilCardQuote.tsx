import './_style.scss'

interface Props {
    description: string;
}

export default function ProfilCardQuote({ description }: Props) {
    return(
        <div className="container_profileCardQuote bg-gray-11 w-[320px]">
            <p>{description}</p>
        </div>
    )
}