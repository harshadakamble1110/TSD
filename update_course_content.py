"""
Update course structure with theory for core concepts and video for advanced concepts
"""
import os
import sys
import json

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Course, CourseTopic

def get_theory_content(topic_title, category_name):
    """Generate theory content for core concepts"""
    theory_content = {
        "Web Development": {
            "Core Concepts": """
# Core Concepts in Web Development

## HTML5 Semantic Elements
HTML5 introduced semantic elements that clearly describe their meaning to both the browser and developer.

### Key Semantic Elements:
- **<header>**: Defines a header for a document or section
- **<nav>**: Defines navigation links
- **<main>**: Specifies the main content of a document
- **<article>**: Defines independent, self-contained content
- **<section>**: Defines a section in a document
- **<aside>**: Defines content aside from the main content
- **<footer>**: Defines a footer for a document or section

### Benefits:
- Better SEO optimization
- Improved accessibility
- Cleaner code structure
- Easier maintenance

## CSS3 Advanced Selectors
CSS3 provides powerful selectors for precise element targeting.

### Selector Types:
- **Attribute Selectors**: Target elements based on attributes
- **Pseudo-classes**: Style elements based on state
- **Pseudo-elements**: Style specific parts of elements
- **Combinators**: Combine selectors for complex targeting

### Example:
```css
/* Attribute selector */
input[type="text"] {
    border: 1px solid #ccc;
}

/* Pseudo-class */
button:hover {
    background-color: #007bff;
}

/* Pseudo-element */
p::first-line {
    font-weight: bold;
}
```

## JavaScript Fundamentals
JavaScript is the programming language of the web.

### Core Concepts:
- **Variables**: `let`, `const`, `var`
- **Data Types**: Numbers, strings, booleans, objects, arrays
- **Functions**: Reusable blocks of code
- **DOM Manipulation**: Interacting with HTML elements
- **Event Handling**: Responding to user actions

### Example:
```javascript
// Variable declaration
const message = "Hello, World!";

// Function
function greet(name) {
    return `Hello, ${name}!`;
}

// DOM manipulation
document.getElementById('output').textContent = greet('Student');
```

## Responsive Design Principles
Responsive design ensures websites work on all devices.

### Key Techniques:
- **Fluid Grids**: Use percentages instead of fixed pixels
- **Flexible Images**: Images that scale with the container
- **Media Queries**: CSS rules for different screen sizes
- **Mobile-First Approach**: Design for mobile first, then scale up

### Media Query Example:
```css
/* Mobile styles (default) */
.container {
    width: 100%;
    padding: 10px;
}

/* Tablet styles */
@media (min-width: 768px) {
    .container {
        width: 750px;
        margin: 0 auto;
    }
}

/* Desktop styles */
@media (min-width: 1200px) {
    .container {
        width: 1170px;
    }
}
```

## Best Practices
- Write semantic HTML
- Use CSS efficiently
- Optimize JavaScript performance
- Ensure accessibility
- Test across browsers
- Follow web standards
            """,
            "Advanced Concepts": """
# Advanced Web Development Concepts

## Modern JavaScript Frameworks
Modern frameworks simplify complex web application development.

### Popular Frameworks:
- **React**: Component-based UI library by Facebook
- **Vue.js**: Progressive JavaScript framework
- **Angular**: Full-featured framework by Google

### React Example:
```jsx
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}
```

## Backend Development with Node.js
Node.js enables JavaScript server-side development.

### Key Concepts:
- **Express.js**: Web application framework
- **RESTful APIs**: Architectural style for web services
- **Database Integration**: MongoDB, MySQL, PostgreSQL
- **Authentication**: JWT, OAuth, sessions

### Express.js Example:
```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// Routes
app.get('/api/users', (req, res) => {
    // Fetch users from database
    res.json(users);
});

app.post('/api/users', (req, res) => {
    // Create new user
    const user = createUser(req.body);
    res.status(201).json(user);
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## Database Integration
Databases store and manage application data.

### Types of Databases:
- **SQL**: Relational databases (MySQL, PostgreSQL)
- **NoSQL**: Document databases (MongoDB)
- **ORM**: Object-Relational Mapping (Sequelize, Mongoose)

### MongoDB Example:
```javascript
const mongoose = require('mongoose');

// Schema definition
const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    age: Number,
    createdAt: {
        type: Date,
        default: Date.now
    }
});

// Model creation
const User = mongoose.model('User', userSchema);

// CRUD operations
async function manageUsers() {
    // Create
    const user = new User({
        name: 'John Doe',
        email: 'john@example.com',
        age: 25
    });
    await user.save();
    
    // Read
    const users = await User.find();
    
    // Update
    await User.updateOne(
        { email: 'john@example.com' },
        { age: 26 }
    );
    
    // Delete
    await User.deleteOne({ email: 'john@example.com' });
}
```

## API Design and Development
APIs enable communication between different software systems.

### RESTful API Principles:
- **Stateless**: Each request contains all necessary information
- **Resource-based**: URLs represent resources
- **HTTP Methods**: GET, POST, PUT, DELETE for operations
- **Status Codes**: Indicate success/failure

### API Example:
```javascript
// GET /api/users - Retrieve all users
app.get('/api/users', async (req, res) => {
    try {
        const users = await User.find();
        res.json({
            success: true,
            data: users,
            count: users.length
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// POST /api/users - Create new user
app.post('/api/users', async (req, res) => {
    try {
        const user = new User(req.body);
        await user.save();
        res.status(201).json({
            success: true,
            data: user
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
});
```

## Deployment Strategies
Deployment makes applications available to users.

### Deployment Options:
- **Shared Hosting**: Basic, cost-effective option
- **VPS Hosting**: More control and resources
- **Cloud Platforms**: AWS, Google Cloud, Azure
- **PaaS**: Heroku, Netlify, Vercel

### Docker Deployment:
```dockerfile
# Dockerfile
FROM node:14-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### CI/CD Pipeline:
- **Continuous Integration**: Automated testing and building
- **Continuous Deployment**: Automated release process
- **Tools**: GitHub Actions, Jenkins, GitLab CI

## Security Best Practices
Security protects applications and user data.

### Key Security Measures:
- **Input Validation**: Prevent injection attacks
- **Authentication**: Verify user identity
- **Authorization**: Control access to resources
- **HTTPS**: Encrypt data transmission
- **Password Security**: Hashing and salting

### Security Example:
```javascript
// Input validation
const validator = require('validator');

function validateEmail(email) {
    return validator.isEmail(email);
}

// Password hashing with bcrypt
const bcrypt = require('bcrypt');

async function hashPassword(password) {
    const saltRounds = 10;
    return await bcrypt.hash(password, saltRounds);
}

// JWT authentication
const jwt = require('jsonwebtoken');

function generateToken(user) {
    return jwt.sign(
        { userId: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '24h' }
    );
}
```
            """
        },
        "Data Science": {
            "Core Concepts": """
# Core Concepts in Data Science

## Statistics Fundamentals
Statistics provides the mathematical foundation for data science.

### Descriptive Statistics:
- **Mean**: Average value of a dataset
- **Median**: Middle value when sorted
- **Mode**: Most frequent value
- **Standard Deviation**: Measure of data spread
- **Variance**: Square of standard deviation

### Example:
```python
import numpy as np
import pandas as pd

# Sample data
data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 1]

# Descriptive statistics
mean = np.mean(data)
median = np.median(data)
std_dev = np.std(data)

print(f"Mean: {mean}")
print(f"Median: {median}")
print(f"Standard Deviation: {std_dev}")
```

## Probability Theory
Probability quantifies uncertainty and likelihood.

### Key Concepts:
- **Probability**: Number between 0 and 1
- **Conditional Probability**: P(A|B)
- **Bayes' Theorem**: P(A|B) = P(B|A) × P(A) / P(B)
- **Random Variables**: Variables with uncertain values

### Probability Distributions:
- **Normal Distribution**: Bell-shaped curve
- **Binomial Distribution**: Success/failure scenarios
- **Poisson Distribution**: Rare events
- **Exponential Distribution**: Time between events

### Example:
```python
from scipy import stats
import matplotlib.pyplot as plt

# Normal distribution
mu, sigma = 0, 1  # mean and standard deviation
x = np.linspace(-3, 3, 100)
y = stats.norm.pdf(x, mu, sigma)

plt.plot(x, y)
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.show()
```

## Data Cleaning Techniques
Clean data is essential for accurate analysis.

### Common Data Issues:
- **Missing Values**: Incomplete data
- **Duplicates**: Repeated records
- **Outliers**: Extreme values
- **Inconsistent Formats**: Different data representations

### Cleaning Strategies:
- **Imputation**: Fill missing values
- **Deduplication**: Remove duplicates
- **Outlier Detection**: Identify extreme values
- **Standardization**: Consistent formatting

### Example:
```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Handle missing values
df['age'].fillna(df['age'].mean(), inplace=True)
df['salary'].fillna(df['salary'].median(), inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Detect outliers using IQR
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df = df[(df['salary'] >= lower_bound) & (df['salary'] <= upper_bound)]
```

## Exploratory Data Analysis (EDA)
EDA reveals patterns and insights in data.

### EDA Techniques:
- **Summary Statistics**: Basic data overview
- **Data Visualization**: Charts and graphs
- **Correlation Analysis**: Variable relationships
- **Distribution Analysis**: Data spread patterns

### Visualization Types:
- **Histograms**: Frequency distribution
- **Scatter Plots**: Variable relationships
- **Box Plots**: Distribution summary
- **Heatmaps**: Correlation matrices

### Example:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['age'], bins=20, alpha=0.7)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['age'], df['salary'])
plt.title('Age vs Salary')
plt.xlabel('Age')
plt.ylabel('Salary')
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
```

## Data Visualization Principles
Effective visualization communicates insights clearly.

### Best Practices:
- **Choose Right Chart Type**: Match data to visualization
- **Clear Labels**: Descriptive titles and axes
- **Appropriate Colors**: Meaningful color schemes
- **Avoid Clutter**: Simple, clean designs

### Chart Selection Guide:
- **Comparison**: Bar charts, line charts
- **Distribution**: Histograms, box plots
- **Relationship**: Scatter plots, heatmaps
- **Composition**: Pie charts, stacked bar charts

### Example:
```python
# Professional visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Age distribution
axes[0, 0].hist(df['age'], bins=15, alpha=0.7, color='skyblue')
axes[0, 0].set_title('Age Distribution')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')

# Salary by department
dept_salary = df.groupby('department')['salary'].mean()
axes[0, 1].bar(dept_salary.index, dept_salary.values, color='lightgreen')
axes[0, 1].set_title('Average Salary by Department')
axes[0, 1].set_xlabel('Department')
axes[0, 1].set_ylabel('Average Salary')
axes[0, 1].tick_params(axis='x', rotation=45)

# Experience vs Salary
axes[1, 0].scatter(df['experience'], df['salary'], alpha=0.6)
axes[1, 0].set_title('Experience vs Salary')
axes[1, 0].set_xlabel('Years of Experience')
axes[1, 0].set_ylabel('Salary')

# Gender distribution
gender_counts = df['gender'].value_counts()
axes[1, 1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
axes[1, 1].set_title('Gender Distribution')

plt.tight_layout()
plt.show()
```
            """,
            "Advanced Concepts": """
# Advanced Data Science Concepts

## Machine Learning Algorithms
Machine learning enables computers to learn from data.

### Supervised Learning:
- **Linear Regression**: Predict continuous values
- **Logistic Regression**: Predict binary outcomes
- **Decision Trees**: Tree-based decision making
- **Random Forest**: Ensemble of decision trees
- **Support Vector Machines**: Classification with margins
- **Neural Networks**: Deep learning models

### Unsupervised Learning:
- **K-Means Clustering**: Group similar data
- **Hierarchical Clustering**: Tree-based clustering
- **Principal Component Analysis**: Dimensionality reduction
- **Association Rules**: Find relationships in data

### Example:
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

# Load data
df = pd.read_csv('housing_data.csv')

# Prepare features and target
X = df[['size', 'bedrooms', 'location']]
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
print(f"Coefficients: {model.coef_}")
```

## Deep Learning
Deep learning uses neural networks with multiple layers.

### Neural Network Components:
- **Input Layer**: Receives data
- **Hidden Layers**: Process information
- **Output Layer**: Produces results
- **Activation Functions**: Introduce non-linearity
- **Loss Functions**: Measure prediction error
- **Optimization Algorithms**: Update weights

### Popular Frameworks:
- **TensorFlow**: Google's deep learning framework
- **Keras**: High-level neural network API
- **PyTorch**: Facebook's deep learning framework

### Example:
```python
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Generate sample data
X = np.random.rand(1000, 10)  # 1000 samples, 10 features
y = np.random.randint(0, 2, 1000)  # Binary classification

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Build neural network
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")
```

## Natural Language Processing (NLP)
NLP enables computers to understand human language.

### NLP Techniques:
- **Tokenization**: Split text into words
- **Stemming**: Reduce words to root form
- **Lemmatization**: Convert words to dictionary form
- **Sentiment Analysis**: Determine emotional tone
- **Named Entity Recognition**: Identify entities
- **Text Classification**: Categorize text

### Example:
```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Sample text
text = "Natural language processing is a subfield of artificial intelligence."

# Tokenization
tokens = word_tokenize(text.lower())

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word not in stop_words]

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

print("Original:", text)
print("Tokens:", tokens)
print("Filtered:", filtered_tokens)
print("Lemmatized:", lemmatized_tokens)

# Text classification example
documents = [
    "I love this product! It's amazing.",
    "This is terrible. I hate it.",
    "It's okay, not great but not bad.",
    "Absolutely fantastic! Highly recommended."
]

labels = [1, 0, 1, 1]  # 1: positive, 0: negative

# Vectorize text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Train classifier
classifier = MultinomialNB()
classifier.fit(X, labels)

# Predict
new_text = ["This product is wonderful!"]
new_X = vectorizer.transform(new_text)
prediction = classifier.predict(new_X)
print(f"Prediction: {'Positive' if prediction[0] == 1 else 'Negative'}")
```

## Computer Vision
Computer vision enables machines to interpret visual information.

### Computer Vision Tasks:
- **Image Classification**: Categorize images
- **Object Detection**: Locate objects in images
- **Image Segmentation**: Partition images into regions
- **Face Recognition**: Identify individuals
- **Optical Character Recognition**: Read text from images

### Example:
```python
import cv2
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image

# Load pre-trained model
model = VGG16(weights='imagenet')

# Load and preprocess image
img_path = 'example.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = tf.keras.applications.vgg16.preprocess_input(x)

# Make prediction
predictions = model.predict(x)

# Decode predictions
decoded_predictions = tf.keras.applications.vgg16.decode_predictions(predictions, top=5)[0]

print("Top 5 predictions:")
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    print(f"{i+1}: {label} ({score:.2f})")

# OpenCV example for image processing
image = cv2.imread('example.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Edge detection
edges = cv2.Canny(gray, 100, 200)

# Face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('Faces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Big Data Technologies
Big data tools handle massive datasets efficiently.

### Big Data Frameworks:
- **Apache Hadoop**: Distributed storage and processing
- **Apache Spark**: Fast cluster computing
- **Apache Kafka**: Real-time data streaming
- **Apache Flink**: Stream processing framework

### Example with PySpark:
```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# Create Spark session
spark = SparkSession.builder.appName("BigDataExample").getOrCreate()

# Load data
df = spark.read.csv("large_dataset.csv", header=True, inferSchema=True)

# Data preprocessing
df = df.dropna()
df = df.filter(df['price'] > 0)

# Feature engineering
assembler = VectorAssembler(
    inputCols=['size', 'bedrooms', 'age'],
    outputCol='features'
)
data = assembler.transform(df)

# Train model
lr = LinearRegression(featuresCol='features', labelCol='price')
model = lr.fit(data)

# Make predictions
predictions = model.transform(data)

# Show results
predictions.select('price', 'prediction').show(5)

# Save model
model.save("linear_regression_model")
```

## Model Deployment
Deployment makes models available for production use.

### Deployment Options:
- **REST APIs**: Web service endpoints
- **Batch Processing**: Scheduled predictions
- **Real-time Inference**: Immediate predictions
- **Edge Deployment**: On-device processing

### Flask API Example:
```python
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load('trained_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Make prediction
        prediction = model.predict(df)
        
        # Return result
        return jsonify({
            'prediction': prediction.tolist(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        })

if __name__ == '__main__':
    app.run(debug=True)
```

## Model Monitoring and Maintenance
Monitoring ensures model performance over time.

### Monitoring Metrics:
- **Accuracy**: Prediction correctness
- **Latency**: Response time
- **Throughput**: Requests per second
- **Data Drift**: Changes in data distribution
- **Model Drift**: Changes in model performance

### Maintenance Strategies:
- **Regular Retraining**: Update with new data
- **A/B Testing**: Compare model versions
- **Performance Tracking**: Monitor key metrics
- **Alert Systems**: Notify on issues
```
        }
    }
    
    # Default theory content for other categories
    default_theory = f"""
# Core Concepts in {category_name}

## Introduction
{category_name} is a fundamental field that requires understanding of key concepts and principles.

## Key Concepts
- **Concept 1**: Fundamental principle
- **Concept 2**: Core methodology
- **Concept 3**: Essential technique
- **Concept 4**: Important theory
- **Concept 5**: Critical knowledge

## Best Practices
- Follow industry standards
- Maintain quality and consistency
- Continuously learn and improve
- Apply theoretical knowledge practically

## Common Challenges
- Understanding complex concepts
- Applying theory to practice
- Staying updated with developments
- Problem-solving approaches

## Summary
Mastering these core concepts provides a strong foundation for advanced study and professional application.
    """
    
    return theory_content.get(category_name, {}).get(topic_title, default_theory)


def update_course_content():
    """Update course content with theory and video structure"""
    with app.app_context():
        try:
            categories = Category.query.all()
            
            for category in categories:
                print(f"🔄 Updating category: {category.name}")
                
                # Get all courses in this category
                courses = Course.query.filter_by(category_id=category.id).all()
                
                for course in courses:
                    print(f"  📚 Updating course: {course.name}")
                    
                    # Get all topics for this course
                    topics = CourseTopic.query.filter_by(course_id=course.id).order_by(CourseTopic.order).all()
                    
                    for topic in topics:
                        # Update Core Concepts with theory content
                        if "Core Concepts" in topic.title:
                            theory_content = get_theory_content(topic.title, category.name)
                            topic.notes_content = theory_content
                            topic.video_url = ""  # No video for core concepts
                            print(f"    📝 Updated theory for: {topic.title}")
                        
                        # Update Advanced Concepts with video placeholder
                        elif "Advanced Concepts" in topic.title:
                            # Keep existing notes but add video placeholder
                            if not topic.video_url:
                                topic.video_url = "https://example.com/video-placeholder"  # Admin can update this
                            print(f"    🎥 Added video placeholder for: {topic.title}")
                    
                    db.session.commit()
                    print(f"    ✅ Updated course: {course.name}")
                
                print(f"  ✅ Updated category: {category.name}")
            
            print("\n🎉 Course content update completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating course content: {e}")
            return False


if __name__ == "__main__":
    print("🔧 Updating Course Content Structure...")
    print("=" * 60)
    
    if update_course_content():
        print("✅ Course content updated successfully!")
        print("\n📋 Content Structure:")
        print("   • Core Concepts: Theory content only (no videos)")
        print("   • Advanced Concepts: Video content ready")
        print("   • Introduction, Final Assessment, Certificate: Unchanged")
        print("\n📝 Theory Content:")
        print("   • Web Development: HTML5, CSS3, JavaScript, Responsive Design")
        print("   • Data Science: Statistics, Probability, Data Cleaning, EDA")
        print("   • Other Categories: General theory content")
    else:
        print("❌ Course content update failed")
