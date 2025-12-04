<svelte:head>
	<title>Canvas</title>
	<meta name="description" content="Link Canvas Account" />
</svelte:head>

<script>
    let accessToken = '';
    let courses = [];
    let error = '';

    async function linkCanvasAccount() {
        error = '';
        courses = [];
<<<<<<< Updated upstream
        const res = await fetch('http://localhost:8000/api/canvas/courses/', {
=======
        const res = await fetch('http://localhost:5173/api/canvas/courses/', {
>>>>>>> Stashed changes
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ access_token: accessToken })
        });
        if (res.ok) {
            courses = await res.json();
        } else {
            const data = await res.json();
            error = data.error || 'Failed to fetch courses';
        }
    }
</script>

<div class="text-column" style = "text-align: center;">
	<h1>Link Canvas account</h1>

    <label for = "accessToken">Enter Canvas Access Token:</label>
    <input style="width: auto;" type = "text" bind:value={accessToken}/><br/>
    <button style= "margin: 1rem 0; padding: 0.75rem 1.5rem; font-size: 1.1rem;"
		on:click={linkCanvasAccount}>
		Link Canvas Account
	</button>
	{#if error}
        <p style="color: red;">{error}</p>
    {/if}
	{#if courses.length}
		<h2>Your Courses:</h2>
		<ul>
			{#each courses as course}
				<li>{course.name}</li>
			{/each}
		</ul>
	{/if}
</div>
