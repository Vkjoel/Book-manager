FROM python:3.10-slim

# Installeer vereiste Python-pakketten
RUN pip install fastapi uvicorn requests

# Stel de werkdirectory in
WORKDIR /app

# Kopieer de applicatiecode
COPY book_manager.py /app/

# Exposeer poort
EXPOSE 8000

# Start de applicatie
CMD ["uvicorn", "book_manager:app", "--host", "0.0.0.0", "--port", "8000"]
