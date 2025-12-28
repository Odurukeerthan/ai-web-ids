const express = require("express");
const app = express();

const logger = require("./middleware/logger");
const authRoutes = require("./routes/auth");

app.use(express.json());
app.use(logger);                 // 🔥 IDS logging
app.use("/api/auth", authRoutes);

app.get("/", (req, res) => {
    res.json({ status: "Backend running" });
});

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});


