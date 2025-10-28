<script>
    import { goto } from '$app/navigation';
    const BACKEND = 'http://localhost:8000';

    let username = '';
    let password = '';
    let error = '';
    let loading = false;

    async function onSubmit(e) {
        e.preventDefault();
        error = '';
        loading = true;
        try {
            const res = await fetch(`${BACKEND}/api/auth/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Login failed');
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            goto('/profile');
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="login-container">
    <h1>Log in to BrainBatch</h1>
    <p>Don't have an account yet? <a href="/createaccount">Create one!</a></p>
    <form on:submit|preventDefault={onSubmit}>
        <div class="form-field">
            <label for="username">Username:</label>
            <input id="username" type="text" bind:value={username} required />
        </div>
        <div class="form-field">
            <label for="password">Password:</label>
            <input id="password" type="password" bind:value={password} required />
        </div>
        {#if error}<p style="color:red">{error}</p>{/if}
        <input type="submit" value={loading ? "Logging in..." : "Log in"} disabled={loading} />
    </form>
</div>

<style>
    .login-container {
        background-color: #fff;
        width: 600px;
        max-width: 100%;
        margin: 1rem auto;
        padding: 2rem;
        border: 1px solid #808080;
        border-radius: 1rem;
    }

    .login-container h1, .login-container p {
        text-align: center;
        margin: 1rem;
    }

    form {
        margin: 2rem auto;
        max-width: 400px;
    }

    .form-field {
        margin-bottom: 1rem;
    }

    .form-field label {
        display: block;
        margin-bottom: 0.5rem;
    }

    .form-field input {
        display: block;
        padding: 0.75rem;
        width: 100%;
        border: 1px solid #808080;
        border-radius: 6px;
    }

    form input[type=submit] {
        display: block;
        margin: 1rem auto;
        background-color: #ff3e00;
        color: #fff;
        font-size: 1.25em;
        font-weight: bold;
        padding: 0.5em 1em;
        border: none;
        border-radius: 6px;
    }

    form input[type=submit]:hover {
        cursor: pointer;
        box-shadow: #912501 3px 3px;
    }
</style>