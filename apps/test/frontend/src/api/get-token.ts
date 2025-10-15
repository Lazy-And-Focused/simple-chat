'use server'

import { cookies } from "next/headers"

export const getToken = async (): Promise<string|false> => {
  const cookie = await cookies();
  
  const value = cookie.get(process.env.COOKIE_TOKEN_NAME!)?.value
  
  if (!value) {
    return false;
  }

  const auth = JSON.parse(value);

  return auth.access_token;
}