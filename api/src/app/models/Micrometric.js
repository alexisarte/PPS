import mongoose from "mongoose";

const MicrometricSchema = new mongoose.Schema({
  logs: [],
});

export default mongoose.models.Micrometric ||
  mongoose.model("Micrometric", MicrometricSchema);
