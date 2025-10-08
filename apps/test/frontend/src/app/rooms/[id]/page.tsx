'use client'

import type { User } from "types/user.type";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { getToken } from "api/get-token";
import { getUser } from "api/get-user";

const Page = () => {
  const [ socket, setSocket ] = useState<WebSocket|null>(null);
  const [ user, setUser ] = useState<User|null>(null);
  const [ loaded, setLoaded ] = useState<boolean>(false);
  const [ connected, setConnect ] = useState<boolean>(false);

  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    (async () => {
      const token = await getToken();
      const gettedUser = await getUser(token);
      
      if (!token || !gettedUser) {
        return;
      }

      const webSocket = new WebSocket(`ws://localhost:8000/api/rooms/${id}?authorization=${token}`);
      
      setSocket(webSocket);
      setUser(gettedUser);

      webSocket.addEventListener("open", () => {
        console.log("Connected");
        setConnect(true);
      });

      setLoaded(true);
    })();

    return () => {
      if (socket) {
        socket.removeEventListener("message", () => {});
        socket.removeEventListener("close", () => {});
        socket.removeEventListener("error", () => {});
        socket.removeEventListener("open", () => {});
      }
    }
  }, []);

  if (!connected || !loaded) {
    return (
      <div className="page">
        Загружаемся и подключаемся...
      </div>
    )
  }

  if (!user) {
    return (
      <div className="page">
        Пользователь не был найден, попробуй авторизоваться ещё раз
      </div>
    )
  }

  return (
    <div className="page">
      Привет, {user.username}, Вы подключены
    </div>
  )
};

export default Page;
