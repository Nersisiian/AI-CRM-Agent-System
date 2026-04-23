run:
	docker-compose up -d

dev:
	uvicorn main:app --reload

train:
	python app/training/run_qlora.py

test:
	pytest tests/