<script>
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    let groups = [];
    let joinableGroups = [];
    let loading = true;
    let error = '';
    let newGroupName = '';

    async function verifyLogin() {
        if (!$auth.isLoggedIn)
        {
            goto('/login');
            return;
        }

        loadGroups();
        loadJoinableGroups();
    }

    async function loadGroups() {
        if (!$auth.isLoggedIn)
        {
            console.error('Error: No user logged in');
            loading = false;
            return;
        }

        loading = true;
        error = '';

        try {
            const res = await fetch('http://127.0.0.1:5000/groups/get_all_groups', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: $auth.userId })
            });
            const response = await res.json();
            console.log('Groups data:', response);
            if (!res.ok) throw new Error(response.error || 'Failed to load groups');
            groups = Array.isArray(response.data) ? response.data : [response.data];
        } catch (e) {
            console.error('Error:', e);
            error = e.message;
        } finally {
            loading = false;
        }
    }

    async function loadJoinableGroups() {
        console.log("Loading joinable groups...");
        if (!$auth.isLoggedIn) {
            console.error('Error: No user logged in');
            return;
        }

        try {
            const res = await fetch('http://127.0.0.1:5000/groups/get_joinable_groups', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: $auth.userId })
            });

            // Check if the response is JSON
            const contentType = res.headers.get('Content-Type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Invalid response format');
            }

            const response = await res.json();
            console.log('Joinable groups data:', response);

            if (!res.ok || response.error) {
                throw new Error(response.error || 'Failed to load joinable groups');
            }

            joinableGroups = Array.isArray(response.data) ? response.data : [];
            console.log("Joinable groups loaded:", joinableGroups);
        } catch (e) {
            console.error('Error:', e);
            error = e.message;
        }
    }

    async function createGroup() {
        if (!$auth.userId)
        {
            console.error('Error: No user logged in');
            return;
        }

        if (!newGroupName.trim()) return;
        const res = await fetch('http://127.0.0.1:5000/groups/new_group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                group_name: newGroupName.trim(),
                creator_id: $auth.userId
            })
        });
        const data = await res.json();
        if (!res.ok) {
            error = data.error || 'Failed to create';
            return;
        }
        console.log('Group created:', data);
        await loadGroups();
    }

    async function joinGroup(groupId) {
        if (!$auth.userId) {
            console.error('Error: No user logged in');
            return;
        }

        try {
            const res = await fetch('http://127.0.0.1:5000/groups/add_member', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    group_id: groupId,
                    user_id: $auth.userId
                })
            });
            const data = await res.json();
            if (!res.ok) {
                error = data.error || 'Failed to join group';
                return;
            }
            console.log('Joined group:', data);
            await loadGroups();
            await loadJoinableGroups();
        } catch (e) {
            console.error('Error:', e);
            error = e.message;
        }
    }

    onMount(verifyLogin);
</script>

<h1>Your Groups</h1>
{#if error}<p style="color:red">{error}</p>{/if}

<div style="margin: 0.5rem 0;">
    <input placeholder="New group name" bind:value={newGroupName} />
    <button on:click={createGroup}>Create</button>
</div>

{#if loading}
    <p>Loading…</p>
{:else}
    <ul>
        {#each groups as g}
            <li><a href={`/groups/${g.id}`}>{g.name}</a></li>
        {:else}
            <p>No groups found. Create one to get started!</p>
        {/each}
    </ul>
{/if}

<h2>Joinable Groups</h2>
{#if joinableGroups.length > 0}
    <ul>
        {#each joinableGroups as group}
            <li>
                {group.name}
                <button on:click={() => joinGroup(group.id)}>Join</button>
            </li>
        {/each}
    </ul>
{:else}
    <p>No joinable groups available.</p>
{/if}