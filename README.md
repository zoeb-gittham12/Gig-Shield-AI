# Gig-Shield-AI
AI-powered parametric insurance for delivery workers

## Inspiration

Delivery workers are crucial to India's gig economy, but they often lose income due to factors beyond their control, such as heavy rain, extreme heat, pollution, and curfews. This motivated us to create a solution that safeguards their daily earnings using AI and automation.

## What it does

GigShield AI is an AI-powered insurance platform that provides automatic compensation to delivery workers for income loss caused by environmental disruptions. Instead of going through manual claims, payouts occur automatically based on real-time data, like weather conditions and location.

## How we built it

We developed a system that includes a mix of frontend, backend, and AI-based logic:

Frontend: Mobile/Web interface for onboarding and user dashboard
Backend: API system for managing user data, claims, and payouts
AI/ML: Models for predicting risk and detecting fraud 
APIs: Weather API, location tracking, and mock payment integration 

We also set up a multi-layer anti-spoofing system that uses behavioral analysis, device data, and anomaly detection to stop GPS spoofing fraud. 

## Adversarial Defense & Anti-Spoofing Strategy

### The Differentiation
Our system goes beyond basic GPS checks by using AI-driven behavioral analysis to tell apart real delivery workers and fraudsters. Genuine users display natural movement patterns, consistent delivery activity, and varying speeds. In contrast, spoofers show unusual behaviors like sudden location jumps, staying in one place, or identical patterns between multiple users. 

We give each user a Fraud Risk Score based on their behavior in comparison to historical data and city-wide patterns.

### The Data
Instead of relying only on GPS, we gather data from various sources:

Location data (GPS and network triangulation) 
Device fingerprinting (to identify emulators or spoofing tools) 
Motion sensors (using accelerometers to confirm movement) 
App activity logs (delivery acceptance and active time) 
External APIs (for weather and traffic checks) 
Crowd comparison (to check consistency with nearby workers) 

### The UX Balance
To ensure fairness, we do not immediately reject suspicious claims: 

Low-risk claims lead to instant payouts. 
Medium-risk claims result in delayed payouts with light verification. 
High-risk claims are flagged for fraud investigation. 

This process ensures that genuine workers are not punished due to network issues or real disruptions.

### Anti-Spoofing Techniques

Detection of sudden GPS jumps (>5 km instantly)
No movement despite active delivery claims
Identical claim patterns across multiple users (syndicate detection)
Multi-sensor validation (GPS + motion + network)

### Key Innovation
Our platform moves from simple GPS-based trust to AI-driven multi-layer verification, making large-scale coordinated fraud very difficult.

## Challenges we ran into

Creating a fair system that prevents false claims while protecting honest users 
Dealing with GPS spoofing and organized fraud attacks 
Balancing automation with user trust and openness 
Developing a pricing model that can scale effectively


## Accomplishments that we're proud of

Developed a complete insurance concept tailored for gig workers 
Designed an AI-based strategy for detecting fraud and preventing spoofing 
Created a no-contact claims system with instant payouts 
Tackled real-world issues like syndicate fraud and data validation


## What we learned

How parametric insurance operates in real-life situations 
The significance of AI in detecting fraud and assessing risk 
How to design user-friendly and secure systems 
How to manage real-world issues like network failures and spoofing


## What's next for Gig-Shield AI

Build a working prototype with real API integration 
Enhance AI models using real-world data 
Collaborate with delivery platforms like Zomato and Swiggy 
Expand services to other gig workers, such as drivers and freelancers
