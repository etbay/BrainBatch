<script>
    import { onMount } from "svelte";
    
    async function foo()
    {
        console.log("Hello");

        const userId = "400f395c-fc85-45d4-a884-883d33d18291";
        const res = await fetch("http://localhost:5000/users/get_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: userId })
        });

        const result = await res.json()
        console.log(result);
    }
</script>

<div class="login-container">
    <h1>Log in to BrainBatch</h1>
    <p>Don't have an account yet? <a href="/createaccount">Create one!</a></p>
    <form>
        <div class="form-field">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required>
        </div>
        <div class="form-field">
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required>
        </div>
<<<<<<< Updated upstream
        <input type="submit" value="Log in">
=======
        <button onclick={foo}>Log In</button>
>>>>>>> Stashed changes
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