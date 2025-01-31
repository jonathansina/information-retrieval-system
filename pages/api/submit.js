// pages/api/submit.js
export default async function handler(req, res) {
	if (req.method === 'POST') {
		try {
			const response = await fetch('http://localhost:5000/submit', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(req.body),
			});

			const data = await response.json();
			res.status(response.status).json(data);
		} catch (error) {
			console.log(error);
			res.status(500).json({ error: 'Failed to submit query' });
		}
	} else {
		res.status(405).json({ error: 'Method not allowed' });
	}
}
