# Assistive Navigation for the Visually Impaired

## Overview
This project is a mobile-based navigation aid for visually impaired users.  
It uses YOLOv8 for real-time object detection and OCR (Optical Character Recognition) to read aloud text from captured images via TTS (Text-to-Speech).  
The system is designed to improve safety and independence for visually impaired individuals during outdoor navigation.

## Features
- Real-time object detection using YOLOv8
- Distance estimation to trigger alerts when obstacles are within 10 meters
- OCR integration to extract and read aloud text from images
- WebSocket-based TTS alerts that operate alongside navigation guidance

## Tech Stack
- Frontend: Flutter
- Backend: Django, WebSocket
- Computer Vision: YOLOv8
- OCR: Tesseract OCR
- TTS: Naver Clova TTS
- Environment: Windows, Ubuntu

## Project Structure
<img width="948" height="639" alt="image" src="https://github.com/user-attachments/assets/f1027704-2368-4a16-bc62-efc8cc704d9b" />
