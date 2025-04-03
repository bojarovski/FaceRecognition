// routes/eventRoutes.js
const express = require("express");
const Event = require("../models/Event");
const router = express.Router();

// Create event
router.post("/", async (req, res) => {
  try {
    const { name, startTime, endTime } = req.body;
    const newEvent = new Event({ name, startTime, endTime, participants: [] });
    await newEvent.save();
    res.json(newEvent);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET all events
router.get("/", async (req, res) => {
  try {
    const events = await Event.find();
    res.json(events);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Join event
router.post("/:eventId/join/:userId", async (req, res) => {
  try {
    const { eventId, userId } = req.params;
    const event = await Event.findById(eventId);
    if (!event) return res.status(404).json({ error: "Event not found" });
    if (!event.participants.includes(userId)) {
      event.participants.push(userId);
      await event.save();
    }
    res.json(event);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get event participants (Admin Panel View)
router.get("/:eventId", async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId).populate(
      "participants"
    );
    if (!event) return res.status(404).json({ error: "Event not found" });
    res.json(event);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
