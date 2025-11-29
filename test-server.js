require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 3001; // Use different port for testing

app.use(cors());
app.use(express.json());

app.get('/test', (req, res) => {
  res.json({ message: 'Test server works!' });
});

const server = app.listen(PORT, () => {
  console.log(`✅ Test server running on http://localhost:${PORT}/test`);
});

// Keep alive
setInterval(() => {
  console.log('Server still alive...');
}, 5000);
