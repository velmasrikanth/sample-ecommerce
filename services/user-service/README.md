User Service (Node.js/Express)

- Port: 5002
- Run:
  - Install deps: `npm install`
  - Run: `npm start`

Endpoints:
- `GET /health` : health check
- `GET /users` : list users
- `GET /users/:id` : get user
- `POST /users` : create user JSON `{ "name": "Alice", "email": "a@b.com" }`

Data stored in `users.json` in the service folder for simplicity.
