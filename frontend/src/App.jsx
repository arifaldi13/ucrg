import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 
import { GithubIcon } from './GithubIcon'; 

function App() {
  const [inputData, setInputData] = useState('{\n  "incident_type": "Power Surge",\n  "location": "Data Center West",\n  "duration": "2 seconds",\n  "resolved": true\n}');
  const [report, setReport] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerateReport = async () => {
    setIsLoading(true);
    setReport('');
    setError('');

    try {
      const jsonData = JSON.parse(inputData);
      const response = await axios.post(
        'https://rifukawa-ucrg.hf.space/generate-report',
        jsonData,
        { headers: { 'Content-Type': 'application/json' } }
      );
      setReport(response.data.report_text);
    } catch (err) {
      console.error(err);
      if (err.response) {
        setError(`API Error: ${err.response.data.error || err.response.statusText}`);
      } else if (err.request) {
        setError('Network Error: Could not connect to the API server.');
      } else if (err.message.includes('JSON.parse')) {
        setError('Input Error: Please provide valid JSON.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>⚡️ Utility Compliance Report Generator (UCRG)</h1>
      <p>Enter structured incident data as JSON to generate a natural-language summary.</p>
      
      <div className="form-group">
        <label htmlFor="jsonData">Input Data (JSON)</label>
        <textarea
          id="jsonData"
          rows="10"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder='{ "incident_type": "...", "location": "..." }'
        />
      </div>

      <button onClick={handleGenerateReport} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate Report'}
      </button>

      {error && (
        <div className="result-box error-box">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {report && (
        <div className="result-box success-box">
          <h3>Generated Report</h3>
          <p>{report}</p>
        </div>
      )}

      <div className="about-section">
	  
	  
        <div className="about-column">
          <h3>About This Project</h3>
          <p>
            This project is a proof-of-concept demonstrating a full-stack AI application. It showcases my ability to fine-tune a Large Language Model (LLM) for a specific, structured-data-to-text task, build a REST API for inference, and create a user-friendly frontend.
          </p>
        </div>
		
        <div className="about-column">
          <h3>Technology Stack</h3>
          <ul>
            <li><strong>Model:</strong> Fine-tuned TinyLlama-1.1B</li>
            <li><strong>ML/Backend:</strong> Python, Flask, PyTorch, Hugging Face</li>
            <li><strong>Frontend:</strong> React.js, Vite, Axios</li>
            <li><strong>Deployment:</strong> Hugging Face Spaces with free CPU</li>
          </ul>
        </div>
		

		<div className="about-column">
		  <h3>Potential & Future Vision</h3>
		  <p>
			While this is a small-scale demo, the underlying technology has significant potential for any industry that relies on data-driven reporting. With more robust data and resources, this system could be scaled to:
		  </p>
		  <ul>
			<li>
			  <strong>Automate Regulatory Compliance:</strong> Automatically generate thousands of daily, weekly, or monthly compliance reports for sectors like energy, finance, and healthcare, saving countless hours of manual work and reducing human error.
			</li>
			<li>
			  <strong>Enhance Operational Awareness:</strong> Instantly translate sensor data, system logs, or incident tickets into plain-language summaries for managers and executives, enabling faster and more informed decision-making.
			</li>
			<li>
			  <strong>Improve Customer Communication:</strong> Automatically create clear, concise updates for customers during service outages or other incidents, improving transparency and satisfaction.
			</li>
		  </ul>
		  <p className="limitation-note">
			<strong>Acknowledge Limitations:</strong> The current model is a proof-of-concept and may occasionally make errors, particularly with complex or ambiguous inputs. A production-grade system would require a larger, more varied training dataset and rigorous validation to ensure near-perfect accuracy. This process of iterative improvement is a core part of developing real-world AI solutions.
		  </p>
		</div>
		
		<a href="https://github.com/arifaldi13/ucrg" target="_blank" rel="noopener noreferrer" className="github-button">
          <GithubIcon />
          <span>View on GitHub</span>
        </a>
		
      </div>
	  
    </div>
  );
}

export default App;