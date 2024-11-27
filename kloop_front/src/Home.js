import React, { useState, useRef  } from 'react';
import axios from 'axios';
import './Home.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';



function Home({ onLogout }) {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false); 
    const [feedback, setFeedback] = React.useState(null);
    const fileInputRef = useRef(null); // Ref to reset file input

    const handleFeedback = async (type) => {
        setFeedback(type); // Update feedback state
        try {
            // Send feedback to the backend
            const res = await axios.post('http://localhost:5000/feedback', {
                feedback: type, 
                query,          
                response,      
            });

            alert(`Feedback "${type}" submitted successfully!`);
        } catch (err) {
            console.error(err);
            alert('Error submitting feedback.');
        }
    };

    // Handle file selection
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // Handle file upload (you could send the file to a server here)
    const handleFileUpload = async () => {
      if (file) {
          try {
            setIsUploading(true);
              // Create a FormData object to send the file
              const formData = new FormData();
              formData.append('file', file);

              // Send the file via a POST request
              await axios.post('http://localhost:5000/upload', formData, {
                  headers: {
                      'Content-Type': 'multipart/form-data',
                  },
              });
              alert('File Uploaded Successfully.');
              setFile(null);
              if (fileInputRef.current) {
                  fileInputRef.current.value = ''; // Clear the file input field
              }
          } catch (error) {
              console.error('Error uploading file:', error);
              alert('Error uploading file.');
          }
          finally {
            setIsUploading(false);
          }
      } else {
          alert('Please select a file to upload.');
      }
  };

    // Handle form submission
    const   handleSubmit = async (e) => {
        e.preventDefault();
        setResponse(''); // Clear previous response

        try {
            const res = await axios.post('http://localhost:5000/query', { query });
            setResponse(res.data.response);
        } catch (error) {
            console.error('Error fetching response:', error);
            setResponse('Error: Unable to fetch response');
        }
    };

    return (
        <div className="Home">
            {/* Navigation Bar */}
            <Navbar bg="light"  >
                <Container className='container_nav'>
                    <Navbar.Brand href="#home" className='navfont'>CORAS</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                    <div className="d-flex align-items-center ms-auto">
                    <Button variant="secondary" onClick={handleFileUpload} disabled={isUploading}>
                    {isUploading ? 'Uploading...' : 'Upload'}
                            </Button>
                           
                            <input
                                type="file"
                                onChange={handleFileChange}
                                ref={fileInputRef}
                                className="me-2"
                                style={{ display: 'inline-block' }}
                            />
                        <Button variant="outline-danger" onClick={onLogout} className="logout ms-auto">
                            Logout
                        </Button> {/* Logout button is now at the extreme right */}
                        </div>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

            {/* Main Content */}
            <Container className="content mt-4">
            <div className="product mb-4 p-3">
    <h3>Welcome to CORAS</h3>
    <p>
    CORAS is an intelligent tool that helps you quickly find important information from large, messy documents like PDFs and Excel files. It uses advanced technology to understand your 
    questions and give you clear, real-time answers, saving you time and improving productivity—perfect for making better decisions faster.
    </p>
</div>
                
                <Row className="justify-content-center">
                <h2>Query Assistant</h2>
                    <Col md={10} lg={20}> {/* Adjust width by changing md and lg sizes */}
                        <Form onSubmit={handleSubmit}>
                            <Form.Group controlId="queryTextarea" className="mb-3">
                                <Form.Label>Type your question here:</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    rows={4}
                                    cols={120}
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="Type your question here..."
                                    required
                                />
                            </Form.Group>
                            <Button variant="primary" type="submit">
                                Submit
                            </Button>
                        </Form>

                        {/* Display Response */}
                        {response && (
                            <div className="response mt-4 p-3 border rounded bg-light">
                                <h3>Response:</h3>
                                <p>{response}</p>
                                {/* Feedback Buttons */}
        <div className="feedback mt-3">
            <h5>Was this response helpful?</h5>
            <Button
                variant="success"
                className="me-2"
                onClick={() => handleFeedback('up')}
            >
                👍 Yes
            </Button>
            <Button
                variant="danger"
                onClick={() => handleFeedback('down')}
            >
                👎 No
            </Button>
        </div>
                            </div>
                        )}
                    </Col>
                </Row>
            </Container>

            {/* Footer */}
            <footer className="footer bg-dark text-center py-3 mt-3">
                <p>© 2024 CORAS. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default Home;
