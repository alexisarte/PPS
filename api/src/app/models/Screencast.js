// models/Screencast.js
import mongoose from 'mongoose';

const ScreencastSchema = new mongoose.Schema({
  events: [],
  eventDetails: [],
});

export default mongoose.models.Screencast || mongoose.model('Screencast', ScreencastSchema);
