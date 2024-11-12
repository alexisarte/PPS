import { connectDB } from "../../../libs/mongodb";
import { NextResponse } from "next/server";
import ScreencastsWithEvents from "../../../models/ScreencastsWithEvents.js";

export async function GET(request, { params }) {
  try {
    await connectDB();
    const { id } = await params;

    if (!id) {
      return NextResponse.json({ error: "ID is required" }, { status: 400 });
    }

    const screencastWithEvents = await ScreencastsWithEvents.findById(id);

    if (!screencastWithEvents) {
      return NextResponse.json({ error: "screencastWithEvents not found" }, { status: 404 });
    }

    return NextResponse.json(screencastWithEvents);
  } catch (error) {
    return NextResponse.error({
      status: 500,
      message: error.message,
    });
  }
}
