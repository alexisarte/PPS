// models/Screencast.js
import mongoose from 'mongoose';

const ScreencastSchema = new mongoose.Schema({
  events: [],
  eventDetails: [],
});

export default mongoose.models.Screencastsevent || mongoose.model('Screencastsevent', ScreencastSchema);
