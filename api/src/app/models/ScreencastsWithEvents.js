import mongoose from "mongoose";

const ScreencastsWithEventsSchema = new mongoose.Schema({
  events: [],
  eventDetails: [],
});

export default mongoose.models.ScreencastsWithEvents || mongoose.model("ScreencastsWithEvents", ScreencastsWithEventsSchema);