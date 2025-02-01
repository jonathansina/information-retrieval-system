// src/app/pages/index.js
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Adjust URL as needed

export default function Home() {
	const [query, setQuery] = useState('');
	const [irResults, setIrResults] = useState([]);
	const [llmResponse, setLlmResponse] = useState('');

	const handleSubmit = async e => {
		e.preventDefault();
		const response = await fetch('/api/submit', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ query }),
		});
		if (!response.ok) {
			console.error('Failed to submit query');
		}
	};

	useEffect(() => {
		socket.on('ir_results', data => {
			setIrResults(data.ir_results);
		});

		socket.on('llm_response', data => {
			setLlmResponse(data.llm_response);
		});

		return () => {
			socket.off('ir_results');
			socket.off('llm_response');
		};
	}, []);

	return (
		<div>
			<h1>Query Submission</h1>
			<form onSubmit={handleSubmit}>
				<input
					type="text"
					value={query}
					onChange={e => setQuery(e.target.value)}
					placeholder="Enter your query"
				/>
				<button type="submit">Submit</button>
			</form>

			<h2>IR Results:</h2>
			<ul>
				{irResults.map((result, index) => (
					<li key={index}>{result}</li>
				))}
			</ul>

			<h2>LLM Response:</h2>
			<p>{llmResponse}</p>
		</div>
	);
}
