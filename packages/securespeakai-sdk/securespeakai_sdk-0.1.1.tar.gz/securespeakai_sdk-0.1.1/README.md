# SecureSpeak AI Python SDK

<div align="center">

![SecureSpeak AI](https://img.shields.io/badge/SecureSpeak-AI-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.1.0-orange?style=for-the-badge)

**The official Python SDK for SecureSpeak AI — Professional deepfake detection with 99.7% accuracy**

[🚀 Quick Start](#quick-start) • [📖 Documentation](#documentation) • [💡 Examples](#examples) • [🔧 Installation](#installation) • [🆘 Support](#support)

</div>

---

## 🌟 Features

- **🎯 High Accuracy**: 99.7% detection rate for AI-generated speech
- **🚀 Simple API**: Clean, intuitive Python interface
- **📁 Multiple Sources**: Analyze local files, URLs, and live audio
- **⚡ Fast Processing**: Real-time analysis capabilities
- **🔒 Secure**: Enterprise-grade security with API key authentication
- **📱 Flexible**: Support for multiple audio formats (WAV, MP3, FLAC, etc.)

## 🔧 Installation

### From PyPI (Recommended)

```bash
pip install securespeakai-sdk
```

### From Source

```bash
git clone https://github.com/your-org/securespeakai-sdk.git
cd securespeakai-sdk
pip install -e .
```

## 🚀 Quick Start

```python
from securespeak import SecureSpeakClient

# Initialize client with your API key
client = SecureSpeakClient("your-api-key-here")

# Analyze a local audio file
result = client.analyze_file("suspicious_audio.wav")

# Check if it's a deepfake
if result['is_deepfake']:
    print(f"🚨 DEEPFAKE DETECTED! Confidence: {result['confidence_score']}%")
else:
    print(f"✅ Authentic audio. Confidence: {result['confidence_score']}%")
```

## 📖 Documentation

### Authentication

Get your API key from the [SecureSpeak AI Dashboard](https://securespeakai.com/dashboard) and initialize the client:

```python
from securespeak import SecureSpeakClient

client = SecureSpeakClient("sk-your-api-key-here")
```

### Core Methods

#### `analyze_file(file_path)`

Analyze a local audio file for deepfake detection.

**Parameters:**
- `file_path` (str): Path to the audio file

**Supported formats:** WAV, MP3, FLAC, M4A, OGG, AIFF, WMA, OPUS

**Example:**
```python
result = client.analyze_file("audio_sample.wav")
```

#### `analyze_url(url)`

Analyze audio directly from a URL (supports YouTube, SoundCloud, direct links, etc.).

**Parameters:**
- `url` (str): URL containing audio content

**Example:**
```python
result = client.analyze_url("https://example.com/audio.mp3")
```

#### `analyze_live(file_path)`

Analyze audio with per-second billing (ideal for real-time applications).

**Parameters:**
- `file_path` (str): Path to the audio file

**Billing:** $0.032 per second of audio

**Example:**
```python
result = client.analyze_live("live_audio_chunk.wav")
```

## 💡 Examples

### Basic Usage

```python
from securespeak import SecureSpeakClient

# Initialize client
client = SecureSpeakClient("your-api-key")

# Analyze different audio sources
try:
    # Local file
    file_result = client.analyze_file("./audio/sample.wav")
    print(f"File analysis: {file_result['is_deepfake']}")
    
    # URL
    url_result = client.analyze_url("https://example.com/audio.mp3")
    print(f"URL analysis: {url_result['is_deepfake']}")
    
    # Live audio
    live_result = client.analyze_live("./live/chunk.wav")
    print(f"Live analysis: {live_result['is_deepfake']}")
    
except Exception as e:
    print(f"Error: {e}")
```

### Batch Processing

```python
import os
from securespeak import SecureSpeakClient

client = SecureSpeakClient("your-api-key")

def analyze_directory(directory_path):
    """Analyze all audio files in a directory"""
    results = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(('.wav', '.mp3', '.flac')):
            file_path = os.path.join(directory_path, filename)
            
            try:
                result = client.analyze_file(file_path)
                results.append({
                    'filename': filename,
                    'is_deepfake': result['is_deepfake'],
                    'confidence': result['confidence_score']
                })
                
            except Exception as e:
                print(f"Error analyzing {filename}: {e}")
    
    return results

# Analyze all files in a directory
results = analyze_directory("./audio_samples/")
for result in results:
    status = "🚨 DEEPFAKE" if result['is_deepfake'] else "✅ AUTHENTIC"
    print(f"{result['filename']}: {status} (Confidence: {result['confidence']}%)")
```

### Advanced Error Handling

```python
from securespeak import SecureSpeakClient
import requests

client = SecureSpeakClient("your-api-key")

def safe_analyze_file(file_path):
    """Analyze file with comprehensive error handling"""
    try:
        result = client.analyze_file(file_path)
        return {
            'success': True,
            'data': result,
            'error': None
        }
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {'success': False, 'error': 'Invalid API key'}
        elif e.response.status_code == 402:
            return {'success': False, 'error': 'Insufficient credits'}
        elif e.response.status_code == 429:
            return {'success': False, 'error': 'Rate limit exceeded'}
        else:
            return {'success': False, 'error': f'HTTP {e.response.status_code}'}
            
    except FileNotFoundError:
        return {'success': False, 'error': 'Audio file not found'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Usage
result = safe_analyze_file("audio.wav")
if result['success']:
    print(f"Analysis complete: {result['data']['is_deepfake']}")
else:
    print(f"Analysis failed: {result['error']}")
```

### Real-time Processing

```python
import time
from securespeak import SecureSpeakClient

client = SecureSpeakClient("your-api-key")

def monitor_audio_stream():
    """Monitor audio stream for deepfakes in real-time"""
    while True:
        try:
            # Assume you have a function that captures audio chunks
            audio_chunk = capture_audio_chunk()  # Your audio capture logic
            
            # Save chunk temporarily
            chunk_path = "temp_chunk.wav"
            save_audio_chunk(audio_chunk, chunk_path)
            
            # Analyze with live endpoint
            result = client.analyze_live(chunk_path)
            
            if result['is_deepfake']:
                print(f"🚨 ALERT: Deepfake detected! Confidence: {result['confidence_score']}%")
                # Trigger your alert system here
                
            # Clean up
            os.remove(chunk_path)
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            
        time.sleep(1)  # Process every second
```

## 📊 Response Format

All methods return a consistent JSON response:

```json
{
    "request_id": "req_abc123def456",
    "authenticity_score": 0.972,
    "is_deepfake": false,
    "confidence": "high",
    "confidence_score": 97.2,
    "classification": {
        "label": "Authentic",
        "raw_prediction": "Human",
        "score_explanation": "Model prediction: 97.2% Human"
    },
    "analysis_time_ms": 145,
    "audio_metadata": {
        "duration_sec": 4.2,
        "sample_rate": 44100,
        "channels": 1,
        "format": "wav",
        "file_size_bytes": 352800
    },
    "detected_technologies": [],
    "risk_factors": [],
    "source_info": {
        "endpoint": "/analyze_file",
        "filename": "audio-sample.wav",
        "source_type": "uploaded_file"
    },
    "timestamps": {
        "received_at": "2024-01-15T10:30:45Z",
        "analyzed_at": "2024-01-15T10:30:45Z"
    },
    "api_version": "1.2.0"
}
```

### Key Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `is_deepfake` | boolean | Whether the audio is detected as fake |
| `authenticity_score` | float | Score from 0.0 (fake) to 1.0 (authentic) |
| `confidence_score` | float | Confidence percentage (0-100) |
| `confidence` | string | Confidence level: "low", "medium", "high" |
| `analysis_time_ms` | integer | Processing time in milliseconds |
| `audio_metadata` | object | Technical audio information |

## 🔧 Requirements

- **Python**: 3.7 or higher
- **Dependencies**: 
  - `requests` >= 2.25.0

## 💰 Pricing

| Endpoint | Cost | Best For |
|----------|------|----------|
| `analyze_file` | $0.018 per request | Batch processing |
| `analyze_url` | $0.025 per request | Social media monitoring |
| `analyze_live` | $0.032 per second | Real-time applications |

## 🚨 Error Handling

The SDK raises standard HTTP exceptions for API errors:

```python
import requests

try:
    result = client.analyze_file("audio.wav")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 402:
        print("Insufficient credits")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"API error: {e}")
except FileNotFoundError:
    print("Audio file not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🛡️ Security Best Practices

1. **Store API keys securely** - use environment variables
2. **Validate input files** - check file types and sizes
3. **Handle errors gracefully** - implement proper exception handling
4. **Monitor usage** - track API calls and costs
5. **Rate limiting** - implement backoff strategies

```python
import os
from securespeak import SecureSpeakClient

# Secure API key handling
api_key = os.getenv('SECURESPEAKAI_API_KEY')
if not api_key:
    raise ValueError("API key not found in environment variables")

client = SecureSpeakClient(api_key)
```

## 📈 Performance Tips

- **Batch processing**: Group multiple files for efficient processing
- **Optimal file sizes**: Keep files under 10MB for best performance
- **Error handling**: Implement retry logic for transient errors
- **Caching**: Cache results for repeated analyses
- **Monitoring**: Track API usage and response times

## 🧪 Testing

```python
# Test your integration
from securespeak import SecureSpeakClient

def test_integration():
    client = SecureSpeakClient("your-test-api-key")
    
    # Test with a known audio file
    result = client.analyze_file("test_audio.wav")
    
    assert 'is_deepfake' in result
    assert 'confidence_score' in result
    assert isinstance(result['is_deepfake'], bool)
    
    print("✅ Integration test passed!")

test_integration()
```