const fs = require("fs");
const path = require("path");

module.exports = (req, res, next) => {
    const startTime = Date.now();

    res.on("finish", () => {
        const logEntry = {
            timestamp: new Date().toISOString(),
            ip: req.ip,
            method: req.method,
            url: req.originalUrl,
            status: res.statusCode,
            payloadSize: JSON.stringify(req.body || {}).length,
            userAgent: req.headers["user-agent"],
            responseTimeMs: Date.now() - startTime
        };

        fs.appendFileSync(
            path.join(__dirname, "../logs/requests.log"),
            JSON.stringify(logEntry) + "\n"
        );
    });

    next();
};
