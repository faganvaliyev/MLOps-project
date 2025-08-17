# 💼 DataMinds'25 DM Office Sales Predictor - Frontend


A modern, user-friendly **Streamlit** application for making **machine learning predictions** with an intuitive drag-and-drop interface.


## 🌟 Features


- **📁 Easy File Upload**: Supports CSV, Excel (.xlsx, .xls) files  
- **👀 Data Preview**: Interactive preview and statistics  
- **🔮 Batch Predictions**: Generate predictions for uploaded datasets  
- **🖊️ Single Prediction**: Input feature values manually for a single prediction  
- **📊 Results Visualization**: Display predictions in tables and metrics  
- **📥 Export Functionality**: Download predictions as CSV  
- **⚡ Session Management**: Persistent file handling across interactions  


## 🛠️ Technology Stack


- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas
- **HTTP Client**: Requests
- **File Handling**: BytesIO for efficient memory management
- **UI Components**: Custom Streamlit components with enhanced styling
- **Dependency Management**: UV (ultra-fast Python package installer)
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose integration

## 🐳 Docker Setup

This frontend application is fully containerized and designed to work as part of a Docker Compose stack.

### Prerequisites

- Docker 20.10+ 
- Docker Compose 2.0+

### Project Dependencies

Dependencies are managed using **UV** for faster, more reliable installations:

```toml
# pyproject.toml
[project]
dependencies = [
    "openpyxl>=3.1.5",
    "streamlit>=1.48.1",
    "pandas>=2.3.1", 
    "requests>=2.28.0",
    "plotly>=6.3.0"
]
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The frontend is part of a larger Docker Compose application:

```bash
# Run the entire stack
docker-compose up -d

# View logs
docker-compose logs frontend

# Stop the stack
docker-compose down
```

The application will be available at `http://localhost:8501`

### Option 2: Standalone Docker

```bash
# Build the frontend image
docker build -t dataminds-frontend .

# Run the container
docker run -p 8501:8501 \
  -e BACKEND_URL=http://backend:8000 \
  dataminds-frontend
```

### Option 3: Local Development

For local development without Docker:

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run streamlit run app.py
```

## 🏗️ Project Structure

### Application Structure

```
frontend/
├── streamlit_app/
│   │
│   ├─ app.py                     # Main entry point
│   ├─ config.py                  # Configs like API URL, constants
│   ├─ utils.py                   # Helper functions (file upload, API calls, etc.)
│   └─ tabs/
│       ├─ dataset_tab.py         # Dataset preview tab
│       ├─ batch_tab.py           # Batch prediction tab
│       ├─ single_tab.py          # Single input prediction tab
│       └─ visualizations_tab.py  # Visualizations tab
├── Dockerfile             # Container build instructions
├── pyproject.toml         # UV dependencies
├── uv.lock                # Locked dependency versions
└── README.md              # Documentation

```

### Key Components

1. **File Upload Handler**: Manages CSV/Excel file uploads with validation
2. **Data Processor**: Loads and previews uploaded data using pandas
3. **API Client**: Communicates with backend ML service
4. **Results Manager**: Displays predictions and handles downloads
5. **Session State**: Maintains application state across interactions

## 🔧 Configuration

### Environment Variables

The application can be configured via environment variables:

```bash
# Backend API endpoint
BACKEND_URL=http://backend:8000

# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Docker Compose Integration

This frontend service integrates with other services in the Docker Compose stack:

```yaml
# Example docker-compose.yml snippet
services:
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    networks:
      - safe_networks
    restart: always
    image: frontend
    container_name: frontend
    volumes:
      - ./frontend:/app
      - frontend_venv:/app/.venv
    ports:
      - "8501:8501"
```

### Backend API Configuration

The application communicates with the backend ML service:

```python
# Default configuration
api_url = "http://backend:8000/predict"
```

### Supported File Formats

- **CSV**: `.csv` files with comma-separated values
- **Excel**: `.xlsx` and `.xls` files

## 📊 Usage Guide

### Step 1: Upload Your Data

1. Use the sidebar file uploader
2. Select a CSV or Excel file
3. View the automatic data preview

### Step 2: Review Data

- **Dataset Overview**: View file metrics (rows, columns, size)
- **Data Preview**: Inspect your data structure
- **Statistics**: Optional statistical summary

### Step 3: Generate Predictions (batch or single) and plot visuals

1. Click the "🚀 Generate Predictions" button
2. Wait for backend processing
3. View results with processing time metrics

### Step 4: Download Results

- Download predictions as CSV file
- Results include original data + prediction column

## 🎯 Expected Data Format

Your input data should be structured with:
- **Features in columns**: Each column represents a data feature
- **Samples in rows**: Each row represents a data point
- **Clean data**: No missing headers, properly formatted values

### Example Format

| Feature_1 | Feature_2 | Feature_3 |  target  |
|-----------|-----------|-----------|----------|
| 1.2       | 0.8       | 10        |  value1  |
| 2.1       | 1.5       | 15        |  value2  |
| 3.4       | 2.3       | 20        |  value3  |

## 🔌 API Integration

### Backend Requirements

The frontend expects a backend service with:

- **Endpoint**: `POST /predict`
- **Input**: Multipart form data with file upload
- **Output**: JSON response with predictions

### Expected API Response Format

```json
{
  "status": "success",
  "message": "Predictions generated successfully",
  "data": {
    "predictions": [123621, 334823, 321344, ...],
    "num_predictions": 200,
    "processing_time_seconds": 0.23
  }
}
```

### Error Handling

The application handles various error scenarios:
- Network connectivity issues
- Invalid file formats
- Backend service errors
- Malformed API responses

## 🎨 UI Features

### Visual Elements

- **Modern Design**: Clean, professional interface
- **Progress Indicators**: Loading spinners for async operations
- **Success Messages**: Visual feedback for successful operations
- **Metrics Display**: Key statistics prominently displayed
- **Expandable Sections**: Organized content with collapsible panels

### Session Management

- **Persistent State**: Uploaded files remain available across interactions
- **Smart Caching**: Efficient memory usage with BytesIO
- **State Cleanup**: Automatic cleanup when files are removed

## 🔒 Security Considerations

- **File Validation**: MIME type detection and validation
- **Size Limits**: Streamlit's built-in file size restrictions
- **Network Timeouts**: 60-second timeout for API calls
- **Error Sanitization**: Safe error message display

## 📈 Performance Features

- **Efficient Data Loading**: BytesIO for memory-efficient file handling
- **Preview Limits**: Display only first 100 rows for large datasets
- **Async Operations**: Non-blocking UI during predictions
- **Response Caching**: Session state prevents redundant operations