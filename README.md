# Flower Classification

A Deep Learning based web application for classifying flower species. The application uses a pre-trained model fine-tuned for flower recognition and provides both a REST API and web interface for predictions.

## Features

- **35 Flower Species Recognition**
- **FastAPI Backend**: Fast, modern Python API framework with automatic documentation
- **Web Interface**: User-friendly frontend for image uploads and predictions
- **Feedback Mechanism**: Feedback mechanism collects data for incorrect predictions and improve the model

## Supported Flower Classes

Amaltas, Ashokatree, Bottlebrushtree, Bougainvillea, Butterflypea, Chrysanthemum, Cockscomb, Cosmos, Dahlia, Gulmohar, Hibiscus, Ixora, Jasmine, Kachnar, Lantana, Lotus, Marigold, Mexicanpetunia, Nightqueen, Oleander, Palash, Periwinkle, Petunia, Plumeria, Portulaca, Prideofindia, Rainlily, Rangooncreeper, Rose, Silkcottontree, Spiderlily, Sunflower, Trumpettree, Tuberose, Zinnia

## Usage

Build the project:
In project directory
```bash
mkdir HuggingFace/flower-classification
bash build.sh
```

Now go to HuggingFace/flower-classification and Build the container image:
```bash
podman build -t flower-classification .
```

Run the container:
```bash
podman run -p 7860:7860 flower-classification
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the repository.
