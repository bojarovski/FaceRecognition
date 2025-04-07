const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const dotenv = require("dotenv");
const userRoutes = require("./routers/userRoutes");
const eventRoutes = require("./routers/eventRouters");

dotenv.config();
const app = express();
app.use(express.json());

// CORS setup with IP whitelist
const whitelist = process.env.WHITELIST_IPS.split(",");
app.use(cors());

// MongoDB connection
mongoose
  .connect(process.env.MONGO_URI)

  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log(err));

// Routes
app.use("/users", userRoutes);
app.use("/events", eventRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
