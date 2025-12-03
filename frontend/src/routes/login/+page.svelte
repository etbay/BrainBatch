<script>
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    let userData = {
        email: '',
        password: ''
    };

    let errorMessage = '';

    async function login(event) {
        event.preventDefault();

        try {
            const createAccountAttempt = await fetch('http://127.0.0.1:5000/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (createAccountAttempt.ok) {
                const result = await createAccountAttempt.json();
                if (result.success)
                {
                    console.log('Login successful.');

                    auth.set({
                        userId: result.data.id, 
                        isLoggedIn: true
                    });

                    goto('/profile');
                }
                else
                {
                    console.log('Incorrect email or password.');
                    errorMessage = 'Invalid email or password.';
                }
            } else {
                const error = await createAccountAttempt.json();
                console.log(`Error: ${error.message || 'Backend communication error.'}`);
            }
        } catch (e) {
            console.error('Error logging in:', e);
            alert('An unexpected error occurred. Please try again.');
        }
    }
</script>

<div class="login-container">
    <h1>Log in to BrainBatch</h1>
    <p>Don't have an account yet? <a href="/createaccount">Create one!</a></p>

    {#if errorMessage}
        <p style="color: red; text-align: center;">{errorMessage}</p>
    {/if}

    <form on:submit={login}>
        <div class="form-field">
            <label for="email">Email:</label>
            <input type="text" name="email" id="email" bind:value={userData.email} required>
        </div>
        <div class="form-field">
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" bind:value={userData.password} required>
        </div>
        <input type="submit" value="Log in" id="login">
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