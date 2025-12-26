const express = require('express');
const app = express();
app.use(express.json());
app.get('/',(req,res)=>{
  res.json({
    status:"OK",
    message:"Backend running inside Kali Linux"
  });
});
app.listen(3000,()=>{
  console.log("Server running on port 3000");
});

