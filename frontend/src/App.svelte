<script>
    import { onMount } from 'svelte';

    let todos = [];
    let newTask = '';
    let isLoading = true; // Track loading state
    let error = null; // Store potential errors

    const API_BASE_URL = 'http://127.0.0.1:5000/api'; // Your Flask API URL

    // Fetch initial todos when the component mounts
    onMount(async () => {
        isLoading = true;
        error = null;
        try {
            const response = await fetch(`${API_BASE_URL}/todos`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            todos = await response.json();
        } catch (e) {
            console.error("Error fetching todos:", e);
            error = "Could not load tasks. Please try again later.";
            todos = []; // Ensure todos is an empty array on error
        } finally {
            isLoading = false;
        }
    });

    // No longer need the localStorage reactive block:
    // $: if (typeof window !== 'undefined') { ... }

    async function addTodo() {
        const trimmedTask = newTask.trim();
        if (!trimmedTask) {
            return;
        }

        const optimisticTodo = { // Temporary ID for UI update
            id: `temp-${Date.now()}`,
            text: trimmedTask,
            completed: false
        };

        // Optimistic UI update (add immediately) - optional but improves UX
        // todos = [optimisticTodo, ...todos];
        // newTask = ''; // Clear input immediately

        try {
            const response = await fetch(`${API_BASE_URL}/todos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: trimmedTask }),
            });

            if (!response.ok) {
                 throw new Error(`HTTP error! status: ${response.status}`);
            }

            const newTodoFromServer = await response.json();

            // Replace optimistic add with real data OR add if not using optimistic update
            todos = [newTodoFromServer, ...todos.filter(t => t.id !== optimisticTodo.id)]; // Add the real one
            newTask = ''; // Clear input after successful add


        } catch (e) {
            console.error("Error adding todo:", e);
            error = "Failed to add task.";
            // Rollback optimistic update if it failed
            // todos = todos.filter(t => t.id !== optimisticTodo.id);
        }
    }

    async function toggleComplete(id) {
        const todoIndex = todos.findIndex(t => t.id === id);
        if (todoIndex === -1) return; // Should not happen

        const originalTodo = { ...todos[todoIndex] }; // Keep original state for rollback
        const updatedStatus = !originalTodo.completed;

        // Optimistic UI Update
        todos = todos.map(t => t.id === id ? { ...t, completed: updatedStatus } : t);

        try {
            const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
                method: 'PUT',
                 headers: {
                    'Content-Type': 'application/json',
                 },
                 body: JSON.stringify({ completed: updatedStatus }) // Send the desired state
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Optional: Update local state with response from server for consistency
            // const updatedTodoFromServer = await response.json();
            // todos = todos.map(t => t.id === id ? updatedTodoFromServer : t);

        } catch (e) {
            console.error("Error toggling todo:", e);
            error = "Failed to update task status.";
            // Rollback optimistic update
            todos = todos.map(t => t.id === id ? originalTodo : t);
        }
    }

    async function removeTodo(id) {
         const originalTodos = [...todos]; // Keep original state for rollback

         // Optimistic UI Update
         todos = todos.filter(todo => todo.id !== id);

        try {
            const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok && response.status !== 204) { // 204 No Content is success
                 throw new Error(`HTTP error! status: ${response.status}`);
            }
            // No need to update UI further if optimistic update was successful

        } catch (e) {
            console.error("Error removing todo:", e);
            error = "Failed to delete task.";
            // Rollback optimistic update
            todos = originalTodos;
        }
    }

    $: remainingTasks = todos.filter(todo => !todo.completed).length;

</script>

<main>
    <h1>Svelte To-Do App (with API)</h1>

    {#if isLoading}
        <p>Loading tasks...</p>
    {/if}

    {#if error}
        <p class="error-message">Error: {error}</p>
    {/if}

    <form on:submit|preventDefault={addTodo}>
        <input
            type="text"
            bind:value={newTask}
            placeholder="What needs to be done?"
            aria-label="New task input"
            disabled={isLoading}
        />
        <button type="submit" disabled={!newTask.trim() || isLoading}>Add Task</button>
    </form>

    {#if !isLoading && todos.length > 0}
        <ul class="todo-list">
            {#each todos as todo (todo.id)}
            <li class:completed={todo.completed}>
                <input
                    type="checkbox"
                    checked={todo.completed}
                    on:change={() => toggleComplete(todo.id)}
                    aria-label={`Mark ${todo.text} as complete`}
                 />
                <span class="todo-text">{todo.text}</span>
                <button
                    class="delete-btn"
                    on:click={() => removeTodo(todo.id)}
                    aria-label={`Delete task ${todo.text}`}
                >
                    ❌
                </button>
            </li>
            {/each}
        </ul>

        <p class="summary">
            {remainingTasks} {remainingTasks === 1 ? 'task' : 'tasks'} remaining
        </p>
    {:else if !isLoading && todos.length === 0}
        <p class="empty-state">No tasks yet! Add one above.</p>
    {/if}

</main>

<style>
    /* Add styles for loading and error states if desired */
    .error-message {
        color: red;
        text-align: center;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border: 1px solid red;
        background-color: #ffeeee;
        border-radius: 4px;
    }

    /* Keep existing styles from original component */
    main {
      max-width: 600px;
      margin: 2rem auto;
      padding: 1rem;
      font-family: sans-serif;
      background-color: #f9f9f9;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
      text-align: center;
      color: #333;
      margin-bottom: 1.5rem;
    }

    form {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
    }

    input[type="text"] {
      flex-grow: 1;
      padding: 0.75rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
    }

    button[type="submit"] {
      padding: 0.75rem 1rem;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.2s ease;
    }

    button[type="submit"]:hover:not(:disabled) {
      background-color: #0056b3;
    }

    button[type="submit"]:disabled {
      background-color: #aaa;
      cursor: not-allowed;
    }

    .todo-list {
      list-style: none;
      padding: 0;
      margin: 0 0 1.5rem 0;
    }

    li {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 0.5rem;
      border-bottom: 1px solid #eee;
      transition: background-color 0.2s ease;
    }

    li:last-child {
      border-bottom: none;
    }

    li:hover {
       background-color: #f0f0f0;
    }

    input[type="checkbox"] {
      cursor: pointer;
      width: 1.2em;
      height: 1.2em;
    }

    .todo-text {
      flex-grow: 1;
      word-break: break-word;
    }

    .completed .todo-text {
      text-decoration: line-through;
      color: #888;
    }

    .delete-btn {
      background: none;
      border: none;
      color: #ff4d4d;
      cursor: pointer;
      font-size: 1.1rem;
      padding: 0.2rem;
      margin-left: auto;
      transition: transform 0.2s ease;
    }

    .delete-btn:hover {
      transform: scale(1.1);
      color: #cc0000;
    }

    .summary {
      text-align: center;
      color: #555;
      font-size: 0.9rem;
      margin-top: 1rem;
    }

    .empty-state {
      text-align: center;
      color: #777;
      padding: 2rem 0;
    }
</style>