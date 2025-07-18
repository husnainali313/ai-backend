const express = require('express');
const fetch = require('node-fetch');
require('dotenv').config();
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/humanizer', async (req, res) => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'mistralai/mistral-7b-instruct',
        messages: [
          { role: 'system', content: 'Rewrite any robotic or AI-generated text into something natural and human-sounding' },
          { role: 'user', content: req.body.input }
        ]
      })
    });
    const data = await response.json();
    res.json(data.choices[0].message.content);
  } catch (err) {
    res.status(500).json({ error: 'Something went wrong' });
  }
});

app.post('/article-generator', async (req, res) => {
  // Similar to humanizer endpoint
});

app.post('/image-generator', async (req, res) => {
  try {
    const response = await fetch('https://api.replicate.com/v1/predictions', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${process.env.REPLICATE_API}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        version: "YOUR_REPLICATE_MODEL_VERSION", // Replace with correct version
        input: { prompt: req.body.prompt }
      })
    });
    const result = await response.json();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Image generation failed' });
  }
});

app.listen(process.env.PORT || 3000, () => {
  console.log('Server is running...');
});
