'use client'

import type { User } from "types/user.type";

import { useEffect, useRef, useState } from "react";

import { getToken } from "api/get-token";
import { getUser } from "api/get-user";

import styles from "./page.module.css";

const Page = () => {
  const [ user, setUser ] = useState<User|null>(null);
  const [ token, setToken ] = useState<string|null>(null);
  
  const [ actived, setActive ] = useState<boolean>(false);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    (async () => {
      const t = await getToken();

      if (!t) {
        return;
      }

      setToken(t);
      setUser(await getUser(t));
    })();
  }, []);

  if (!user || !token) {
    return (
      <div className="page">
        Hello, I'm page
      </div>
    )
  }

  return (
    <div className="page">
      Привет, я страница, а ты... {user.username}
      <button
        onClick={() => {
          if (!modalRef.current) {
            return;
          }

          setActive(!actived);

          modalRef.current.style.display = !actived ? "flex" : "none";
        }}
      >Присоединиться</button>

      <div
        className={styles.modal}
        style={{display: "none"}}
        ref={modalRef}
      >
        <div className={styles.input}>
          <form onSubmit={(e) => {
            e.preventDefault();
            const id = Object.fromEntries(new FormData(e.currentTarget).entries())["room"];

            location.href = ("/rooms/" + id);
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
