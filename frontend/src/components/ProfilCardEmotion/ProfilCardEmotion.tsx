import './_style.scss'

const hexEmotionColors: Record<string, string> = {
  joie: "#FDD835",
  détente: "#A3D5FF",
  enthousiasme: "#FFB74D",
  motivation: "#FF7043",
  envieDeDanser: "#4DB6AC",
  excitation: "#D81B90",
  tristesse: "#7986CB",
  colère: "#EF5350",
  mélancolie: "#B39DDB",
  nostalgie: "#F3C6F1",
  neutre: "#B0BEC5",
  confiance: "#81C784"
};

interface Props {
  top_3_emotions: string[];
  emotion_colors: Record<string, string>;
}

export default function ProfilCardEmotion({ top_3_emotions, emotion_colors }: Props) {
    return(
        <div className="container_profilCardEmotion bg-white h-fit w-[320px] mb-4">
            <ul className="container_profilCardEmotion--list sfpro-light flex-col">
                {top_3_emotions.map((emotion, index) => (
                    <li key={index} className="flex justify-between items-center py-2 border-b border-white/10">
                      <span className="text-sm text-gray-500 w-1/3">{hexEmotionColors[emotion]}</span>
                      <span className="text-sm font-medium w-1/3 text-center">{emotion}</span>
                      <span className="w-[36px] h-[24px] rounded-full w-1/3" style={{ backgroundColor: emotion_colors[emotion] || hexEmotionColors[emotion] || 'black' }}></span>
                    </li>
                ))}
            </ul>
        </div>
    )
}