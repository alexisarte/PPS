import { connectDB } from "../../libs/mongodb";
import { NextResponse } from "next/server";
import Screencast from "../../models/Screencastevent.js";

export async function GET() {
  await connectDB();

  const casts = await Screencast.find({});

  return NextResponse.json(casts);
}


