'use server'

import type { User } from "types/user.type";

import { cookies } from "next/headers";
import { cache } from "react";

export const getUser = cache(async (token: string|null|false): Promise<User|null> => {
  const cookie = await cookies();
  
  if (!token) {
    const user = cookie.get("user")?.value;
    
    if (!user) {
      return null
    };
    
    return JSON.parse(user);
  };

  const user = await fetch("http://localhost:8000/api/user", {
    method: "GET",
    headers: {
      authorization: token
    },
    next: {
      revalidate: 300,
    },
    cache: "force-cache"
  }).then((data) => data.json());
  
  return user;
});