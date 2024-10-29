import { connectDB } from "../../libs/mongodb";
import { NextResponse } from "next/server";
import Tempcol from "../../models/Tempcol";

export async function GET() {
  await connectDB();

  const casts = await Tempcol.find({});

  return NextResponse.json(casts);
}


