'use client'

import type { User } from "types/user.type";
import type { Message } from "types/message.type";

import { useParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { getToken } from "api/get-token";
import { getUser } from "api/get-user";

import styles from "./page.module.css";

const resolveClassName = (authorId: number, userId: number) => {
  return authorId === userId
    ? "self_message"
    : "alien_message";
}

const Page = () => {
  const [ socket, setSocket ] = useState<WebSocket|null>(null);
  const [ user, setUser ] = useState<User|null>(null);
  const [ loaded, setLoaded ] = useState<boolean>(false);
  const [ connected, setConnect ] = useState<boolean>(false);

  const textRef = useRef<HTMLTextAreaElement>(null);
  const [ messages, setMessages ] = useState<Message[]>([
    {author: "Anon", author_id: 0, text: "Test"}
  ]);

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

      webSocket.addEventListener("message", (message) => {
        const data = JSON.parse(message.data) as Message;

        setMessages((previous) => [...previous, data]);
      })
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
      <div className={styles.chat_window}>
        <div className={styles.chat}>
          {
            messages.map((message, i) => (
              <div key={i} className={[
                styles.message,
                styles[resolveClassName(message.author_id, user.id)]
              ].join(" ")}>
                <span>{message.author}: {message.text}</span>
              </div>
            ))
          }
        </div>
        <form className={"message " + styles.input} onSubmit={(e) => {
          e.preventDefault();

          if (!socket || !textRef.current) {
            return;
          }

          socket.send(JSON.stringify({
            text: textRef.current.value,
            author: user.username,
            author_id: user.id
          }));

          textRef.current.value = "";
        }}>
          <textarea ref={textRef} placeholder="Введите сообщение" name="message"></textarea>
          <input type="submit" value="Готово" />
        </form>
      </div>
    </div>
  )
};

export default Page;
