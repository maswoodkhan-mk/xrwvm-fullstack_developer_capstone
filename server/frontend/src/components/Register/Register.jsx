import React, { useState } from 'react';
import './Register.css';

export default function Register() {
  const [form, setForm] = useState({
    userName: '',
    firstName: '',
    lastName: '',
    email: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);

  const update = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const submit = async (event) => {
    event.preventDefault();
    setMessage('');
    setBusy(true);

    try {
      const response = await fetch('/djangoapp/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || data.error || 'Registration failed.');
      }
      setMessage(data.message || data.status || 'Registration request completed.');
    } catch (error) {
      setMessage(error.message || 'Could not connect to the registration service.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="register_container">
      <h2>Register</h2>
      <form onSubmit={submit}>
        <label htmlFor="userName">Username</label>
        <input id="userName" name="userName" value={form.userName}
          onChange={update} autoComplete="username" required />

        <label htmlFor="firstName">First Name</label>
        <input id="firstName" name="firstName" value={form.firstName}
          onChange={update} autoComplete="given-name" required />

        <label htmlFor="lastName">Last Name</label>
        <input id="lastName" name="lastName" value={form.lastName}
          onChange={update} autoComplete="family-name" required />

        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" value={form.email}
          onChange={update} autoComplete="email" required />

        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" value={form.password}
          onChange={update} autoComplete="new-password" required />

        <button type="submit" disabled={busy}>
          {busy ? 'Registering…' : 'Register'}
        </button>
        {message && <p role="status">{message}</p>}
      </form>
    </main>
  );
}
