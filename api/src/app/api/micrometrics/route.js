import { connectDB } from "../../libs/mongodb";
import { NextResponse } from "next/server";
import Micrometric from "../../models/Micrometric";

export async function GET() {
  await connectDB();

  const micrometrics = await Micrometric.find({});

  return NextResponse.json(micrometrics);
}
