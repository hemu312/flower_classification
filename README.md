# Flower Classification

A deep learning-based web application for classifying flower species. The application uses a pre-trained model fine-tuned for flower recognition and provides both a REST API and web interface for predictions.

## Features

- **35 Flower Species Recognition**: Classifies flowers including roses, sunflowers, tulips, lilies, and many more
- **Top-5 Predictions**: Returns the top 5 most likely classifications with confidence scores
- **FastAPI Backend**: Fast, modern Python API framework with automatic documentation
- **Web Interface**: User-friendly frontend for image uploads and predictions

## Supported Flower Classes

Amaltas, Ashokatree, Bottlebrushtree, Bougainvillea, Butterflypea, Chrysanthemum, Cockscomb, Cosmos, Dahlia, Gulmohar, Hibiscus, Ixora, Jasmine, Kachnar, Lantana, Lotus, Marigold, Mexicanpetunia, Nightqueen, Oleander, Palash, Periwinkle, Petunia, Plumeria, Portulaca, Prideofindia, Rainlily, Rangooncreeper, Rose, Silkcottontree, Spiderlily, Sunflower, Trumpettree, Tuberose, Zinnia

## Usage

Build the container image:
```bash
podman build -t flower-classification .
```

Run the container:
```bash
podman run -p 7860:7860 flower-classification
```

## API Endpoint

### POST `/predict`

Upload an image for flower classification.

**Request:**
- Method: `POST`
- Endpoint: `/predict`
- Content-Type: `multipart/form-data`
- Parameter: `image` (image file)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the repository.
