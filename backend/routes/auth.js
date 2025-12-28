const express = require("express");
const router = express.Router();

/*
⚠️ INTENTIONALLY VULNERABLE
- Plaintext credentials
- No hashing
- No rate limiting
- No sanitization
*/
router.post("/login", (req, res) => {
    const { username, password } = req.body;

    if (username === "admin" && password === "admin123") {
        return res.status(200).json({
            success: true,
            message: "Login successful"
        });
    }

    return res.status(401).json({
        success: false,
        message: "Invalid credentials"
    });
});

module.exports = router;
