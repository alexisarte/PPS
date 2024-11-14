import mongoose from "mongoose";

const AnonymizationSchema = new mongoose.Schema({
  logs: [],
});

export default mongoose.models.Anonymization ||
  mongoose.model("Anonymization", AnonymizationSchema);
