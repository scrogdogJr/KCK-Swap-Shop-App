import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './Home.css';

function Home() {
  return (
    <Container className="mt-5">
      <Row className="align-items-center mb-5">
        <Col md={6}>
          <h1>Welcome to KCK Swap Shop</h1>
          <p className="lead">A community marketplace for buying, selling, and trading items locally.</p>
          <Button variant="primary" size="lg">
            Browse Items
          </Button>{' '}
          <Button variant="outline-primary" size="lg">
            List an Item
          </Button>
        </Col>
        <Col md={6} className="text-center">
          <div className="hero-placeholder">
            <i className="bi bi-shop"></i>
            <p>Hero Image / Placeholder</p>
          </div>
        </Col>
      </Row>

      <Row className="mt-5">
        <Col md={4} className="mb-4">
          <div className="feature-card">
            <div className="feature-icon">🛒</div>
            <h5>Easy Browsing</h5>
            <p>Browse through thousands of items in your community.</p>
          </div>
        </Col>
        <Col md={4} className="mb-4">
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h5>Connect</h5>
            <p>Message sellers and negotiate the best deals.</p>
          </div>
        </Col>
        <Col md={4} className="mb-4">
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h5>Secure</h5>
            <p>Safe transactions with verified community members.</p>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
