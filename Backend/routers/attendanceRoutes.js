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

    const result = await Attendance.updateOne(
      { event: eventId, user: user._id },
      { $setOnInsert: { seenAt: new Date() } },
      { upsert: true }
    );

    if (result.upsertedCount && result.upsertedCount > 0) {
      // New attendance inserted
      return res.status(201).json({ message: "Attendance recorded (new)" });
    } else {
      // Already exists
      return res.status(200).json({ message: "Already recorded" });
    }

  } catch (err) {
    console.error("Attendance by-name error:", err);
    return res.status(500).json({ error: err.message });
  }
});

router.post("/emotion-detected", async (req, res) => {
  try {
    const { eventId, name, emotion } = req.body;

    if (!eventId || !name || !emotion || !Array.isArray(emotion) || emotion.length === 0) {
      return res.status(400).json({ error: "eventId, name, and non-empty emotion array required" });
    }

    // Split full name into first name + surname
    const parts = name.trim().split(/\s+/);
    const first = parts.shift();
    const surname = parts.join(" ") || "";

    // Find the user
    const user = await User.findOne({ name: first, surname });
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // Find the most confident emotion
    const topEmotion = emotion.reduce((best, current) =>
      current.confidence > best.confidence ? current : best
    );

    // Update the attendance entry
    const updateResult = await Attendance.updateOne(
      { event: eventId, user: user._id },
      {
        $set: {
          emotion: {
            emotion: topEmotion.emotion,
            confidence: topEmotion.confidence,
          },
        },
      }
    );

    if (updateResult.matchedCount === 0) {
      return res.status(404).json({ error: "Attendance entry not found" });
    }

    console.log(`🎭 Updated emotion for ${name}:`, topEmotion);
    return res.sendStatus(200);
  } catch (err) {
    console.error("Emotion logging error:", err);
    return res.status(500).json({ error: err.message });
  }
});


module.exports = router;
