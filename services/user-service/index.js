const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const DATA_FILE = path.join(__dirname, 'users.json');

function loadUsers() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw || '[]');
  } catch (e) {
    return [];
  }
}

function saveUsers(users) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(users, null, 2), 'utf8');
}

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.get('/users', (req, res) => {
  const users = loadUsers();
  res.json(users);
});

app.get('/users/:id', (req, res) => {
  const users = loadUsers();
  const u = users.find(x => String(x.id) === req.params.id);
  if (!u) return res.status(404).json({ error: 'not found' });
  res.json(u);
});

app.post('/users', (req, res) => {
  const { name, email } = req.body || {};
  if (!name || !email) return res.status(400).json({ error: 'name and email required' });
  const users = loadUsers();
  const id = users.length ? Math.max(...users.map(u => u.id)) + 1 : 1;
  const u = { id, name, email };
  users.push(u);
  saveUsers(users);
  res.status(201).json(u);
});

const PORT = process.env.PORT || 5002;
app.listen(PORT, '0.0.0.0', () => console.log(`User service listening on ${PORT}`));
