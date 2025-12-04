<script>
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcomeFallback from '$lib/images/svelte-welcome.png';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>Welcome to BrainBatch!</h1>
	<h2 class="tagline">The place to collaborate with your classmates</h2>
	<p>Log in or create an account above to get started.</p>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		text-align: center;
		text-transform: uppercase;
	}

	.tagline {
		font-style: italic;
		font-weight: 600;
		font-size: 1.25rem;
		margin-top: -1rem;
		margin-bottom: 2rem;
	}
</style>
