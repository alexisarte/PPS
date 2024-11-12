import { connectDB } from "../../libs/mongodb";
import { NextResponse } from "next/server";
import Anonymization from "../../models/Anonymization.js";

export async function GET() {
  await connectDB();

  const anonymizations = await Anonymization.find({});

  return NextResponse.json(anonymizations);
}
