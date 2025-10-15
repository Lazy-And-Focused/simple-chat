'use client'

import type { User } from "types/user.type";

import { useEffect, useRef, useState } from "react";

import { getToken } from "api/get-token";
import { getUser } from "api/get-user";
import { getRoomPath } from "api/constants";

import styles from "./page.module.css";

const Page = () => {
  const [ user, setUser ] = useState<User|null>(null);
  const [ token, setToken ] = useState<string|null>(null);
  
  const [ actived, setActived ] = useState<boolean>(false);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    (async () => {
      const gettedToken = await getToken();

      if (!gettedToken) {
        return;
      }

      setToken(gettedToken);
      setUser(await getUser(gettedToken));
    })();
  }, []);

  if (!user || !token) {
    return (
      <div className="page">
        Hello, I'm page
      </div>
    )
  }
  
  const handleJoinButton = () => {
    if (!modalRef.current) {
      return;
    }

    setActived(!actived);

    modalRef.current.style.display = !actived ? "flex" : "none";
  }

  return (
    <div className="page">
      Привет, я страница, а ты... {user.username}
      <button onClick={handleJoinButton}>Присоединиться</button>
      <div
        className={styles.modal}
        style={{display: "none"}}
        ref={modalRef}
      >
        <div className={styles.input}>
          <form onSubmit={(event) => {
            event.preventDefault();
            const id = new FormData(event.currentTarget).get("room") as string|null;

            if (!id) {
              throw new Error("No id");
            }

            location.href = getRoomPath(id);
          }}>
            <input name="room" type="number" placeholder="Введите номер комнаты" />
            <input type="submit" value={"Присоединиться"} />
          </form>
        </div>
      </div>
    </div>
  )
}

export default Page;
