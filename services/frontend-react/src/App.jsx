import React, { useEffect, useState } from 'react'

const GATEWAY = import.meta.env.VITE_GATEWAY_URL || 'http://localhost:5000'

function fetchJSON(path, opts){
  return fetch(GATEWAY + path, opts).then(async r => {
    const txt = await r.text()
    try { return JSON.parse(txt) } catch(e){ return txt }
  })
}

export default function App(){
  const [products, setProducts] = useState([])
  const [users, setUsers] = useState([])
  const [orders, setOrders] = useState([])
  const [form, setForm] = useState({ pname:'', pprice:'', uname:'', uemail:'', ouser:'', oproduct:'', oqty:1 })

  useEffect(()=>{ loadAll() }, [])

  async function loadAll(){
    setProducts(await fetchJSON('/api/products'))
    setUsers(await fetchJSON('/api/users'))
    setOrders(await fetchJSON('/api/orders'))
  }

  async function createProduct(){
    if(!form.pname || !form.pprice) return alert('Provide product name and price')
    await fetchJSON('/api/products', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name: form.pname, price: parseFloat(form.pprice)}) })
    setForm({...form, pname:'', pprice:''})
    loadAll()
  }

  async function createUser(){
    if(!form.uname || !form.uemail) return alert('Provide user name and email')
    await fetchJSON('/api/users', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name: form.uname, email: form.uemail}) })
    setForm({...form, uname:'', uemail:''})
    loadAll()
  }

  async function createOrder(){
    const user_id = parseInt(form.ouser)
    const product_id = parseInt(form.oproduct)
    const quantity = parseInt(form.oqty)
    if(!user_id || !product_id || !quantity) return alert('Provide user, product and quantity')
    const res = await fetchJSON('/api/orders', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_id, product_id, quantity}) })
    if(res && res.error) return alert('Error: ' + JSON.stringify(res))
    setForm({...form, ouser:'', oproduct:'', oqty:1})
    loadAll()
  }

  return (
    <div style={{fontFamily:'Arial', padding:20}}>
      <h1>Sample E-commerce (React)</h1>
      <div style={{display:'flex', gap:20}}>
        <div style={{width:320}}>
          <h3>Products</h3>
          <input placeholder="name" value={form.pname} onChange={e=>setForm({...form, pname:e.target.value})} />
          <input placeholder="price" value={form.pprice} onChange={e=>setForm({...form, pprice:e.target.value})} />
          <button onClick={createProduct}>Create</button>
          <ul>{products && products.map(p=> <li key={p.id}>#{p.id} {p.name} - ${p.price}</li>)}</ul>
        </div>

        <div style={{width:320}}>
          <h3>Users</h3>
          <input placeholder="name" value={form.uname} onChange={e=>setForm({...form, uname:e.target.value})} />
          <input placeholder="email" value={form.uemail} onChange={e=>setForm({...form, uemail:e.target.value})} />
          <button onClick={createUser}>Create</button>
          <ul>{users && users.map(u=> <li key={u.id}>#{u.id} {u.name} - {u.email}</li>)}</ul>
        </div>

        <div style={{width:320}}>
          <h3>Create Order</h3>
          <input placeholder="user id" value={form.ouser} onChange={e=>setForm({...form, ouser:e.target.value})} />
          <input placeholder="product id" value={form.oproduct} onChange={e=>setForm({...form, oproduct:e.target.value})} />
          <input placeholder="quantity" value={form.oqty} onChange={e=>setForm({...form, oqty:e.target.value})} />
          <button onClick={createOrder}>Create Order</button>
          <ul>{orders && orders.map(o=> <li key={o.id}>#{o.id} user:{o.user_id} product:{o.product_id} qty:{o.quantity}</li>)}</ul>
        </div>
      </div>
    </div>
  )
}
