import { useEffect, useState } from "react";
import { createSession } from "@/lib/api";

export function useSessionId (){
    const [sessionId, setSesssionId] = useState<string | null>(null);

    useEffect(() =>{
        const existingSessionId = localStorage.getItem("sessionId");
        if (existingSessionId) {
            setSesssionId(existingSessionId);
        }else{
            const fetchSession = async () => {
                const { sessionId } = await createSession();
                if (sessionId){
                    setSesssionId(sessionId);
                    localStorage.setItem("sessionId", sessionId)
                }
            };
            fetchSession();
        }
    }, [])
    return sessionId
}