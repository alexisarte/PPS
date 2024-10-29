"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [castsWithEvents, setCastsWithEvents] = useState([]);
  const [minimumCastsWithEvents, setMinimumCastsWithEvents] = useState([]);

  useEffect(() => {
    const fetchcastsWithEvents = async () => {
      const response = await fetch("/api/castsWithEvents");
      const data = await response.json();
      setCastsWithEvents(data.eventDetails);
    };

    const fetchMinimumCastsWithEvents = async () => {
      const response = await fetch("/api/castsWithEvents/5efb293884fd56d072653bac");
      const data = await response.json();
      setMinimumCastsWithEvents(data.eventDetails);
    }

    // fetchMinimumCastsWithEvents();
    // fetchcastsWithEvents();
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>
          <h1>castsWithEvents</h1>
          {
            // <ul>
            //   {minimumCastsWithEvents.map((screencast) => (
            //     <li key={screencast._id}>
            //       {
            //         screencast.map((event, index) => (
            //           <span key={event._id} className="text-white">{index}:{event.values.data.text}  </span>
            //         ))
            //       }
            //     </li>
            //   ))}
            // </ul>
          }
          {/* <ul>
            {castsWithEvents.map((screencast, index) => (
              <li key={screencast._id} className="text-white">{index}. {screencast.values.data.text}</li>
            ))}
          </ul> */}
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
