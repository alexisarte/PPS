import { connectDB } from "../../libs/mongodb";
import { NextResponse } from "next/server";
import ScreencastsWithEvents from "../../models/ScreencastsWithEvents.js";

export async function GET() {
  await connectDB();

  const casts = await ScreencastsWithEvents.find({});

  return NextResponse.json(casts);
}


