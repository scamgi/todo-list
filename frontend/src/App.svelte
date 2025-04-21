<script>
	import { onMount } from 'svelte';

	let todos = []; 
	let newTask = ''; 

	onMount(() => {
	  const storedTodos = localStorage.getItem('svelte-todos');
	  if (storedTodos) {
		try {
		  todos = JSON.parse(storedTodos);
		} catch (e) {
		  console.error("Error parsing todos from localStorage", e);
		  todos = []; 
		}
	  }
	});

	$: if (typeof window !== 'undefined') {
		localStorage.setItem('svelte-todos', JSON.stringify(todos));
	}

	function addTodo() {
	  const trimmedTask = newTask.trim(); 
	  if (!trimmedTask) {

		return;
	  }

	  todos = [
		{
		  id: Date.now(), 
		  text: trimmedTask,
		  completed: false
		},
		...todos 
	  ];
	  newTask = ''; 
	}

	function toggleComplete(id) {
	  todos = todos.map(todo => {
		if (todo.id === id) {
		  return { ...todo, completed: !todo.completed };
		}
		return todo;
	  });
	}

	function removeTodo(id) {
	  todos = todos.filter(todo => todo.id !== id);
	}

	$: remainingTasks = todos.filter(todo => !todo.completed).length;

  </script>

  <main>
	<h1>Svelte To-Do App</h1>
  <h1>TITOLO TEMPORANEO</h1>

	<form on:submit|preventDefault={addTodo}>
	  <input
		type="text"
		bind:value={newTask}
		placeholder="What needs to be done?"
		aria-label="New task input"
	  />
	  <button type="submit" disabled={!newTask.trim()}>Add Task</button>
	</form>

	{#if todos.length > 0}
	  <ul class="todo-list">
		{#each todos as todo (todo.id)}
		  <li class:completed={todo.completed}>
			<input
			  type="checkbox"
			  bind:checked={todo.completed}
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
	{:else}
	  <p class="empty-state">No tasks yet! Add one above.</p>
	{/if}

  </main>

  <style>
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
