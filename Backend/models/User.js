const mongoose = require("mongoose");
const UserSchema = new mongoose.Schema({
  name: String,
  surname: String,
  email: String,
  image: String,
});
module.exports = mongoose.model("User", UserSchema);
