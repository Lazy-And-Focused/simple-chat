'use server'

import type { Auth } from "../types/auth.type";

import { cookies } from "next/headers";

export const authenticate = async ({
  email,
  password,
  username
}: {
  email: string,
  password: string,
  username: string
}): Promise<Auth> => {
  const cookie = await cookies();
  const response = await fetch("http://localhost:8000/api/auth", {
    method: "GET",
    headers: {
      email, password
    }
  });

  if (response.status === 200) {
    const auth = await response.json();

    cookie.set("token", JSON.stringify(auth));
    return auth;
  }

  const code = await fetch("http://localhost:8000/api/auth", {
    method: "POST",
    headers: {
      email, password
    },
    body: JSON.stringify({username})
  }).then(data => data.json());

  const auth = await fetch("http://localhost:8000/api/auth?code="+code, {
    method: "GET"
  }).then(data => data.json());

  cookie.set("token", JSON.stringify(auth));

  return auth;
}