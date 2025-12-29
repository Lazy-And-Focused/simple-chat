'use client'

import type { RefObject } from "react";
import { useState } from "react";

type ListenerProps = {
  onChangeActive: (newActive: boolean) => unknown,
  overwriteListener?: boolean
} | {
  onChangeActive?: undefined,
  overwriteListener?: undefined
}

type Props = {
  ref: RefObject<HTMLDivElement | null>,
  children: React.ReactNode,
  summary: React.ReactNode,
  listenerProps?: ListenerProps
};

export const useModal = ({
  ref,
  children,
  summary,
  listenerProps
}: Props) => {
  const [ actived, setActived ] = useState<boolean>(false);

  const onClick = () => {
    listenerProps?.onChangeActive?.(!actived);

    if (!ref.current) {
      return;
    }

    setActived(!actived);

    ref.current.style.display = !actived ? "flex" : "none";
  };

  return {
    state: { actived, setActived },
    listeners: { onClick },
    component: (
      <>
        <button onClick={listenerProps?.overwriteListener
          ? () => (listenerProps.onChangeActive(!actived))
          : onClick
        }>{summary}</button>
        {children}
      </>
    )
  }
};

export const ModalComponent = (props: Props) => useModal(props).component;