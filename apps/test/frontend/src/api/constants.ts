export const ROOMS_ROUTE = "/rooms";
export const CHOOSE_ROOM_PATH = "/choose-room";

export const getRoomPath = (id: number|string) => `${ROOMS_ROUTE}/${id}`;