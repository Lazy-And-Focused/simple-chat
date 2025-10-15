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
  const response = await fetch(process.env.API_ENV + "/api/auth", {
    method: "GET",
    headers: {
      email, password
    }
  });

  if (response.status === 200) {
    const auth = await response.json();

    cookie.set(process.env.COOKIE_TOKEN_NAME!, JSON.stringify(auth));
    return auth;
  }

  const code = await fetch(process.env.API_ENV + "/api/auth", {
    method: "POST",
    headers: {
      email, password
    },
    body: JSON.stringify({username})
  }).then(data => data.json());

  const authResponse = await fetch(process.env.API_ENV + "/api/auth?code="+code, {
    method: "GET"
  });

  if (authResponse.status !== 200) {
    throw new Error(authResponse.statusText);
  }

  const auth = await authResponse.json();

  cookie.set(process.env.COOKIE_TOKEN_NAME!, JSON.stringify(auth));

  return auth;
}