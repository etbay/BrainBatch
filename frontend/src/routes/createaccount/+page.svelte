<script>
    import { goto } from '$app/navigation';
    const BACKEND = 'http://localhost:8000';

    let username = '';
    let displayname = '';
    let email = '';
    let password = '';
    let error = '';
    let loading = false;

    async function onSubmit(e) {
        e.preventDefault();
        error = '';
        loading = true;
        try {
            const res = await fetch(`${BACKEND}/api/auth/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    password,
                    email,
                    display_name: displayname
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Registration failed');
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
    <h1>Create a BrainBatch account</h1>
    <p>Already have an account? <a href="/login">Log in!</a></p>
    <form on:submit|preventDefault={onSubmit}>
        <div class="form-field">
            <label for="username">Username</label>
            <input id="username" type="text" bind:value={username} required />
            <small>A 3 to 24 character name unique to your account. Can contain letters, numbers, and underscores.</small>
        </div>
        <div class="form-field">
            <label for="displayname">Display name</label>
            <input id="displayname" type="text" bind:value={displayname} />
        </div>
        <div class="form-field">
            <label for="email">Email</label>
            <input id="email" type="email" bind:value={email} />
            <small>BrainBatch can send you notifications via email.</small>
        </div>
        <div class="form-field">
            <label for="password">Password</label>
            <input id="password" type="password" bind:value={password} minlength="8" required />
            <small>Passwords must be at least 8 characters long. A strong password contains an unpredictable sequence of letters, numbers, and symbols.</small>
        </div>
        {#if error}<p style="color:red">{error}</p>{/if}
        <input type="submit" value={loading ? "Creating..." : "Create account"} disabled={loading} />
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