import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const allData = {};
        const queries = [
          'headphones',
          'smartphones',
          'wireless_earbuds',
          'bluetooth_speakers',
          'laptop',
          'smartwatch',
          'tablet',
          'camera',
          'gaming_console',
          'e-reader',
        ];

        for (const query of queries) {
          try {
            const response = await fetch(`/data/${query.replace(' ', '_')}.json`);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status} for ${query}`);
            }
            const jsonData = await response.json();
            allData[query] = jsonData;
          } catch (fetchError) {
            console.error(`Error fetching data for ${query}:`, fetchError);
            setError(error || fetchError); // Set error if not already set
          }
        }
        setData(allData);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading scraped data...</div>;
  }

  if (error) {
    return <div>Error loading data: {error.message}</div>;
  }

  return (
    <div className="App">
      <h1>Amazon Scraped Data</h1>
      {Object.keys(data).map((query) => (
        <div key={query}>
          <h2>{query.replace('_', ' ').toUpperCase()}</h2>
          {data[query] && data[query].length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Reviews</th>
                  <th>Price</th>
                  <th>Image</th>
                  <th>Scrape Date</th>
                </tr>
              </thead>
              <tbody>
                {data[query].map((product, index) => (
                  <tr key={index}>
                    <td>{product.title}</td>
                    <td>{product.total_reviews}</td>
                    <td>{product.price}</td>
                    <td>
                      {product.image_url && (
                        <img
                          src={product.image_url}
                          alt={product.title}
                          style={{ maxWidth: '100px', maxHeight: '100px' }}
                        />
                      )}
                    </td>
                    <td>{product.scrape_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No products found for {query.replace('_', ' ').toUpperCase()}.</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default App;