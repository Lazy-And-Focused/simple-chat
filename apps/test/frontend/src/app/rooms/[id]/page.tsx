'use client'

import type { User } from "types/user.type";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { getToken } from "api/get-token";
import { getUser } from "api/get-user";

import styles from "./page.module.css";

const Page = () => {
  const [ socket, setSocket ] = useState<WebSocket|null>(null);
  const [ user, setUser ] = useState<User|null>(null);
  const [ loaded, setLoaded ] = useState<boolean>(false);
  const [ connected, setConnect ] = useState<boolean>(false);

  const [ messages, setMessages ] = useState<{
    author_id: number,
    author: string,
    text: string
  }[]>([]);

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
    <div className={styles.main}>
      <span>Привет, {user.username}, Вы подключены</span>
      <div className={styles.chat}>
        {
          messages.map(message => (
            <div className={`${styles.message} ${styles["message_" + `${message.author_id === user.id}`]}`}>
              <span>{message.author}: {message.text}</span>
            </div>
          ))
        }
      </div>
    </div>
  )
};

export default Page;
