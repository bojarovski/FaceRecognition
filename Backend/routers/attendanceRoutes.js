// routes/attendanceRoutes.js
const express = require("express");
const Attendance = require("../models/Attendence"); // corrected filename
const Event = require("../models/Event");
const User = require("../models/User");
const router = express.Router();

// Upsert attendance by userId (existing route)
router.post("/", async (req, res) => {
  try {
    const { eventId, userId } = req.body;
    if (!eventId || !userId) {
      return res.status(400).json({ error: "eventId and userId are required" });
    }

    const ev = await Event.findById(eventId);
    if (!ev) return res.status(404).json({ error: "Event not found" });

    await Attendance.updateOne(
      { event: eventId, user: userId },
      { $setOnInsert: { seenAt: new Date() } },
      { upsert: true }
    );

    return res.sendStatus(200);
  } catch (err) {
    if (err.code === 11000) return res.sendStatus(200);
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
});

// List all attendance entries for an event
router.get("/event/:id", async (req, res) => {
  try {
    const rows = await Attendance.find({ event: req.params.id })
      .populate("user", "name surname email image")
      .sort({ seenAt: 1 });
    return res.json(rows);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
});

// Post attendance by recognized name
router.post("/by-name", async (req, res) => {
  try {
    const { eventId, name } = req.body;
    if (!eventId || !name) {
      return res.status(400).json({ error: "eventId and name are required" });
    }

    const ev = await Event.findById(eventId);
    if (!ev) return res.status(404).json({ error: "Event not found" });

    const parts = name.trim().split(/\s+/);
    const first = parts.shift();
    const surname = parts.join(" ") || "";

    let user = await User.findOne({ name: first, surname });
    if (!user) {
      user = await User.create({ name: first, surname, email: "", image: "" });
    }

    await Attendance.updateOne(
      { event: eventId, user: user._id },
      { $setOnInsert: { seenAt: new Date() } },
      { upsert: true }
    );

    return res.sendStatus(200);
  } catch (err) {
    console.error("Attendance by-name error:", err);
    return res.status(500).json({ error: err.message });
  }
});

module.exports = router;
