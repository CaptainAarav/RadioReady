# RadioReady

A Discord bot to help you study for your UK Amateur Radio Foundation licence exam.
I am planning to eventually add question for intermediate and full licence exams.

Quiz yourself on band plans, licence conditions, EMC, propagation, safety, and more — all based on the official RSGB syllabus V1.6.

---

## Features

- `/quiz` — Take a quiz with a configurable number of questions, answered via interactive buttons
- `/bandplan_info` - Lets you view the info the selected bandplan
- `/qcode_info` - Lets you view the info the selected Q-code
- `/help` - Displays a list of commands and their usage
- `/leaderboard` - Displays the top 10 players and their scores
- `/my_stats` - Displays the number of questions answered and the total score
- `/ping` - Displays the bot's latency
- Questions sourced directly from official RSGB Foundation mock exam papers (Syllabus V1.6, September 2024)
- Score tracking and leaderboard
---

## Tech Stack

- Python 3.13-slim(we use slim so that you don't have to use the full python image when building in docker)
- [disnake](https://docs.disnake.dev/) library
- Docker + Docker Compose
- Hosted on a Raspberry Pi 4B

---

## Self Hosting

### Prerequisites

- Docker and Docker Compose installed
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Setup

1. Clone the repo
   ```bash
   git clone https://github.com/CaptainAarav/RadioReady.git
   cd RadioReady
   ```

2. Create a `.env` file in the project root
   ```
   TOKEN=your_bot_token_here
   ```

3. Build and run with Docker Compose
   ```bash
   docker compose build && docker compose up -d
   ```

4. Check the logs
   ```bash
   docker compose logs -f
   ```

---

## Project Structure

```
ham-radio-bot/
├── cogs/
│   └── quiz.py        # Quiz command and logic
├── data/
│   └── questions.json # JSON for all questions (RSGB V1.6)
├── main.py            # Initialisation of the Bot
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Question Bank

All questions are taken from official RSGB Foundation mock exam papers for syllabus V1.6, which came into effect on 1 September 2024. Questions that require diagrams or images have been excluded as they cannot be represented in text form.

Categories covered:

- Licence conditions
- Band plans
- Technical (receivers, transmitters, antennas)
- Propagation
- EMC (electromagnetic compatibility)
- Operating practice
- Safety
- EIRP / ERP

---

## Contributing

Pull requests are welcome! If you want to contribute — whether that's adding questions, fixing bugs, or building new features, open a PR and I'll review it. If it gets accepted, your name will be added to the contributors list below.

### Contributors

*No contributors yet*

---

## Licence

MIT

---

> Built by [Aarav Sahni](https://github.com/CaptainAarav) — M7NBO
