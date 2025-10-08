'use server'

import { cookies } from "next/headers"

export const getToken = async () => {
  const cookie = await cookies();
  
  const value = cookie.get("auth")?.value
  
  if (!value) {
    return false;
  }

  const auth = JSON.parse(value);

  return auth.access_token;
}