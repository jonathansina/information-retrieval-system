let firstQuery = true;
let retrieval_active = false;

document.addEventListener('DOMContentLoaded', event => {
	const form = document.getElementById('query-form');
	const queryInput = document.getElementById('query');
	const chathistory = document.querySelector('.history');

	const retrievalButton = document.querySelector('.retrieval_button');
	const retrievalResult = document.querySelector('retrieval_result');

	if (firstQuery) {
		firstQuery = false;

		form.addEventListener('submit', function (event) {
			event.preventDefault(); // Prevent the default form submission

			// Move the form to the bottom corner
			form.classList.add('moved');

			// Simulate initiating the chat
			chathistory.innerHTML = `<p>You submitted: ${queryInput.value}</p><p>Chat initiated...</p>`;
			chathistory.classList.add('history--active');

			// Optionally clear the input field
			queryInput.value = '';

			retrievalButton.classList.add('retrieval_button--active');
		});
	}

	// const socket = io('http://localhost:5000');

	// socket.on('ir_results', data => {
	// 	document.getElementById('ir-results').innerHTML = `<h2>IR Results:</h2><ul>${data.ir_results
	// 		.map(result => `<li>${result}</li>`)
	// 		.join('')}</ul>`;
	// });

	// socket.on('llm_response', data => {
	// 	document.getElementById(
	// 		'chatbot'
	// 	).innerHTML += `<h2>LLM Response:</h2><p>${data.llm_response}</p>`;
	// });

	// document.getElementById('query-form').addEventListener('submit', async e => {
	// 	e.preventDefault();
	// 	const query = document.getElementById('query').value;

	// 	const response = await fetch('/submit', {
	// 		method: 'POST',
	// 		headers: {
	// 			'Content-Type': 'application/json',
	// 		},
	// 		body: JSON.stringify({ query }),
	// 	});

	// 	if (!response.ok) {
	// 		console.error('Failed to submit query');
	// 	}
	// });
});
