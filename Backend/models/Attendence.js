// Backend/models/Attendance.js
const mongoose = require("mongoose");

const AttendanceSchema = new mongoose.Schema({
  event: { type: mongoose.Schema.Types.ObjectId, ref: "Event", required: true },
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  seenAt: { type: Date, default: Date.now },
});

AttendanceSchema.index({ event: 1, user: 1 }, { unique: true });

module.exports = mongoose.model("Attendance", AttendanceSchema);
