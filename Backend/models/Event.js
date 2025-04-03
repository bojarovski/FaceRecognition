const mongoose = require("mongoose");
const EventSchema = new mongoose.Schema({
  name: String,
  startTime: Date,
  endTime: Date,
  participants: [{ type: mongoose.Schema.Types.ObjectId, ref: "User" }],
});
module.exports = mongoose.model("Event", EventSchema);
