<script lang="ts">
    const serverHost = "http://localhost:5000/";
    let username = $state("");
    let password = $state("");
    let buttonText = $state("Log in");
    let disallowSubmit = $state(false);
    let errortext = $state("");

    async function submitLogin(event: SubmitEvent) {
        event.preventDefault();
        if (disallowSubmit)
            return;
        disallowSubmit = true;
        buttonText = "Please wait...";
        errortext = "";

        const requestBody = JSON.stringify({
            username: username,
            password: password
        });
        const response = await fetch(serverHost + "login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: requestBody
        }).catch((error) => {
            errortext = "HTTP error: " + error.message;
            buttonText = "Log in";
            disallowSubmit = false;
        });
        if (!response)
            return;

        const responseData = await response.json();
        console.log(responseData); // Log response to console for testing

        if (responseData.success) {
            // No place to redirect to yet. Just say "success".
            buttonText = "Success!";
        } else {
            errortext = "Error: " + responseData.error;
            buttonText = "Log in";
            disallowSubmit = false;
        }
    }
</script>

<div class="login-container">
    <h1>Log in to BrainBatch</h1>
    <p>Don't have an account yet? <a href="/createaccount">Create one!</a></p>
    <form id="form" onsubmit={submitLogin}>
        <div class="form-field">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required bind:value={username}>
        </div>
        <div class="form-field">
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required bind:value={password} minlength="8" maxlength="2048">
        </div>
        <small class="errortext" style="{errortext == '' ? 'display:none;' : ''}">{errortext}</small>
        <input type="submit" value={buttonText} disabled={disallowSubmit}>
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

    form input[type=submit]:disabled {
        background-color: #af2d00;
        cursor: not-allowed;
    }

    .errortext {
        color: red;
        text-align: center;
        margin: 0.5rem auto;
    }
</style>