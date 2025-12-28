const fs = require("fs");
const path = require("path");

module.exports = (req, res, next) => {
    const startTime = Date.now();

    res.on("finish", () => {
        const payload=JSON.stringify(req.body || "");
        const logEntry = {
            timestamp: new Date().toISOString(),
            ip: req.ip,
            method: req.method,
            url: req.originalUrl,
            status: res.statusCode,
            payloadSize: payload.length,
            payloadSnippet:payload.slice(0,200),
            userAgent: req.headers["user-agent"],
            responseTimeMs:Date.now() - startTime
        };

        const logPath = path.join(__dirname, "../logs/requests.log");
        const logLine = JSON.stringify(logEntry) + "\n";
        fs.appendFileSync(logPath, logLine, { encoding: "utf8" });

    });

    next();
};
