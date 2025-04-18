const http = require('http');
const fs = require('fs').promises;
const path = require('path');

const hostname = 'localhost';
const port = 3001; // You can choose a different port if needed

const server = http.createServer(async (req, res) => {
  console.log('Received request for:', req.url, 'Method:', req.method); // For debugging

  if (req.url === '/api/scraped_data' && req.method === 'GET') {
    try {
      const data = {};
      const rootDir = path.join(__dirname, '..', '..'); // Go up two levels to the root directory
      console.log('rootDir:', rootDir); // For debugging
      const files = await fs.readdir(rootDir);
      console.log('Files in rootDir:', files); // For debugging

      for (const file of files) {
        if (file.endsWith('.json')) {
          const query = file.replace('.json', '').replace('_', ' ');
          const filePath = path.join(rootDir, file);
          console.log('Attempting to read:', filePath); // For debugging
          const fileData = await fs.readFile(filePath, 'utf-8');
          data[query] = JSON.parse(fileData);
        }
      }

      console.log('Data being sent:', data); // Print the data object before sending the response

      res.setHeader('Content-Type', 'application/json');
      res.statusCode = 200;
      res.end(JSON.stringify(data));

    } catch (error) {
      console.error('Error reading JSON files:', error);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Failed to load scraped data' }));
    }
  } else {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Not Found');
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});