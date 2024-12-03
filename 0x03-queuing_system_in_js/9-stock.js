const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Create Express app
const app = express();
const port = 1245;

// List of products
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Create Redis client and promisify its methods
const client = redis.createClient();
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Function to get product by ID
function getItemById(id) {
  return listProducts.find(product => product.id === id);
}

// Function to reserve stock in Redis
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock from Redis
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0;
}

// Routes

// Route to list all products
app.get('/list_products', (req, res) => {
  const products = listProducts.map(({ id, name, price, stock }) => ({
    itemId: id,
    itemName: name,
    price: price,
    initialAvailableQuantity: stock,
  }));
  res.json(products);
});

// Route to get a specific product by ID
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currentReservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - currentReservedStock;

  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentQuantity,
  });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currentReservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - currentReservedStock;

  if (currentQuantity <= 0) {
    return res.status(400).json({
      status: 'Not enough stock available',
      itemId: itemId,
    });
  }

  // Reserve one item
  await reserveStockById(itemId, currentReservedStock + 1);

  res.json({
    status: 'Reservation confirmed',
    itemId: itemId,
  });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
