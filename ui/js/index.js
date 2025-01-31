let firstQuery = true;
let retrieval_active = false;

document.addEventListener('DOMContentLoaded', event => {
	const form = document.getElementById('query-form');
	const queryInput = document.getElementById('query');
	const chathistory = document.querySelector('.history');
	let query = '';

	const retrievalButton = document.querySelector('.retrieval_button');
	const retrievalResult = document.querySelector('.retrieval_result');

	form.addEventListener('submit', function (event) {
		event.preventDefault(); // Prevent the default form submission
		query = queryInput.value;
		queryInput.value = '';

		if (firstQuery) {
			form.classList.add('moved');
			retrievalButton.classList.add('retrieval_button--active');
			chathistory.classList.add('history--active');

			firstQuery = !firstQuery;
		}

		chathistory.innerHTML += `<p class="message user_message">${query}</p>`;
	});

	retrievalButton.addEventListener('click', () => {
		retrievalResult.classList.toggle('retrieval_result--active');
	});

	const socket = io('http://localhost:5000');

	socket.on('ir_results', data => {
		retrievalButton.classList.toggle('retrieval_button--rotate');
		retrievalResult.innerHTML = `${data.ir_results
			.map(result => `<div class="retrieved_item">${result}</div>`)
			.join('')}`;
	});

	socket.on('llm_response', data => {
		chathistory.innerHTML += `<p class="message agent_message">${data.llm_response}</p>`;
	});

	form.addEventListener('submit', async e => {
		e.preventDefault();
		console.log(query);

		const response = await fetch('/submit', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ query }),
		});

		if (!response.ok) {
			console.error('Failed to submit query');
		}
	});
});
