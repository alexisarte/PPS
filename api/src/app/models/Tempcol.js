import mongoose from "mongoose";

const TempcolSchema = new mongoose.Schema({
  events: [],
  eventDetails: [],
});

export default mongoose.models.Tempcol || mongoose.model("Tempcol", TempcolSchema);