<script>
    let userData = {
        username: '',
        display_name: '',
        email: '',
        password: ''
    };

    async function createAccount(event) {
        event.preventDefault();

        const createAccountAttempt = await fetch('http://127.0.0.1:5000/users/new_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (createAccountAttempt.ok) {
            const result = await createAccountAttempt.json();
            alert('Account created successfully!');
            console.log(result);
        } else {
            const error = await createAccountAttempt.json();
            alert(`Error: ${error.message}`);
        }
    }
</script>

<div class="login-container">
    <h1>Create a BrainBatch account</h1>
    <p>Already have an account? <a href="/login">Log in!</a></p>
    <form on:submit={createAccount}>
        <div class="form-field">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" bind:value={userData.username} pattern="\w&#123;3,24&#125;" required>
            <small>A 3 to 24 character name unique to your account. Can contain letters, numbers, and underscores.</small>
        </div>
        <div class="form-field">
            <label for="displayname">Display name:</label>
            <input type="text" name="displayname" id="displayname" bind:value={userData.display_name}>
            <small>Should be your real name or something others can identify you with.</small>
        </div>
        <div class="form-field">
            <label for="email">Email address:</label>
            <input type="email" name="email" id="email" bind:value={userData.email}>
            <small>BrainBatch can send you notifications via email.</small>
        </div>
        <div class="form-field">
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" bind:value={userData.password} minlength="8" maxlength="2048" required>
            <small>Passwords must be at least 8 characters long. A strong password contains an unpredictable sequence of letters, numbers, and symbols.</small>
        </div>
        <input type="submit" value="Create account">
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