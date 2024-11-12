import mongoose from "mongoose";

const AnonymizationSchema = new mongoose.Schema({
  events: [],
  eventDetails: [],
});

export default mongoose.models.Anonymization ||
  mongoose.model("Anonymization", AnonymizationSchema);
