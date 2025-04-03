// routes/userRoutes.js
const express = require("express");
const multer = require("multer");
const path = require("path");
const User = require("../models/User");
const router = express.Router();

const storage = multer.diskStorage({
  destination: "./uploads/",
  filename: (req, file, cb) => {
    cb(
      null,
      file.fieldname + "-" + Date.now() + path.extname(file.originalname)
    );
  },
});
const upload = multer({ storage });

// Create user
router.post("/", upload.single("image"), async (req, res) => {
  try {
    const { name, surname, email } = req.body;
    const image = req.file ? req.file.filename : "";
    const newUser = new User({ name, surname, email, image });
    await newUser.save();
    res.json(newUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET all users
router.get("/", async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
