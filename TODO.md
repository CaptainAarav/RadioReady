# Ham Radio Quiz Bot — TODO

## ✅ Phase 1: Setup
- [✅] Create project folder `ham-radio-bot/`
- [✅] Set up a virtual environment (`python -m venv venv`)
- [✅] Install disnake (`pip install disnake`)
- [✅] Install python-dotenv (`pip install python-dotenv`)
- [✅] Create a Discord application and bot at discord.com/developers
- [✅] Store bot token in a `.env` file

## Phase 2: Question Bank
- [✅] Create `questions.json`
- [✅] Structure each question with: text, options (A–D), answer, category
- [✅] Write at least 30 questions covering: band plans, Q-codes, EIRP/ERP limits, callsign rules, operating practices

## Phase 3: Core Bot
- [ ] Create `main.py` and connect the bot to Discord
- [ ] Load question bank from `questions.json` on startup
- [ ] Build `/quiz` slash command — sends a random question with A/B/C/D buttons
- [ ] Handle button interactions — tell the user if they're right or wrong
- [ ] Build `/bandplan` slash command — look up a band by name (e.g. `/bandplan 2m`)
- [ ] Build `/qcode` slash command — explain a Q-code (e.g. `/qcode QRM`)

## Phase 4: Score Tracking
- [ ] Set up SQLite database with a scores table (user_id, correct, total)
- [ ] Record each quiz answer to the database
- [ ] Build `/score` slash command — show the user their personal stats
- [ ] Build `/leaderboard` slash command — top 5 in the server

## Phase 5: Polish & Deploy
- [ ] Add category filter to `/quiz` (e.g. `/quiz category:bandplan`)
- [ ] Write a Dockerfile
- [ ] Deploy to Raspberry Pi via Docker Compose
- [ ] Test in your Discord server
- [ ] Share in the OARC Discord