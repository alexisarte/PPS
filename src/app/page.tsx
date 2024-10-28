"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [castsWithEvents, setCastsWithEvents] = useState([]);

  useEffect(() => {
    const fetchcastsWithEvents = async () => {
      const response = await fetch("/api/castsWithEvents");
      const data = await response.json();
      setCastsWithEvents(data);
    };

    fetchcastsWithEvents();
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>
          <h1>castsWithEvents</h1>
          <ul>
            {castsWithEvents.map((screencast, index) => (
              <li key={screencast._id} className="text-white">{index}. {screencast.eventDetails[0][0].values.data.text}</li>
            ))}
          </ul>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
