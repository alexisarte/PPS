import { connectDB } from "../../../libs/mongodb";
import { NextResponse } from "next/server";
import Tempcol from "../../../models/Tempcol";

export async function GET(request, { params }) {
  try {
    await connectDB();
    const { id } = await params;

    if (!id) {
      return NextResponse.json({ error: "ID is required" }, { status: 400 });
    }

    const tempcol = await Tempcol.findById(id);

    if (!tempcol) {
      return NextResponse.json({ error: "tempcol not found" }, { status: 404 });
    }

    return NextResponse.json(tempcol);
  } catch (error) {
    return NextResponse.error({
      status: 500,
      message: error.message,
    });
  }
}
