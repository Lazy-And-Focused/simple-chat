'use client'

import { useRef, useState } from "react";

import { authenticate } from "api/authenticate";
import { CHOOSE_ROOM_PATH } from "api/constants";

import { ModalComponent } from "../components/modal.component";

import styles from "./page.module.css";

export default function Home() {
  const modalRef = useRef<HTMLDivElement>(null);

  return (
    <div className={"page"}>
      Привет, это приложение simple chat, хочешь зарегистрироваться?

      <ModalComponent
        ref={modalRef}
        summary={"Хочу"}
      >
        <div
          className={styles.modal}
          style={{display: "none"}}
          ref={modalRef}
        >
          <div className={styles.input}>
            <form className="auth" onSubmit={(e) => {
              e.preventDefault();
              const data = Object.fromEntries(new FormData(e.currentTarget).entries()) as {
                email: string,
                password: string,
                username: string
              };

              authenticate(data).then(() => {
                location.href = CHOOSE_ROOM_PATH;
              });
            }}>
              <input className="auth" name="email" placeholder="Введите свою почту" type="email" />
              <input className="auth" name="password" placeholder="Введите свой пароль" type="password" />
              <input className="auth" name="username" placeholder="Введите своё имя" type="text" />
              <input className="auth" type="submit" value="Готово" />
            </form>
          </div>
        </div>
      </ModalComponent>
    </div>
  );
}
